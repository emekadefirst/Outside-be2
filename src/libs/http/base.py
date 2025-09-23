import httpx
import orjson
from typing import Dict, Optional, Any


class APIService:
    def __init__(self, url: str, header: Optional[Dict] = None, body: Optional[Dict] = None):
        self.url = url
        self.header = header
        self.body = body

    async def get(self) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url, headers=self.header, params=self.body)
            return self._handle_response(response)

    async def post(self) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                headers=self.header,
                content=orjson.dumps(self.body) if self.body else None,
            )
            return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Any:
        try:
            return response.json()
        except Exception:
            return response.text
