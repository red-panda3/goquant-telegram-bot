from pydantic import BaseModel

class L1Snapshot(BaseModel):
    symbol: str
    exchange: str
    bid: float
    ask: float
    ts: int          # milliseconds epoch