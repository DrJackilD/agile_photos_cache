import asyncio
from asyncio.base_events import BaseEventLoop

from sanic import Sanic
from sanic.log import logger
from sanic.request import Request
from sanic.response import json

from agile_photo_collection import settings
from agile_photo_collection.cache import DictBasedCache
from agile_photo_collection.use_cases import CachePhotosUseCase

app = Sanic(__name__)


@app.listener("before_server_start")
async def cache_photos(application: Sanic, _):
    application.cache = DictBasedCache("id", ["author", "camera", "tags"])
    await CachePhotosUseCase(application.cache).run()


async def update_cache(application, loop):
    try:
        logger.debug(f"update_cache sleep for {settings.CACHE_UPDATE_DELAY} seconds")
        await asyncio.sleep(settings.CACHE_UPDATE_DELAY)
        logger.debug(f"update_cache started")
        application.cache = DictBasedCache("id", ["author", "camera", "tags"])
        await CachePhotosUseCase(application.cache).run()
        logger.debug(f"update_cache finished")
        application.refresh_cache_task = loop.create_task(
            update_cache(application, loop)
        )
    except asyncio.CancelledError:
        logger.info("Shutdown update_cache")


@app.listener("after_server_start")
async def schedule_refresh_cache_task(application: Sanic, loop: BaseEventLoop):
    application.refresh_cache_task = loop.create_task(update_cache(application, loop))


@app.listener("before_server_stop")
async def stop_refresh_cache(application: Sanic, _):
    application.refresh_cache_task.cancel()


@app.route("/search/<term:path>")
async def search(request: Request, term):
    data = request.app.cache.get_by_index(term)
    return json({"data": data})
