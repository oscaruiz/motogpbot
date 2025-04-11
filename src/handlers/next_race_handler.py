from telegram import Update
from telegram.ext import ContextTypes
from src.services.motogp_service import MotoGPService
from src.utils.reply import safe_reply
from src.config import MOTOGP_API_URL
from dateutil import parser
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

motogp_service = MotoGPService(MOTOGP_API_URL)

async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /next command to fetch the next MotoGP race."""
    race_data = motogp_service.get_next_races()

    if not race_data or "calendar" not in race_data:
        await safe_reply(update, "Race information is not available at the moment.")
        return

    now = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Find the first upcoming race
    next_race = None
    for race in race_data["calendar"]:
        race_start = parser.parse(race["start_date"])
        if race_start.date() >= now.date():
            next_race = race
            break

    if not next_race:
        await safe_reply(update, "No upcoming races found.")
        return

    race_name = next_race["friendly_name"]
    location = f"{next_race['name']} - {next_race['circuit']}"
    dates = next_race["dates"]
    hashtag = next_race.get("hashtag", "N/A")

    # Convert key sessions to ES time using zoneinfo
    es_timezone = ZoneInfo("Europe/Madrid")
    sessions_info = []

    for session in next_race.get("key_session_times", []):
        session_name = session["session_name"]
        session_time_utc = parser.parse(session["start_datetime_utc"]).astimezone(timezone.utc)
        local_time = session_time_utc.astimezone(es_timezone)
        sessions_info.append(f"🏁 {session_name}: {local_time.strftime('%d %b %H:%M')} (ES Time)")

    message = (
        f"🏍️ *Next MotoGP Race:* {race_name}\n"
        f"📍 *Location:* {location}\n"
        f"📅 *Dates:* {dates}\n"
        f"🔹 *Hashtag:* {hashtag}\n\n"
        f"⏳ *Key Sessions:*\n" + "\n".join(sessions_info)
    )

    await safe_reply(update, message)
