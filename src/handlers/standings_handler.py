# src/handlers/standings_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from src.services.motogp_service import MotoGPService
from src.utils.reply import safe_reply
from src.config import MOTOGP_API_URL
from datetime import datetime

motogp_service = MotoGPService(MOTOGP_API_URL)

def format_date(date_str):
    """Formats ISO datetime into a more readable string."""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y %H:%M UTC")
    except Exception:
        return "Unknown time"

async def get_rider_standings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /standings command to show current rider rankings."""
    standings_data = motogp_service.get_rider_standings()

    if standings_data:
        last_race = standings_data.get('last_race', 'Unknown race')
        updated_at = standings_data.get('updated_at', 'Unknown time')
        formatted_update_time = format_date(updated_at)

        riders = standings_data.get('data', [])
        standings_info = "\n".join([
            f"{rider['position']}. {rider['name']} - {rider['points']} points"
            for rider in riders
        ])

        message = (
            f"🏆 *Rider Standings after {last_race}* _(updated at {formatted_update_time})_\n\n"
            f"{standings_info}"
        )

        await safe_reply(update, message)
    else:
        await safe_reply(update, "Rider standings are not available at the moment.")
