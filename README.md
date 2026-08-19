# 🎾 WTN

Tracking my singles and doubles [WTN](https://worldtennisnumber.com) (World Tennis Number) over time by scraping my [LTA profile](https://competitions.lta.org.uk/player-profile/d6a6f490-b524-4ddd-bd28-31d6559ff120).

## Current

* **Singles**: 25.9
* **Doubles**: 23.8

## Progress

```mermaid
---
config:
  xyChart:
    width: 900
    height: 400
---
xychart-beta
  title "WTN Ratings Progress"
  x-axis ["22/08", "12/09", "19/09", "22/05", "28/05", "11/06", "06/11", "04/12", "11/12", "08/01", "29/01", "07/02", "10/03", "25/03", "29/04", "27/05", "08/07", "15/07", "22/07", "12/08"]
  y-axis "Rating" 25 --> 32
  line [29.0, 27.9, 27.5, 27.4, 27.4, 26.8, 26.8, 26.8, 26.9, 26.9, 26.9, 26.9, 26.8, 26.8, 26.8, 26.8, 26.8, 26.8, 26.5, 25.9]
  line [30.3, 29.3, 29.3, 29.3, 30.0, 30.0, 29.5, 29.6, 29.5, 29.3, 29.4, 28.7, 29.0, 28.7, 28.5, 28.0, 28.2, 27.9, 27.9, 24.3]
```

## History

Available in: [data/ratings.csv](data/ratings.csv)

## Development

### Setup

Install [Poetry](https://python-poetry.org/) for managing Python dependencies.

    make setup && make install

### Running

Run script to fetch ratings and write them to [data/ratings.csv](data/ratings.csv) if they have changed.

    make run