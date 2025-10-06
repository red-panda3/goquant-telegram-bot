import pytest
from data.ws import MockGoMarketWS   # <-- use the WebSocket mock, not REST

@pytest.mark.asyncio
async def test_mock_ws():
    ws = MockGoMarketWS("fake-key")   # constructor expects api_key
    count = 0
    async for snap in ws.subscribe_l1(["BTC-USDT"]):
        assert snap.bid > 0
        assert snap.ask > snap.bid
        count += 1
        if count == 3:
            break