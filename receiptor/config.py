import logging

# hosts the bot is allowed to fetch recipes from
ALLOWED_HOSTS = {"foodsdictionary.co.il", "www.foodsdictionary.co.il"}

REQUEST_TIMEOUT = 15  # seconds
MAX_REDIRECTS = 5
# Telegram rejects messages longer than 4096 characters
MAX_MESSAGE_LENGTH = 4096

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# don't log every polling request (the URL contains the bot token)
logging.getLogger("httpx").setLevel(logging.WARNING)
