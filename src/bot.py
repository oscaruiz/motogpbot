import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN
from handlers import register_handlers

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Check if the token is retrieved successfully
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your Telegram bot.')

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    register_handlers(application)

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
