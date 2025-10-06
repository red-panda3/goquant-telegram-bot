import asyncio, json, websockets
from typing import AsyncIterator
from .models import L1Snapshot
import random, time

class GoMarketWS:
    def __init__(self, api_key: str, url: str = "wss://gomarket-stream.goquant.io/ws/v1"):
        self.url = url
        self.key = api_key

    async def subscribe_l1(self, symbols: list[str]) -> AsyncIterator[L1Snapshot]:
        async with websockets.connect(self.url, extra_headers={"x-api-key": self.key}) as ws:
            sub = {"op": "subscribe", "topic": "l1", "symbols": symbols}
            await ws.send(json.dumps(sub))
            async for msg in ws:
                data = json.loads(msg)
                yield L1Snapshot(**data)

class MockGoMarketWS(GoMarketWS):
    async def subscribe_l1(self, symbols: list[str]) -> AsyncIterator[L1Snapshot]:
        while True:
            for sym in symbols:
                mid = 30000 if "BTC" in sym else 2000
                spread = mid * 0.001
                yield L1Snapshot(
                    symbol=sym,
                    exchange=random.choice(["binance", "okx", "bybit", "deribit"]),
                    bid=round(mid - spread/2, 2),
                    ask=round(mid + spread/2, 2),
                    ts=int(time.time()*1000)
                )
            await asyncio.sleep(1)                