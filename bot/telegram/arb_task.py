import asyncio
from telegram import Bot, Update
from telegram.ext import ContextTypes
from data.ws import MockGoMarketWS
from engine.arb import SpreadCalculator
from data.models import L1Snapshot

async def arb_loop(bot: Bot, chat_id: int, symbol: str, threshold: float, msg_id: int | None):
    ws = MockGoMarketWS("fake")
    calc = SpreadCalculator()
    snapshots: dict[str, L1Snapshot] = {}
    async for snap in ws.subscribe_l1([symbol]):
        snapshots[snap.exchange] = snap
        if len(snapshots) < 2:
            continue
        # pick any two exchanges
        a, b = list(snapshots.values())[:2]
        sig = calc.check(a, b, threshold)
        if sig is None:
            continue
        text = (f"🔔 {symbol} arb: {sig.spread_pct:.2f} %\n"
                f"Buy  {sig.buy_venue}  {sig.buy_price}\n"
                f"Sell {sig.sell_venue}  {sig.sell_price}")
        if msg_id is None:
            msg = await bot.send_message(chat_id=chat_id, text=text)
            msg_id = msg.message_id
        else:
            await bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id)

async def monitor_arb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if len(ctx.args) < 2:
        await update.message.reply_text("Usage: /monitor_arb <symbol> <threshold>%")
        return
    sym = ctx.args[0].upper()
    try:
        thr = float(ctx.args[1].rstrip("%"))
    except ValueError:
        await update.message.reply_text("Threshold must be a number (e.g. 0.3%)")
        return
    chat_id = update.effective_chat.id
    task = asyncio.create_task(arb_loop(ctx.bot, chat_id, sym, thr, None))
    ctx.user_data[f"arb_{sym}"] = task
    await update.message.reply_text(f"Monitoring {sym} arb ≥ {thr} %")