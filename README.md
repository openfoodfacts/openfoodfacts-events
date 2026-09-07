# Open Food Facts Events

API written using FastAPI to manage events and implement a leaderboard and badge
system. It was written during the Google.org Fellowship Hackathon and is now
being refactored into a reusable events and gamification backend.

It can also be the foundation:
* for users and categories dashboard / flow 
* a rating system for edits to help moderation
* statistics on read events like scans

## Contributing

See [AGENTS.md](AGENTS.md) for development setup, quality checks, and security
guidelines. Contributions are welcome, especially around integrating this API
with the rest of Open Food Facts.

## Installation

To run the API locally, install Docker and Docker Compose, copy the required
settings into a local `.env` file, and run `make dev`. The API is then
available at http://localhost:8000 and its interactive documentation is at
http://localhost:8000/docs.

For a non-containerized setup, install dependencies with `poetry install`, set
`ADMIN_USERNAME` and `ADMIN_PASSWORD`, and run:

```sh
poetry run uvicorn app.main:app --reload
```

It will work best with a local install of Product Opener sending events to it: https://openfoodfacts.github.io/openfoodfacts-server/ but you can simulate events.

## API Documentation

The API documentation is available at https://events.openfoodfacts.net/docs.

## Examples

### cURL

**Create an event (needs auth):**
```sh
curl -X POST -u admin:admin https://events.openfoodfacts.net/events
```

**Get the list of events:**
```sh
curl https://events.openfoodfacts.net/events
```

**Get leaderboard:**
```sh
curl https://events.openfoodfacts.net/leaderboard
```

**Get user badges:**
```sh
curl https://events.openfoodfacts.net/badges?user_id=<USER_ID>
curl https://events.openfoodfacts.net/badges?device_id=<DEVICE_ID>
```

### Python

```py
import requests

API_URL = "https://events.openfoodfacts.net"

# Create event
response = requests.post(API_URL + '/events', json={'user_id': 'test', 'event_type': 'invite_shared'})
print(response)

# Get leaderboard
leaderboard = requests.get(API_URL + '/leaderboard').json()
for ix, data in leaderboard.items():
    name = data['user_id'] or data['device_id']
    points = data['score']
    print(f"{ix}: {name} with {points} points")

# Get user badges
badges = requests.get(API_URL + "/badges?user_id=test").json()
print(badges)
```
