from telegram import Update
from telegram.ext import ContextTypes
from src.services.motogp_service import MotoGPService
from src.utils.reply import safe_reply
from src.config import MOTOGP_API_URL

motogp_service = MotoGPService(MOTOGP_API_URL)

async def get_previous_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /previous command to show last race details."""
    race_data = motogp_service.get_previous_race()
    
    if not race_data or "past_event" not in race_data:
        await safe_reply(update, "No previous race data found.")
        return

    event = race_data["past_event"]
    
    race_name = event.get("friendly_name", "Unknown race")
    location = f"{event.get('name', '')} - {event.get('circuit', '')}"
    dates = event.get("dates", "Unknown dates")
    country_code = event.get("country_code", "unknown")
    country_flag = f":flag_{country_code.lower()}:" if country_code else ""

    # Optional: no 'winner' field found in the data you posted
    # So we leave winner out or simulate it
    message = (
        f"🏁 Last MotoGP Race {race_name}\n"
        f"📍 Location: {location}\n"
        f"📅 Dates: {dates}\n"
    )

    await safe_reply(update, message)
