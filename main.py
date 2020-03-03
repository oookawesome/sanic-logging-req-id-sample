import uuid

from sanic import Sanic
from sanic.log import logger
from sanic.response import json

from src.ctx import Ctx
from src.sample import Sample
from src.settings import CUSTOM_LOG_CONFIG

app = Sanic(log_config=CUSTOM_LOG_CONFIG)


@app.middleware('request')
async def add_key(request):
    Ctx.request_id.set(str(uuid.uuid4())[:8])


@app.route("/")
async def test(request):
    logger.info('Get request.')
    s = Sample()
    s.print_text()
    return json({"hello": "world"})


if __name__ == "__main__":
    logger.info('--------------------------------')
    logger.info('-------- Server Started! -------')
    logger.info('--------------------------------')
    app.run(host="0.0.0.0", port=8000)
