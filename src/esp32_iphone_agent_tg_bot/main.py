"""Main entry point for the Telegram bot."""

import asyncio
import logging
import os
import sys
from typing import Any

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from .agent_api import AgentAPIError, AgentClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = {int(x) for x in os.getenv("ALLOWED_USER_IDS", "").split(",") if x}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message."""
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(
        "Hello! Send me a task for your iPhone, e.g.,\n`/task Open Whiteboard and draw a smiley face`",
        parse_mode=ParseMode.MARKDOWN,
    )


async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle task instructions."""
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Unauthorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /task <instruction>")
        return

    instruction = " ".join(context.args)
    client = AgentClient()

    status_message = await update.message.reply_text(f"⏳ Executing: {instruction}")

    try:
        async for step in client.send_task(instruction):
            if screenshot_b64 := step.get("screenshot"):
                import base64

                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=base64.b64decode(screenshot_b64),
                    caption=f"Step: {step.get('description', 'Action executed')}",
                )
            elif status := step.get("status"):
                await status_message.edit_text(f"{status}: {instruction}")

        await status_message.edit_text(f"✅ Task completed: {instruction}")
    except AgentAPIError as e:
        await status_message.edit_text(f"❌ Error: {e}")
    finally:
        await client.close()


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle non-command messages."""
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text("Please use /task <instruction> to send a task.")


def main() -> None:
    """Run the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        sys.exit(1)

    if not ALLOWED_USER_IDS:
        logger.warning("ALLOWED_USER_IDS is not set. The bot will be public!")

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("task", handle_task))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    logger.info("Starting ESP32 iPhone Agent Telegram Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
