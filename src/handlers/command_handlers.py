from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from services.motogp_service import MotoGPService
from config import MOTOGP_API_URL
from dateutil import parser
import datetime

# Initialize the MotoGP service
motogp_service = MotoGPService(MOTOGP_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your Telegram bot.')

async def get_race_data(update: Update, context: ContextTypes.DEFAULT_TYPE, race_type: str):
    """Fetch race data based on race type (current, next, previous)."""
    race_data = motogp_service.get_races()

    if not race_data:
        await update.message.reply_text("Race information is not available at the moment.")
        return

    race_info = race_data.get(race_type, None)
    
    if race_info:
        event_name = race_info.get('name', 'Race name not available')
        event_dates = race_info.get('dates', 'Dates not available')
        event_circuit = race_info.get('circuit', 'Circuit not available')
        event_country = race_info.get('country', 'Country not available')
        
        session_times = race_info.get('key_session_times', [])
        sessions_info = "\n".join([f"{session['session_shortname']}: {session['session_name']} - {format_date(session['start_datetime_utc'])}" for session in session_times])

        message = format_race_message(event_name, event_dates, event_circuit, event_country, sessions_info)
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("No race information available.")

async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /proxima command."""
    race_data = motogp_service.get_races()

    current_event = race_data.get('current_event', None)
    
    if current_event:
        await get_race_data(update, context, 'current_event')
    else:
        await get_race_data(update, context, 'upcoming_event')

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
            f"{driver['position']}. {driver['name']} - {driver['points']} points (Prev: {driver['prev_position']}, Deficit: {driver['deficit_percentage']}%)"
            for driver in driver_standings
        ])

        reply_text = (
            f"Driver Standings after {last_race} (updated at {formatted_update_time}):\n\n{standings_info}"
        )
        await update.message.reply_text(reply_text)
    else:
        await update.message.reply_text("Driver results information is not available at the moment.")

def format_race_message(event_name, event_dates, event_circuit, event_country, sessions_info):
    """Format the race information into a readable message."""
    return (f"The {event_name} is taking place at {event_circuit} in {event_country} from {event_dates}.\n\n"
            f"Session Times:\n{sessions_info}")

def register_handlers(application):
    """Register command handlers."""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('proxima', get_next_race))
    application.add_handler(CommandHandler('anterior', get_previous_race))
    application.add_handler(CommandHandler('pilotos', get_driver_results))

def format_date(date_str):
    """Format date string to a more readable format with 2 hours added."""
    # Parse the date string with dateutil.parser
    date_obj = parser.parse(date_str)
    
    # Add timedelta of 2 hours
    date_obj += datetime.timedelta(hours=2)
    
    # Format the adjusted datetime into a readable format
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_date
    """Format date string to a more readable format with 2 hours added."""
    # Parse the date string with dateutil.parser
    date_obj = parser.parse(date_str)
    
    # Add timedelta of 2 hours
    date_obj += datetime.timedelta(hours=2)
    
    # Format the adjusted datetime into a readable format
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_date