# prompt: create an ai chat bot for telegram with nsfw blocking

# Install necessary libraries
!pip install python-telegram-bot
!pip install transformers

# Import libraries
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Replace with your Telegram bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Initialize the AI chatbot pipeline
classifier = pipeline("text-classification", model="facebook/bart-large-mnli")

def start(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /start is issued."""
  update.message.reply_text('Hi! I am your AI chatbot. Ask me anything!')

def echo(update: Update, context: CallbackContext) -> None:
  """Echo the user message and check for NSFW content."""
  user_message = update.message.text

  # Classify the message using the NSFW classifier
  result = classifier(user_message)
  if result[0]['label'] == 'LABEL_1' and result[0]['score'] > 0.8:
    update.message.reply_text("Sorry, I cannot respond to NSFW content.")
  else:
    # Replace with your preferred AI chatbot logic (e.g., using a language model)
    # Here's a simple example:
    update.message.reply_text(f"You said: {user_message}")


def main() -> None:
  """Start the bot."""
  updater = Updater(BOT_TOKEN)

  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
