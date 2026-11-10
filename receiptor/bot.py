import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from receiptor.config import MAX_MESSAGE_LENGTH
from receiptor.recipe import fetch, find_recipe_urls, parse_ingredients, split_message

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_error_handler(self.error)

    def run(self):
        self.application.run_polling()

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello there! Send me a link to a recipe on foodsdictionary.co.il "
                                        "and I'll send you its ingredients.")

    @staticmethod
    async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error('Update "%s" caused an error', update, exc_info=context.error)

    @staticmethod
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message
        if not message:
            return
        for url in find_recipe_urls(message.text):
            try:
                # requests is blocking, so run it off the event loop
                html = await asyncio.to_thread(fetch, url)
                ingredients = parse_ingredients(html)
            except Exception:
                logger.exception("Failed to read recipe %s", url)
                await message.reply_text("Sorry, I couldn't read that recipe.")
                continue

            if not ingredients:
                await message.reply_text("I didn't find any ingredients on that page.")
                continue
            for text in split_message(ingredients, MAX_MESSAGE_LENGTH):
                await message.reply_text(text)
