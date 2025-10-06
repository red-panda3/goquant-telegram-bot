from telegram.ext import Application, CommandHandler
from bot.settings import settings
from .handlers import start, list_symbols,monitor_arb   # ← import new handler
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

def build_application() -> Application:
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list_symbols", list_symbols))
    app.add_handler(CommandHandler("monitor_arb", monitor_arb))  # ← new command
    return app