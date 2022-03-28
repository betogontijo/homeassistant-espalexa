"""Sample API Client."""
import logging
import asyncio
import socket
from typing import Optional
import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class IntegrationBlueprintApiClient:
    def __init__(
        self, host: str, session: aiohttp.ClientSession
    ) -> None:
        """Sample API Client."""
        self._host = host
        self._session = session

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "http://" + self._host + "/api"
        if not hasattr(self, '_username'):
            auth = await self.api_wrapper("post", url, data={"devicetype": "homeassistant"}, headers=HEADERS)
            self._username = auth[0].get('success').get('username')
        if not hasattr(self, '_devices'):
            devices = await self.api_wrapper("get", url + "/" + self._username + "/lights")
            self._devices = devices
        return self

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "http://" + self._host + "/api/" + self._username + "/lights/" + value + "/state"
        await self.api_wrapper("put", url, data={"on": True}, headers=HEADERS)

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    json = await response.json()
 #                   _LOGGER.warn("get " + str(json))
                    return json
                elif method == "put":
                    response = await self._session.put(url, headers=headers, json=data)
                    json = await response.json()
#                    _LOGGER.warn("put " + str(json))
                    return json
                elif method == "patch":
                    response = await self._session.patch(url, headers=headers, json=data)
                    json = await response.json()
#                    _LOGGER.warn("patch " + str(json))
                    return json
                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                    json = await response.json()
#                    _LOGGER.warn("post " + str(json))
                    return json
        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
