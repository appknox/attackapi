import pickle

import redis


rc = redis.StrictRedis(host='localhost', port=6379, db=0)


def response(flow):
    client_address = str(flow.client_conn.address).split(':')[0]
    path = flow.request.path
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
    print('Tracked: {}://{}{}'.format(r.scheme, r.host, r.path)[:100])
