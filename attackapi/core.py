import json
import os
import pickle
import shlex
import subprocess
import sys
import threading
import tempfile
import yaml
from os.path import dirname, join

import jinja2
import redis


from .utils import get_ip


rc = redis.StrictRedis(host='localhost', port=6379, db=0)

CHANNEL = 'attackapi'

TEMPLATE = jinja2.Template("""{{ method }} {{ path }} {{ http_version }}
Host: {{ host }}:{{ port }}
{% for k, v in headers.items() %}{{ k }}: {{ v }}
{% endfor %}{% if body %}
{{ body }}{% endif %}
""")


tmp_dir = '/tmp/attackapi/'


MAPPINGS = {
    'FUZZ': ['500_errors', 'length_diff'],
    'BUFFER_OVERFLOW': ['bof_strings', 'bof_timing'],
    'COMMAND_INJECTION': ['command_injection'],
    'INTEGER_OVERFLOW': ['int_timing'],
    'JSON_DEPTH_OVERFLOW': ['json_depth_limit_strings', 'json_depth_timing'],
    'LDAP_INJECTION': [],
    'REDOS': ['redos_timing'],
    'SQL_INJECTION': ['sql_strings', 'sql_timing'],
    'STRING_VALIDATION': [],
    'XML_EXTERNAL_ENTITY': ['xml_strings', 'xml_timing'],
    'XSS': ['xss_strings'],
    'CORS_WILDCARD': ['CORS_HEADER'],
    'XST': ['XST_HEADER'],
    'SSL_ENDPOINT': ['SSL_ERROR'],
}

FNULL = open(os.devnull, 'w')


def syntribos_scan(url, template, out_file):
    cmd = ('syntribos --syntribos-endpoint {} --syntribos-templates {}'
           ' --outfile {} run'.format(url, template, out_file))
    subprocess.call(shlex.split(cmd), stderr=FNULL, stdout=FNULL)
    # subprocess.call(shlex.split(cmd))


def detect_vulnerability(failure):
    for name, defect_types in MAPPINGS:
        if failure['defect_type'] in defect_types:
            description = '{}: {}\n'.format(
                failure['url'], failure['description'].replace('\n', '. ')
            )
        instances = failure.get('instances', [])
        for instance in instances:
            instance.pop('strings', None)
            instance.pop('signals', None)
            description = '\n'.join([description, yaml.dump(instance)])
        return description


def analyze_results(results):
    vulnerabilities = []
    failures = results['failures']
    for failure in failures:
        vulnerability = detect_vulnerability(failure)
        if vulnerability:
            vulnerabilities.append(vulnerability)
    return vulnerabilities


def detect_vulnerabilities(request):
    r = request
    url = '{}://{}:{}'.format(r['scheme'], r['host'], r['port'])
    print('ATTACKING: {}/{}'.format(url, r['path']))
    _, template_file = tempfile.mkstemp(dir=tmp_dir, suffix='.template')
    with open(template_file, 'w') as fh:
        fh.write(TEMPLATE.render(**request))
    _, out_file = tempfile.mkstemp(dir=tmp_dir, suffix='.out')
    syntribos_scan(url, template_file, out_file)
    results = json.load(open(out_file))
    vulnerabilities = analyze_results(results)
    return vulnerabilities


def attack():
    print('Attacking tracked APIs')
    ps = rc.pubsub()
    ps.psubscribe(CHANNEL)
    while True:
        for message in ps.listen():
            data = message['data']
            if data == 1:
                continue
            request = pickle.loads(data)
            try:
                vulnerabilities = detect_vulnerabilities(request)
                print(vulnerabilities)
            except Exception as e:
                print(e)
                # print(type(data),len(data))


def monitor():
    ip_address = get_ip()
    port = 8080
    print()
    print('Visit mitm.it and install certificate'.format(ip_address, port))
    print('Starting proxy on {}:{}'.format(ip_address, port))
    print()
    thread = threading.Thread(target=attack)
    thread.start()
    script = join(dirname(__file__), 'store_requests.py')
    cmd = 'mitmdump -s {}'.format(script)
    cmd = shlex.split(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        if b'Tracked: ' in line:
            sys.stdout.write(line.decode())
