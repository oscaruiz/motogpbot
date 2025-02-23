from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.error import NetworkError
from services.motogp_service import MotoGPService
from config import MOTOGP_API_URL
from dateutil import parser
import datetime
import asyncio

# Initialize the MotoGP service
motogp_service = MotoGPService(MOTOGP_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await safe_reply(update, "Hello! I am your Telegram bot.")

async def safe_reply(update, message, retries=3, delay=2):
    """Safely send messages with retry logic in case of network errors."""
    for i in range(retries):
        try:
            await update.message.reply_text(message)
            return
        except NetworkError as e:
            print(f"Network error: {e}. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            delay *= 2  # Exponential backoff
    print("Failed to send message after multiple attempts.")

async def get_race_data(update: Update, context: ContextTypes.DEFAULT_TYPE, race_type: str):
    """Fetch race data based on race type (current, next, previous)."""
    race_data = motogp_service.get_races()  # Ensure this is a function call

    if not race_data:
        await safe_reply(update, "Race information is not available at the moment.")
        return

    await safe_reply(update, f"Race type: {race_type}")  # Placeholder message

async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /proxima command to fetch the next MotoGP race."""
    race_data = motogp_service.get_next_races()

    if not race_data or "calendar" not in race_data:
        await safe_reply(update, "Race information is not available at the moment.")
        return

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

    # Find the first upcoming race
    next_race = None
    for race in race_data["calendar"]:
        race_start = parser.parse(race["start_date"])
        if race_start > now:
            next_race = race
            break

    if not next_race:
        await safe_reply(update, "No upcoming races found.")
        return

    # Extract race details
    race_name = next_race["friendly_name"]
    location = f"{next_race['name']} - {next_race['circuit']}"
    dates = next_race["dates"]
    hashtag = next_race.get("hashtag", "N/A")
    country_flag = f":flag_{next_race['country_code'].lower()}:"  # Telegram supports flag emojis

    # Extract key sessions
    sessions_info = []
    for session in next_race.get("key_session_times", []):
        session_name = session["session_name"]
        session_time_utc = parser.parse(session["start_datetime_utc"])
        local_offset = next_race["local_tz_offset"]
        local_time = session_time_utc + datetime.timedelta(hours=local_offset)
        sessions_info.append(f"🏁 {session_name}: {local_time.strftime('%d %b %H:%M')} (Local Time)")

    # Format response message
    message = (
        f"🏍️ *Next MotoGP Race: {race_name}\n"
        f"📍 *Location:* {location}\n"
        f"📅 *Dates:* {dates}\n"
        f"🔹 *Hashtag:* {hashtag}\n"
        f"\n⏳ *Key Sessions:*\n" + "\n".join(sessions_info)
    )

    # Send the formatted message
    await safe_reply(update, message)

async def get_previous_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /anterior command."""
    await get_race_data(update, context, 'past_event')


async def get_driver_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /driver_results command."""
    driver_results_data = motogp_service.get_driver_results()

    if driver_results_data:
        last_race = driver_results_data.get('last_race', 'Unknown race')
        updated_at = driver_results_data.get('updated_at', 'Unknown time')
        formatted_update_time = format_date(updated_at)

        driver_standings = driver_results_data.get('data', [])
        standings_info = "\n".join([
            f"{driver['position']}. {driver['name']} - {driver['points']} points"
            for driver in driver_standings
        ])

        reply_text = f"Driver Standings after {last_race} (updated at {formatted_update_time}):\n\n{standings_info}"
        await safe_reply(update, reply_text)
    else:
        await safe_reply(update, "Driver results information is not available at the moment.")


def format_date(date_str):
    """Format date string to a more readable format with 2 hours added."""
    date_obj = parser.parse(date_str)
    date_obj += datetime.timedelta(hours=2)
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def register_handlers(application):
    """Register command handlers."""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('proxima', get_next_race))
    # application.add_handler(CommandHandler('anterior', get_previous_race))
    application.add_handler(CommandHandler('pilotos', get_driver_results))
