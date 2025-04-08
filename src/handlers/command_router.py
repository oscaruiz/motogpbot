from telegram.ext import CommandHandler
from src.handlers.start_handler import get_start_message
from src.handlers.next_race_handler import get_next_race
from src.handlers.previous_race_handler import get_previous_race
from src.handlers.standings_handler import get_rider_standings

def register_handlers(app):
    # English
    app.add_handler(CommandHandler("start", get_start_message))
    app.add_handler(CommandHandler("next", get_next_race))
    app.add_handler(CommandHandler("previous", get_previous_race))
    app.add_handler(CommandHandler("standings", get_rider_standings))

    # Español (alias)
    app.add_handler(CommandHandler("proxima", get_next_race))
    app.add_handler(CommandHandler("anterior", get_previous_race))
    app.add_handler(CommandHandler("pilotos", get_rider_standings))
