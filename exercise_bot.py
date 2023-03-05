import telegram
import os

from telegram.ext import Updater, CommandHandler
from notion_handlers.get_latest_data import get_latest_data
from notion_handlers.add_exercise import add_exercise
from notion_handlers.get_exercise_history import get_exercise_history


# Set up the Telegram bot
bot = telegram.Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
updater = Updater(token=os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def list_command_handler(update, context):
    # Get the latest exercise data from the Notion database
    exercise_data = get_latest_data()

    # If there are no previous exercises, inform the user and return
    if not exercise_data:
        update.message.reply_text("No previous exercises found.")
        return

    # Format the exercise data for display
    message = "Your previous exercises are:\n\n"
    for entry, (weight, reps) in exercise_data.items():
        message += f"{entry.capitalize()}: {weight}kg, {reps} reps\n"

    # Send the exercise data to the user
    update.message.reply_text(message)


list_handler = CommandHandler("list", list_command_handler)
dispatcher.add_handler(list_handler)

def start_command_handler(update, context):
    # Send a welcome message to the user
    message = "Hello! Welcome to the exercise bot. To save an exercise, use the /save command followed by the exercise name, weight, and reps. For example: /save squat 20 50"
    update.message.reply_text(message)


# Set up a CommandHandler for the "/start" command
start_handler = CommandHandler("start", start_command_handler)
dispatcher.add_handler(start_handler)


# Define a function to handle the "/save" command
def save_command_handler(update, context):
    # Get the exercise data from the user's message
    command = update.message.text.split()
    name = command[1]
    weight = int(command[2])
    reps = int(command[3])

    # Call the add_exercise function to save the exercise data
    add_exercise(name.capitalize(), weight, reps)

    # Send a message to the user to confirm that the exercise was saved
    message = f"Saved {name.capitalize()} with {weight} kilograms and {reps} reps."
    update.message.reply_text(message)


# Set up a CommandHandler for the "/save" command
save_handler = CommandHandler("save", save_command_handler)
dispatcher.add_handler(save_handler)


def history_command_handler(update, context):
    # Get the exercise name and property name from the command arguments
    args = context.args
    if not args:
        update.message.reply_text("Please specify an exercise name")
        return
    exercise_name = args[0].lower()
    property_name = args[1].lower() if len(args) > 1 else None

    # Map alternative property names to the standard names used in Notion
    property_name_map = {
        "rep": "reps",
        "repetition": "reps",
        "reps": "reps",
        "weights": "weight",
        "kg": "weight",
        "kgs": "weight",
        "w": "weight",
        "weight": "weight",
    }
    property_name = property_name_map.get(property_name, property_name)

    # Get the exercise history from the Notion database
    history = get_exercise_history(exercise_name, property_name)

    # Format the exercise history for display
    if isinstance(history, str):
        # Handle error messages
        message = history
    elif not history:
        # Handle empty history
        message = f"No history found for {exercise_name.capitalize()}"
    elif isinstance(history[0], tuple):
        # Handle history with both weight and reps data
        message = f"{exercise_name.capitalize()} history:\n\n"
        for i, data in enumerate(history):
            weight, reps = data
            message += f"{i+1}. {weight}kg, {reps} reps\n"
    else:
        # Handle history with only one property
        message = f"{exercise_name.capitalize()} {property_name.capitalize()} history:\n\n"
        for i, value in enumerate(history):
            message += f"{i+1}. {value}\n"

    # Send the exercise history to the user
    update.message.reply_text(message)


history_handler = CommandHandler("history", history_command_handler)
dispatcher.add_handler(history_handler)

# Start the bot
updater.start_polling()
updater.idle()
