# utils/reply.py

from telegram import Update
import logging

logger = logging.getLogger(__name__)

async def safe_reply(update: Update, text: str, parse_mode: str = "Markdown"):
    """
    Sends a reply safely, catching exceptions (e.g., message deleted or invalid chat).
    """
    try:
        await update.message.reply_text(text, parse_mode=parse_mode)
    except Exception as e:
        logger.warning(f"Failed to send message: {e}")
