# receiptorBot

A Telegram bot that reads recipes. Send it a link to a recipe on
[foodsdictionary.co.il](http://www.foodsdictionary.co.il) and it replies with the list of ingredients.

## Install
```bash
pip install .
```

## Run
Create a bot with [@BotFather](https://t.me/BotFather), then pass its token with
`TELEGRAM_TOKEN` or put it in a `token.txt` file in the current directory:
```bash
TELEGRAM_TOKEN=<your token> receiptor
```

## Tests
```bash
python -m unittest discover -s tests
```
