from dataclasses import dataclass, field
from data.models import L1Snapshot

@dataclass
class Cbbo:
    symbol: str
    bid: float
    bid_venue: str
    ask: float
    ask_venue: str
    mid: float = field(init=False)
    def __post_init__(self):
        self.mid = round((self.bid + self.ask)/2, 2)

class CbboCalculator:
    def __init__(self):
        self.books: dict[str, dict[str, L1Snapshot]] = {}  # symbol -> exchange -> snap

    def update(self, snap: L1Snapshot) -> Cbbo | None:
        self.books.setdefault(snap.symbol, {})[snap.exchange] = snap
        if len(self.books[snap.symbol]) < 2:
            return None
        bids = [(ex, s.bid) for ex, s in self.books[snap.symbol].items()]
        asks = [(ex, s.ask) for ex, s in self.books[snap.symbol].items()]
        best_bid, best_bid_px = max(bids, key=lambda x: x[1])
        best_ask, best_ask_px = min(asks, key=lambda x: x[1])
        return Cbbo(symbol=snap.symbol, bid=best_bid_px, bid_venue=best_bid,
                    ask=best_ask_px, ask_venue=best_ask)