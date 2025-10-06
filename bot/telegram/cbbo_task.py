import asyncio
from telegram import Bot, Update
from telegram.ext import ContextTypes
from data.ws import MockGoMarketWS
from engine.cbbo import CbboCalculator

async def live_cbbo_loop(bot: Bot, chat_id: int, symbol: str, message_id: int | None):
    ws = MockGoMarketWS("fake")  # swap later
    calc = CbboCalculator()
    async for snap in ws.subscribe_l1([symbol]):
        cbbo = calc.update(snap)
        if cbbo is None:
            continue
        mid = (cbbo.bid + cbbo.ask) / 2
        text = (f"{cbbo.symbol}\n"
                f"Best bid: {cbbo.bid} ({cbbo.bid_venue})\n"
                f"Best ask: {cbbo.ask} ({cbbo.ask_venue})\n"
                f"Mid: {mid:.2f}")
        if message_id is None:
            msg = await bot.send_message(chat_id=chat_id, text=text)
            message_id = msg.message_id
        else:
            await bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)

async def view_market(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    symbol = ctx.args[0].upper()
    chat_id = update.effective_chat.id
    task = asyncio.create_task(live_cbbo_loop(ctx.bot, chat_id, symbol, None))
    ctx.user_data[f"cbbo_{symbol}"] = task
    await update.message.reply_text(f"Started live CBBO for {symbol}")