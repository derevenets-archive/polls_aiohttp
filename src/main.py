import aiohttp_jinja2
import jinja2
from aiohttp import web
from db import init_pg, close_pg
from routes import setup_routes
from settings import config
from middlewares import setup_middlewares


async def init_app():
    app = web.Application()
    app['config'] = config

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    # setup views and route
    setup_routes(app)

    setup_middlewares(app)

    return app


def main():
    app = init_app()
    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main()
