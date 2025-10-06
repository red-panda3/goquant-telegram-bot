import asyncio, logging
from bot.telegram.app import build_application

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

async def main() -> None:
    app = build_application()
    await app.initialize()          # 1. init
    await app.start()               # 2. start job-queue
    await app.updater.start_polling()  # 3. start polling
    try:
        await asyncio.Event().wait()   # 4. sleep forever
    finally:
        await app.updater.stop()      # 5. graceful stop
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())