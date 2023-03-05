# Telegram Fitness Bot

A simple Telegram bot for tracking your fitness progress using Notion.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [License](#license)

## Installation

1. Clone the repository:

`git clone https://github.com/ibrahimaltay/lifts-logger.git`


2. Install the required Python packages:
`pip install -r requirements.txt`

3. Create a new Telegram bot using BotFather, and obtain your bot token.

4. Create a new Notion integration, and obtain your integration key.

5. Create a new Notion database using the provided template, and share it with your integration.

6. Set the environment variables `TELEGRAM_BOT_TOKEN` and `NOTION_KEY` to your Telegram bot token and Notion integration key, respectively.

7. Run the bot:

`python exercise_bot.py`

## Usage

To use the bot, simply send one of the available commands to your bot:

- `/start`: Introduce the bot and show the available commands.
- `/help`: Show the available commands.
- `/add <exercise> <weight> <reps>`: Add a new exercise to the Notion database.
- `/list`: Show a list of your previous exercises and their data.
- `/history <exercise> [property]`: Show the historical weight and/or reps data for a given exercise.

## Commands

- `/start`: Introduce the bot and show the available commands.
- `/help`: Show the available commands.
- `/add <exercise> <weight> <reps>`: Add a new exercise to the Notion database.
- `/list`: Show a list of your previous exercises and their data.
- `/history <exercise> [property]`: Show the historical weight and/or reps data for a given exercise.

## License

This project is licensed under the [MIT License](LICENSE).

