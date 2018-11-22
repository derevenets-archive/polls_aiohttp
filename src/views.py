import aiohttp_jinja2
from aiohttp import web
from db import get_question
from exceptions import RecordNotFound


async def index(request):
    return web.Response(text='Hello Aiohttp!')


@aiohttp_jinja2.template('detail.html')
async def poll(request):
    async with request.app['db'].ascuire() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = get_question(conn, question_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {
            'question': question,
            'choices': choices
        }
