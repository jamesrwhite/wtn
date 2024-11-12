import httpx
from parsel import Selector

from constants import PROFILE_URL


def fetch(url):
    # Fetch the profile page (including cookie to bypass cookie banner)
    response = httpx.get(
        url=PROFILE_URL,
        cookies={'st': 'l=2057&exp=45847.799465463&c=1&cp=1'},
    )

    # Extract the ratings from the page
    html = Selector(text=response.text)
    elements = html.css('.tag-duo__value::text').getall()
    [singles, doubles] = [r.strip() for r in elements if r.strip() != '']

    return (singles, doubles)