import aiopg.sa


async def init_pg(app):
    """For making DB queries we need an engine instance"""
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**conf)  # TODO: explicitly?
    app['db'] = engine


async def close_pg(app):
    """It is a good practice to close all resources on program exit"""
    app['db'].close()
    await app['db'].wait_closed()
