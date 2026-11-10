"""Find recipe links in a message and extract their ingredients."""
import logging
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from receiptor.config import ALLOWED_HOSTS, MAX_REDIRECTS, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


def is_allowed_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and (parsed.hostname or "").lower() in ALLOWED_HOSTS


def find_recipe_urls(text):
    return [url for url in URL_PATTERN.findall(text or "") if is_allowed_url(url)]


def fetch(url):
    """GET url, following redirects only while they stay on an allowed host."""
    for _ in range(MAX_REDIRECTS + 1):
        response = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        if not response.is_redirect:
            response.raise_for_status()
            return response.text
        url = urljoin(url, response.headers["Location"])
        if not is_allowed_url(url):
            raise ValueError("redirect to a host that isn't allowed: {}".format(url))
    raise ValueError("too many redirects")


def parse_ingredients(html):
    """Return a list of "amount name" strings from a recipe page."""
    ingredients = []
    for li in BeautifulSoup(html, "html.parser").find_all("li"):
        name = li.find("span", {"property": "v:name"})
        amount = li.find("span", {"property": "v:amount"})
        if name and amount:
            ingredients.append(" ".join(part for part in (amount.get_text(strip=True),
                                                          name.get_text(strip=True)) if part))
    return ingredients


def split_message(lines, max_length):
    """Join lines into as few messages as possible, each up to max_length characters."""
    messages, current = [], ""
    for line in lines:
        line = line[:max_length]
        if current and len(current) + 1 + len(line) > max_length:
            messages.append(current)
            current = line
        else:
            current = current + "\n" + line if current else line
    if current:
        messages.append(current)
    return messages
