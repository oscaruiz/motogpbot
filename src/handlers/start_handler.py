from telegram import Update
from telegram.ext import ContextTypes
from src.utils.reply import safe_reply


async def get_start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    message = (
        "🏁 *Welcome to the MotoGP Bot!*\n\n"
        "Use the following commands to explore:\n"
        "• /next - Get the next MotoGP race\n"
        "• /previous - Show the latest race results\n"
        "• /standings - View current rider standings\n"
    )
    await safe_reply(update, message)
