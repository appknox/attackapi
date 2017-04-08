import pickle

import redis

from attackapi.utils import can_ignore, Colors, color_print


rc = redis.StrictRedis(host='localhost', port=6379, db=0)


def response(flow):
    client_address = str(flow.client_conn.address).split(':')[0]
    path = flow.request.path
    r = flow.request
    if can_ignore(r):
        url = '{}://{}{}'.format(r.scheme, r.host, r.path)[:100]
        striked_url = '\u0336'.join(url) + '\u0336'
        text = 'IGNORED: {}'.format(striked_url)
        color_print(text, Colors.OKBLUE)
        return
    req = dict(
        client_address=client_address,
        path=path,

        method=flow.request.method,
        http_version=flow.request.http_version,

        scheme=flow.request.scheme,
        host=flow.request.host,
        port=flow.request.port,

        headers=flow.request.headers,
        body=flow.request.raw_content,
    )
    pkl = pickle.dumps(req)
    rc.publish('attackapi', pkl)
    r = flow.request
    text = 'TRACKED: {}://{}{}'.format(r.scheme, r.host, r.path)[:100]
    color_print(text, Colors.OKGREEN)
