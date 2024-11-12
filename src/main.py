import csv
import logging
from datetime import datetime
from os import environ
from time import time

from jinja2 import Environment, FileSystemLoader

from constants import DATA_FILE, PROFILE_URL, README, README_TEMPLATE
from data import fetch

log = logging.getLogger(__name__)
logging.basicConfig(level=environ.get('LOG_LEVEL', 'INFO'))


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

            log.info('Updating %s template', README_TEMPLATE)
            template = Environment(loader=FileSystemLoader('.')).get_template(README_TEMPLATE)
            readme = template.render(singles=singles, doubles=doubles)
            open(README, 'w').write(readme)
