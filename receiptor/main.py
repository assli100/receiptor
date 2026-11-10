import os
import sys

from receiptor import bot


def read_token():
    """Read the bot token from $TELEGRAM_TOKEN, or from token.txt."""
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        try:
            with open("token.txt", "r") as f:
                token = f.read()
        except FileNotFoundError:
            pass
    token = (token or "").strip()
    if not token:
        sys.exit("No bot token: set TELEGRAM_TOKEN or put the token in token.txt")
    return token


def main():
    receiptor_bot = bot.Bot(read_token())
    receiptor_bot.run()


if __name__ == '__main__':
    main()
