import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

question = Table(
    'question', meta,

    Column('id', Integer, primary_key=True),
    Column('question_text', String(200), nullable=False),
    Column('pub_date', Date, nullable=False),
)

choice = Table(
    'choice', meta,

    Column('id', Integer, primary_key=True),
    Column('choice_text', String(200), nullable=False),
    Column('votes', Integer, server_default='0', nullable=False),
    Column(
        'question_id',
        Integer,
        ForeignKey('question.id', ondelete='CASCADE')
    )
)


async def init_pg(app):
    """For making DB queries we need an engine instance"""
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**conf)  # TODO: explicitly?
    app['db'] = engine


async def close_pg(app):
    """It is a good practice to close all resources on program exit"""
    app['db'].close()
    await app['db'].wait_closed()
