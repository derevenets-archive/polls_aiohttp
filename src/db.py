import aiopg.sa

from exceptions import RecordNotFound


async def init_pg(app):
    """For making DB queries we need an engine instance"""
    pg_config = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**pg_config)
    app['db'] = engine


async def close_pg(app):
    """It is a good practice to close all resources on program exit"""
    app['db'].close()
    await app['db'].wait_closed()


async def get_question(conn, question_id):
    result = await conn.execute(
        question.select().where(question.c.id == question_id)
    )
    question_record = await result.first()
    if not question_record:
        raise RecordNotFound(f"Question with id: {question_id} does not exists")
    result = await conn.execute(
        choice.select()
            .where(choice.c.id == question_id)
            .order_by(choice.c.id)
    )
    choice_records = await result.fetchall()
    return question_record, choice_records
