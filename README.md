# Open Food Facts Events

API written using Fast API to manage events and implement a leaderboard / badge
system.

## Installation

To run the API locally, run `make dev`. This assumes you have `Makefile`, `Docker` and `docker-compose` installed on your machine.

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
# Database schema migrations
The schema migrations are managed by [Alembic](https://alembic.sqlalchemy.org)

You can type for example
```
# generate the schema migration script
# To do after each important update in the model
alembic revision -m "My model changes"
# upgrade the schema at the top of the revision history
alembic upgrade head
```

You can find more informations in the [Alembic](https://alembic.sqlalchemy.org) documentation, and [pytest-alembic](https://pytest-alembic.readthedocs.io/en/latest/) for writing tests about your migrations.