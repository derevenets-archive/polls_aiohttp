import aiohttp_jinja2
import jinja2
from aiohttp import web
from db import init_pg, close_pg
from routes import setup_routes
from settings import config

app = web.Application()

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

# setup Jinja2 template renderer
aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('src', 'templates'))

setup_routes(app)
app['config'] = config
web.run_app(app)
