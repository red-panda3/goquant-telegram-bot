from tinydb import TinyDB, Query
from pathlib import Path

Path("data").mkdir(exist_ok=True)
db = TinyDB("data/userdb.json")
User = Query()

def save_monitor(chat_id: int, typ: str, symbol: str, threshold: float):
    db.upsert({"chat_id": chat_id, "type": typ, "symbol": symbol, "threshold": threshold},
              User.chat_id == chat_id and User.symbol == symbol)

def load_monitors():
    return db.all()