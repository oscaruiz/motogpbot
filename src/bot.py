import logging
from telegram.ext import Application
from src.config import BOT_TOKEN
from src.handlers.command_router import register_handlers


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the MotoGP Telegram bot."""
    if not BOT_TOKEN:
        raise ValueError("No BOT_TOKEN provided in config.py or .env")

    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    register_handlers(application)

    # Start polling
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
