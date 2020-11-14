import asyncio

from sanic.log import logger

from agile_photo_collection.cache import DictBasedCache
from agile_photo_collection.rest_clients import agile_engine_photo_client


class CachePhotosUseCase:
    def __init__(self, cache):
        self.cache: DictBasedCache = cache
        self.client = agile_engine_photo_client

    async def run(self):
        logger.debug(f"Use case: {self.__class__.__name__} started")
        result = await self.client.get_photos()
        await self._cache_pictures(result["pictures"])
        coros = [self._cache_page(i) for i in range(2, result["pageCount"] + 1)]
        await asyncio.gather(*coros)
        logger.info(f"Cache created")

    async def _cache_pictures(self, pictures):
        logger.debug(f"cache pictures")
        pics = await asyncio.gather(
            *[self.client.get_photo(pic["id"]) for pic in pictures]
        )
        for pic in pics:
            pic["tags"] = [t.strip() for t in pic["tags"].split("#") if t.strip()]
            self.cache.index(pic)

    async def _cache_page(self, page):
        result = await self.client.get_photos(page=page)
        await self._cache_pictures(result["pictures"])
