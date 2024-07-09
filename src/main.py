import csv
import logging
from datetime import datetime
from decimal import Decimal
from os import environ
from time import time

import httpx
from parsel import Selector

PROFILE_URL = 'https://competitions.lta.org.uk/player-profile/d6a6f490-b524-4ddd-bd28-31d6559ff120'
DATA_FILE = 'data/ratings.csv'

log = logging.getLogger(__name__)
logging.basicConfig(level=environ.get('LOG_LEVEL', 'INFO'))

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

if __name__ == '__main__':
    # Fetch the latest ratings
    [singles, doubles] = fetch(PROFILE_URL)
    log.info('Latest singles rating: %s', singles)
    log.info('Latest doubles rating: %s', doubles)

    # Fetch the previous ratings
    previous = list(csv.reader(open(DATA_FILE, 'r')))
    log.info('Previous ratings available: %d', len(previous)-1)

    if len(previous) > 1:
        [date, previous_singles, previous_doubles] = previous[-1]
        log.info('Previous singles rating: %s', previous_singles)
        log.info('Previous doubles rating: %s', previous_doubles)

        # Write back the new ratings if they have changed
        if singles != previous_singles or doubles != previous_doubles:
            today = datetime.fromtimestamp(time()).strftime('%d/%m/%Y')
            updated = [today, singles, doubles]
            log.info('Ratings have changed, updating date file: %s', updated)
            
            update = csv.writer(open(DATA_FILE, 'a'))
            update.writerow(updated)
