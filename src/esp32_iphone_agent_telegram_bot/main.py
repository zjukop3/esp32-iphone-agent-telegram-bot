"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from .agent_client import AgentClient

# Load environment variables
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

agent_client = AgentClient(base_url=AGENT_API_URL)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! Send me a task for the iPhone.\n"
        "Usage: `/open <app_name> and <action>`\n"
        "Example: `/open Whiteboard and draw a smiley face`",
        parse_mode="Markdown"
    )


async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming task messages."""
    if not context.args:
        await update.message.reply_text("Please provide a task description.")
        return

    task_description = " ".join(context.args)
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    logger.info(f"Received task from {user_id}: {task_description}")
    await update.message.reply_text(f"⏳ Task received: \"{task_description}\"\nDispatching to ESP32 iPhone Agent...")

    # Add task to the queue and process asynchronously
    asyncio.create_task(process_task(chat_id, task_description, context))


async def process_task(chat_id: int, task_description: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the task asynchronously."""
    try:
        await context.bot.send_message(chat_id=chat_id, text="🤖 Agent is working on it...")
        
        # Call the agent API
        result = await agent_client.run_task(task_description)
        
        if result.get("status") == "success":
            screenshot_url = result.get("screenshot_url")
            if screenshot_url:
                await context.bot.send_message(chat_id=chat_id, text="✅ Task completed successfully!")
                # In a real scenario, you'd download the image and send it
                await context.bot.send_photo(chat_id=chat_id, photo=screenshot_url)
            else:
                await context.bot.send_message(chat_id=chat_id, text="✅ Task completed, but no screenshot available.")
        else:
            error_msg = result.get("error", "Unknown error")
            await context.bot.send_message(chat_id=chat_id, text=f"❌ Task failed: {error_msg}")
    except Exception as e:
        logger.error(f"Error processing task: {e}")
        await context.bot.send_message(chat_id=chat_id, text=f"❌ An error occurred: {str(e)}")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open", handle_task))

    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
