# small project

## Features

- Search for the best trip combinations based on origin, budget, and number of nights.
- Displays detailed trip information including hotel and flight details.
- ranking search results based on factors:
  - Rating (DESC)
  - Star of the hotel (DESC)
  - price (ASC)
  - total number of stops for the round trip flight
- Utilizes an LRU cache to store and retrieve previously computed results for faster response times.
- Simple and intuitive user interface.
- random data generation scripts

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: JSON files for flights and hotels
- **Caching**: LRU (Least Recently Used) Cache implemented in Python

## Setup
### Prerequisites

- Python 3.10
- Flask

`requirements.txt`:
Package      |Version
------------ |-------
blinker      |1.8.2
click        |8.1.7
Flask        |3.0.3
itsdangerous |2.2.0
Jinja2       |3.1.4
MarkupSafe   |2.1.5
random11     |0.0.1
Werkzeug     |3.0.3
### Installation
- ` python3 -m venv app`
- ` source venv/bin/activate`
- install packages:
  - if on local machine: ` pip install -r requirements.txt`
  - on Replit: click on "Dependencies" under Tools in the side panel, then manually add packages:
    - Flask,
    - random ( it;s only used in the data generation scripts. It seems like this package is already included by default)

### Run
If you want to randomly generate a different set of datasets: `python3 data_generation.py`

If you are on local machine:
- go to the directory where the main.py is located, run `python3 main.py`.
- go to the local host displayed on your console, likely being: http://127.0.0.1:5000

If you are on Replit:
- open the Shell and run `python3 main.py` | or click on the green `Run` button :D
- on the bottom of the console, there's a line looks like "Port :5000 opened ...", click on the settings icon located on the right end of this line, and configure the external ports from there.

## Assumptions
- assume calling `/searchBestTrip` API once == calling getHotels + getFlights once each.
- assuming all flights are avialable everyday.
- assuming all hotels are always avialable, and prices are the same each day, so we are booking the same hotels everyday.

## Major Optimizations
- Implemented LRU cache in backend handling similar queries (budget, origin). user can only send predefined budget ranges to increasse efficiency of LRU.
- Reduce time complexity of computing matching flight with hotels with hashmap.
