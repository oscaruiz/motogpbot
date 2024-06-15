from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from src.services.motogp_service import MotoGPService
from config import MOTOGP_API_URL

import datetime


# Initialize the MotoGP service
motogp_service = MotoGPService(MOTOGP_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your Telegram bot.')

async def get_current_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /current command."""
    next_race_data = motogp_service.get_races()

    current_event = next_race_data.get('current_event', None)
    
    if not current_event:
        await update.message.reply_text("There is no current event happening at the moment.")
        return

    if next_race_data:
        event_name = next_race_data.get('current_event', {}).get('name', 'No upcoming race name available')
        event_dates = next_race_data.get('current_event', {}).get('dates', 'Dates not available')
        event_circuit = next_race_data.get('current_event', {}).get('circuit', 'Circuit not available')
        event_country = next_race_data.get('current_event', {}).get('country', 'Country not available')
        
        session_times = next_race_data.get('current_event', {}).get('key_session_times', [])
        sessions_info = "\n".join([f"{session['session_shortname']}: {session['session_name']} - {format_date(session['start_datetime_utc'])}" for session in session_times])

        await update.message.reply_text(f"The next MotoGP race is the {event_name}, which will take place at {event_circuit} in {event_country} from {event_dates}.\n\nSession Times:\n{sessions_info}")
    else:
        reply_text = "No upcoming MotoGP race information available."
        await update.message.reply_text(reply_text)
    
async def get_next_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /proxima command."""
    next_race_data = motogp_service.get_races()

    if next_race_data:
        event_name = next_race_data.get('upcoming_event', {}).get('name', 'No upcoming race name available')
        event_dates = next_race_data.get('upcoming_event', {}).get('dates', 'Dates not available')
        event_circuit = next_race_data.get('upcoming_event', {}).get('circuit', 'Circuit not available')
        event_country = next_race_data.get('upcoming_event', {}).get('country', 'Country not available')
        
        session_times = next_race_data.get('upcoming_event', {}).get('key_session_times', [])
        sessions_info = "\n".join([f"{session['session_shortname']}: {session['session_name']} - {format_date(session['start_datetime_utc'])}" for session in session_times])

        await update.message.reply_text(f"The next MotoGP race is the {event_name}, which will take place at {event_circuit} in {event_country} from {event_dates}.\n\nSession Times:\n{sessions_info}")
    else:
        reply_text = "No upcoming MotoGP race information available."
        await update.message.reply_text(reply_text)

async def  get_previous_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /anterior command."""
    previous_race_data = motogp_service.get_races()

    if previous_race_data:
        event_name = previous_race_data.get('past_event', {}).get('name', 'No upcoming race name available')
        event_dates = previous_race_data.get('past_event', {}).get('dates', 'Dates not available')
        event_circuit = previous_race_data.get('past_event', {}).get('circuit', 'Circuit not available')
        event_country = previous_race_data.get('past_event', {}).get('country', 'Country not available')
        
        session_times = previous_race_data.get('past_event', {}).get('key_session_times', [])
        sessions_info = "\n".join([f"{session['session_shortname']}: {session['session_name']} - {format_date(session['start_datetime_utc'])}" for session in session_times])

        await update.message.reply_text(f"The previous MotoGP race was the {event_name}, which took place at {event_circuit} in {event_country} from {event_dates}.")
    else:
        reply_text = "No previous MotoGP race information available."
        await update.message.reply_text(reply_text)

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

def register_handlers(application):
    """Register command handlers."""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('proxima', get_next_race))
    application.add_handler(CommandHandler('anterior', get_previous_race))
    application.add_handler(CommandHandler('pilotos', get_driver_results))

def format_date(date_str):
    """Format date string to a more readable format with 2 hours added."""
    print("ATTENTION!!!!!!!!")
    # Remove 'Z' if it exists
    if date_str.endswith('Z'):
        date_str = date_str[:-1]
    
    # Parse the date string
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    
    # Print the parsed datetime before adding timedelta
    print("Parsed datetime (before adding timedelta):", date_obj)
    
    # Add timedelta of 2 hours
    date_obj += datetime.timedelta(hours=2)
    
    # Print the parsed datetime after adding timedelta
    print("Parsed datetime (after adding timedelta):", date_obj)
    
    # Format the adjusted datetime into a readable format
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_date
