from dataclasses import dataclass
from data.models import L1Snapshot

@dataclass
class ArbSignal:
    buy_venue: str
    buy_price: float
    sell_venue: str
    sell_price: float
    spread_pct: float
    symbol: str

class SpreadCalculator:
    def check(self, a: L1Snapshot, b: L1Snapshot, threshold_pct: float) -> ArbSignal | None:
        # avoid zero-division
        if b.ask <= 0 or a.ask <= 0:
            return None

        # leg 1: buy on B, sell on A
        if a.bid > b.ask * (1 + threshold_pct / 100):
            spread = (a.bid - b.ask) / b.ask * 100
            return ArbSignal(
                buy_venue=b.exchange, buy_price=b.ask,
                sell_venue=a.exchange, sell_price=a.bid,
                spread_pct=round(spread, 3),
                symbol=a.symbol,
            )

        # leg 2: buy on A, sell on B
        if b.bid > a.ask * (1 + threshold_pct / 100):
            spread = (b.bid - a.ask) / a.ask * 100
            return ArbSignal(
                buy_venue=a.exchange, buy_price=a.ask,
                sell_venue=b.exchange, sell_price=b.bid,
                spread_pct=round(spread, 3),
                symbol=a.symbol,
            )

        return None