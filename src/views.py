import aiohttp_jinja2
import models
from aiohttp import web
from db import get_question, make_vote
from exceptions import RecordNotFound


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(models.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return {'questions': questions}


@aiohttp_jinja2.template('detail.html')
async def poll(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = await get_question(conn, question_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'question': question,
            'choices': choices
        }


@aiohttp_jinja2.template('results.html')
async def results(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = await get_question(conn, question_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'question': question,
            'choices': choices
        }


async def vote(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        data = await request.post()
        try:
            choice_id = data['choice']
        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='You have not specified choice value') from e
        try:
            await make_vote(conn, question_id, choice_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        url = request.app.router['results'].url_for(question_id=question_id)
        return web.HTTPFound(location=url)
