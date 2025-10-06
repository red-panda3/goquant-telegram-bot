from engine.cbbo import CbboCalculator
from data.models import L1Snapshot
import time

def test_cbbo():
    now = int(time.time() * 1000)
    calc = CbboCalculator()
    
    assert calc.update(L1Snapshot(symbol="BTC-USDT", exchange="okx", bid=50_000, ask=50_010, ts=now)) is None

    cbbo = calc.update(L1Snapshot(symbol="BTC-USDT", exchange="binance", bid=50_005, ask=50_008, ts=now))
    assert cbbo is not None
    assert cbbo.bid == 50_005
    assert cbbo.ask == 50_008
    assert cbbo.bid_venue == "binance"
    assert cbbo.ask_venue == "binance"