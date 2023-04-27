# Open Food Facts Events

API written using Fast API to manage events and implement a leaderboard / badge
system.

It can also be the foundation:
* for users and categories dashboard / flow 
* a rating system for edits to help moderation
* statistics on read events like scans

## Installation

To run the API locally, run `make dev`. This assumes you have `Makefile`, `Docker` and `docker-compose` installed on your machine.

It will work best with a local install of Product Opener sending events to it: https://openfoodfacts.github.io/openfoodfacts-server/ but you can simulate events.

## API Documentation

The API documentation is available at https://events.openfoodfacts.net/docs.

## Examples

### cURL

**Create an event (needs auth):**
```
curl -X POST -u admin:admin https://events.openfoodfacts.net/events
```

**Get the list of events:**
```
curl https://events.openfoodfacts.net/events
```

**Get leaderboard:**
```
curl https://events.openfoodfacts.net/leaderboard
```

**Get user badges:**
```
curl https://events.openfoodfacts.net/badges?user_id=<USER_ID>
curl https://events.openfoodfacts.net/badges?device_id=<DEVICE_ID>
```

### Python

```py
import requests

API_URL = 'https://events.openfoodfacts.net' 

# Create event
response = requests.post(API_URL + '/events', json={'user_id': 'test', 'event_type': 'invite_shared'})
print(response)

# Get leaderboard
leaderboard = requests.get(API_URL + '/leaderboard').json()
for ix, data in leaderboard.items():
    name = data['user_id'] or data['device_id']
    points = data['score']
    print('{ix}: {name} with {score} points')

# Get user badges
badges = request.get(API_URL + '/badges?user_id=test').json()
print(badges)
```
