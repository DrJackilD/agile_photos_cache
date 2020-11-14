import typing as t
from http import HTTPStatus
from urllib.parse import urljoin

import ujson
from aiohttp.client import ClientSession
from sanic.log import logger

from agile_photo_collection import settings

AVAILABLE_METHODS = t.Union[t.Literal["GET"], t.Literal["POST"], t.Literal["HEAD"]]


class ApiMethods:
    get: t.Literal["GET"] = "GET"
    post: t.Literal["POST"] = "POST"
    head: t.Literal["HEAD"] = "HEAD"


def ensure_auth(func):
    async def ensure_auth_func(self, *args, **kwargs):
        await self._auth()
        return await func(self, *args, **kwargs)

    return ensure_auth_func


class RestClientResponse:
    def __init__(self, data: t.Union[str, dict], status: int):
        self.data = data
        self.status = status


class AgileEnginePhotoRestClient:
    base_url = "http://interview.agileengine.com:80"

    token: t.Optional[str] = None
    headers: t.Optional[dict]

    def __init__(self):
        self.headers = None

    async def _auth(self):
        if self.token is not None:
            # check, that token is still valid
            r = await self._make_request(
                "/images",
                ApiMethods.head,
            )
            if r.status == HTTPStatus.OK:
                return

        r = await self._make_request(
            "/auth", ApiMethods.post, data={"apiKey": settings.AGILE_PHOTO_API_KEY}
        )
        if not r.data["auth"]:
            raise RestClientException("Can not authorize with provided token")
        self.token = r.data["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @ensure_auth
    async def get_photos(self, page: int = 1, limit: int = 20) -> dict:
        logger.debug(f"get photos: page={page}, limit={limit}")
        uri = f"/images?page={page}&limit={limit}"
        r = await self._make_request(uri, ApiMethods.get)
        return r.data

    @ensure_auth
    async def get_photo(self, id_) -> dict:
        logger.debug(f"get photo with id: {id_}")
        uri = f"/images/{id_}"
        r = await self._make_request(uri, ApiMethods.get)
        return r.data

    async def _make_request(
        self,
        uri: str,
        method: AVAILABLE_METHODS,
        data: dict = None,
    ) -> RestClientResponse:
        url = urljoin(self.base_url, uri)
        logger.debug(f"{method} {url}: request")
        async with ClientSession() as session:
            if method in [ApiMethods.get, ApiMethods.post]:
                if method == ApiMethods.get:
                    r = await session.get(url, headers=self.headers)
                else:
                    headers = self.headers or {}
                    headers["Content-Type"] = "application/json"
                    r = await session.post(url, headers=headers, data=ujson.dumps(data))
                response = RestClientResponse(await r.json(), r.status)
            elif method == ApiMethods.head:
                r = await session.head(url, headers=self.headers, data=data)
                response = RestClientResponse(await r.text(), r.status)
            else:
                raise RestClientException(f"Invalid API method: {method}")
        logger.debug(f"{method} {url}: status: {r.status}")
        return response


class RestClientException(Exception):
    pass


agile_engine_photo_client = AgileEnginePhotoRestClient()
