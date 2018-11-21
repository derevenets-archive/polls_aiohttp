from aiohttp import web

from settings import config
from routes import setup_routes
from db import init_pg, close_pg

app = web.Application()

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

setup_routes(app)
app['config'] = config
web.run_app(app)

