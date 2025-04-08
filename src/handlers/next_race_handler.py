# handlers/next_race_handler.py

import datetime
from dateutil import parser
from telegram import Update
from telegram.ext import ContextTypes
from src.services.motogp_service import MotoGPService
from src.utils.reply import safe_reply

from src.config import MOTOGP_API_URL
motogp_service = MotoGPService(MOTOGP_API_URL)

async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /next command to fetch the next MotoGP race."""
    race_data = motogp_service.get_next_races()

    if not race_data or "calendar" not in race_data:
        await safe_reply(update, "Race information is not available at the moment.")
        return

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    next_race = next(
        (r for r in race_data["calendar"] if parser.parse(r["start_date"]) > now),
        None
    )

    if not next_race:
        await safe_reply(update, "No upcoming races found.")
        return

    race_name = next_race["friendly_name"]
    location = f"{next_race['name']} - {next_race['circuit']}"
    dates = next_race["dates"]
    hashtag = next_race.get("hashtag", "N/A")
    country_flag = f":flag_{next_race['country_code'].lower()}:"  # optional if flags supported

    sessions_info = [
        f"🏁 {s['session_name']}: {(parser.parse(s['start_datetime_utc']) + datetime.timedelta(hours=next_race['local_tz_offset'])).strftime('%d %b %H:%M')} (Local Time)"
        for s in next_race.get("key_session_times", [])
    ]

    message = (
        f"🏍️ *Next MotoGP Race:* {race_name}\n"
        f"📍 *Location:* {location}\n"
        f"📅 *Dates:* {dates}\n"
        f"🔹 *Hashtag:* {hashtag}\n\n"
        f"⏳ *Key Sessions:*\n" + "\n".join(sessions_info)
    )

    await safe_reply(update, message)
