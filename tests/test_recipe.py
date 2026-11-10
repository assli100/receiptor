import asyncio
import unittest
from unittest import mock

from receiptor import recipe
from receiptor.bot import Bot

PAGE = """
<ul>
  <li><span property="v:amount">2 cups</span> <span property="v:name">flour</span></li>
  <li><span property="v:amount"></span><span property="v:name">salt</span></li>
  <li>no ingredient here</li>
</ul>
"""


def fake_response(status=200, text="", location=None):
    res = mock.Mock(status_code=status, text=text, is_redirect=location is not None,
                    headers={"Location": location} if location else {})
    res.raise_for_status.return_value = None
    return res


class RecipeTest(unittest.TestCase):
    def test_find_urls_only_on_allowed_host(self):
        text = ("look http://www.foodsdictionary.co.il/Recipes/1 and "
                "https://foodsdictionary.co.il/r/2 "
                "http://evil.com/?x=http://www.foodsdictionary.co.il "
                "http://www.foodsdictionary.co.il.evil.com/x "
                "http://evil.com@127.0.0.1/")
        self.assertEqual(recipe.find_recipe_urls(text),
                         ["http://www.foodsdictionary.co.il/Recipes/1", "https://foodsdictionary.co.il/r/2"])

    def test_parse_ingredients(self):
        self.assertEqual(recipe.parse_ingredients(PAGE), ["2 cups flour", "salt"])

    def test_split_message(self):
        self.assertEqual(recipe.split_message(["aaa", "bbb", "cc"], 7), ["aaa\nbbb", "cc"])
        self.assertEqual(recipe.split_message(["x" * 10], 4), ["xxxx"])

    @mock.patch("receiptor.recipe.requests.get")
    def test_fetch_follows_allowed_redirect(self, get):
        get.side_effect = [fake_response(301, location="https://www.foodsdictionary.co.il/r/1"),
                           fake_response(text="ok")]
        self.assertEqual(recipe.fetch("http://www.foodsdictionary.co.il/r/1"), "ok")

    @mock.patch("receiptor.recipe.requests.get")
    def test_fetch_refuses_redirect_elsewhere(self, get):
        get.return_value = fake_response(302, location="http://169.254.169.254/")
        with self.assertRaises(ValueError):
            recipe.fetch("http://www.foodsdictionary.co.il/r/1")
        self.assertEqual(get.call_count, 1)


class BotTest(unittest.TestCase):
    @mock.patch("receiptor.bot.fetch", return_value=PAGE)
    def test_handle_message_sends_one_message(self, fetch):
        message = mock.Mock(text="http://www.foodsdictionary.co.il/Recipes/1")
        message.reply_text = mock.AsyncMock()
        asyncio.run(Bot.handle_message(mock.Mock(message=message), None))
        message.reply_text.assert_awaited_once_with("2 cups flour\nsalt")

    @mock.patch("receiptor.bot.fetch")
    def test_ignores_other_links(self, fetch):
        message = mock.Mock(text="http://evil.com/?u=http://www.foodsdictionary.co.il")
        message.reply_text = mock.AsyncMock()
        asyncio.run(Bot.handle_message(mock.Mock(message=message), None))
        fetch.assert_not_called()
        message.reply_text.assert_not_awaited()

    def test_bot_builds(self):
        Bot("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


if __name__ == "__main__":
    unittest.main()
