import random
import string
import datetime
from settings import db

import aiomysql as aiomysql
from aiohttp import web

from routes import routes


@web.middleware
async def log_middleware(request, handler):
    request._dt = datetime.datetime.now()
    request._hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    print('{} : '.format(request._hash))
    resp = await handler(request)
    print('{} : [{} - {}] {}({}) {}'.format(
        request._hash, request._dt, datetime.datetime.now(), request.method, resp.status, request.path_qs))
    return resp


async def connect_to_db(app):
    app['db_pool'] = await aiomysql.create_pool(
            host=db['host'],
            db=db['database'],
            user=db['user'],
            password=db['password'],
            autocommit=db['autocommit'],
            charset=db['charset'])


async def close_connection(app):
    app['db_pool'].terminate()
    await app['db_pool'].wait_closed()


async def launch_server(*, ssh_tunnel=None, debug=...):
    app = web.Application(debug=debug, middlewares=[log_middleware], client_max_size=1024*1024*10)
    app['ssh_tunnel'] = ssh_tunnel

    app.on_startup.append(connect_to_db)
    app.on_cleanup.append(close_connection)
    if ssh_tunnel:
        async def close_ssh(application):
            if application['ssh_tunnel'].is_active:
                application['ssh_tunnel'].close()

        app.on_cleanup.append(close_ssh)

    for route in routes:
        app.router.add_route(*route)

    return app


if __name__ == "__main__":
    web.run_app(launch_server(), host='0.0.0.0', port=8080)
