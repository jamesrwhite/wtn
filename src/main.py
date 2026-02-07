import argparse
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


def generate_mermaid_chart(ratings_data):
    """Generate a Mermaid xyChart from ratings data."""
    # Skip header row
    data = ratings_data[1:]
    
    # Limit to last 20 data points for readability
    data = data[-20:]
    
    # Format dates (convert DD/MM/YYYY to shorter format)
    dates = []
    singles = []
    doubles = []
    
    for row in data:
        date_str, single, double = row
        # Convert to short format (DD/MM)
        date_parts = date_str.split('/')
        short_date = f"{date_parts[0]}/{date_parts[1]}"
        dates.append(short_date)
        singles.append(single)
        doubles.append(double)
    
    # Build Mermaid chart
    chart = ["```mermaid"]
    chart.append("---")
    chart.append("config:")
    chart.append("  xyChart:")
    chart.append("    width: 900")
    chart.append("    height: 400")
    chart.append("---")
    chart.append("xychart-beta")
    chart.append('  title "WTN Ratings Progress"')
    chart.append(f'  x-axis [{', '.join([f"\"{d}\"" for d in dates])}]')
    chart.append('  y-axis "Rating" 25 --> 32')
    chart.append(f'  line [{', '.join(singles)}]')
    chart.append(f'  line [{', '.join(doubles)}]')
    chart.append("```")
    
    return '\n'.join(chart)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Fetch and track WTN ratings')
    parser.add_argument('--force', action='store_true', 
                        help='Force regeneration of README even if ratings haven\'t changed')
    args = parser.parse_args()
    
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
        ratings_changed = singles != previous_singles or doubles != previous_doubles
        
        if ratings_changed:
            today = datetime.fromtimestamp(time()).strftime('%d/%m/%Y')
            updated = [today, singles, doubles]
            log.info('Ratings have changed, updating date file: %s', updated)
            
            update = csv.writer(open(DATA_FILE, 'a'))
            update.writerow(updated)
        
        # Update README if ratings changed or force flag is set
        if ratings_changed or args.force:
            if args.force and not ratings_changed:
                log.info('Force flag set, regenerating README')
            
            log.info('Updating %s template', README_TEMPLATE)
            
            # Generate Mermaid chart
            all_ratings = list(csv.reader(open(DATA_FILE, 'r')))
            mermaid_chart = generate_mermaid_chart(all_ratings)
            
            template = Environment(loader=FileSystemLoader('.')).get_template(README_TEMPLATE)
            readme = template.render(singles=singles, doubles=doubles, chart=mermaid_chart)
            open(README, 'w').write(readme)
