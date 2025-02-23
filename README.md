# MotoGP Telegram Bot

This is a Telegram bot for MotoGP fans, providing real-time information about the latest and upcoming races, driver standings, and more. The bot is built with Python, leveraging the `python-telegram-bot` library and a MotoGP API to fetch race data and results.

## Features

- `/start` - Greets the user and initializes the bot.
- `/proxima` - Shows information about the next upcoming race, including race dates, location, and session times.
- `/anterior` - Displays information about the previous race.
- `/pilotos` - Fetches the current driver standings and updates.
  
## Requirements

- Python 3.12 or higher
- Docker (for deploying via Docker container)
- Access to the MotoGP API for race data

## Troubleshooting

If the bot is not responding:
- Check if the Docker container is running with `docker ps`.
- Ensure your environment variables are correctly set, including the Telegram API token and MotoGP API URL.

Common Docker issues:
- If you face Docker issues, run `docker logs motogp-bot` to see the logs from the container for troubleshooting.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
- [MotoTiming API](https://mototiming.live/)

