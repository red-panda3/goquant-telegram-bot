import aiohttp
from typing import List


class GoMarketREST:
    def __init__(self, api_key: str, base_url: str = "https://gomarket-api.goquant.io"):
        self.base = base_url.rstrip("/")      # guard against trailing slash
        self.key = api_key
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={"x-api-key": self.key})
        return self

    async def __aexit__(self, *_):
        if self.session:
            await self.session.close()

    async def list_symbols(self, exchange: str, kind: str = "spot") -> List[str]:
        url = f"{self.base}/api/symbols/{exchange}/{kind}"
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return [s["symbol"] for s in data]


class MockGoMarketREST(GoMarketREST):
    async def list_symbols(self, exch: str, kind: str = "spot") -> List[str]:
        # Keep same signature; ignore exch/kind for brevity
        return ["BTC-USDT", "ETH-USDT", "SOL-USDT"]