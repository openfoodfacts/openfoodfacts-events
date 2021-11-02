from app.main import ADMIN_PASSWORD, ADMIN_USERNAME, app
from app.constants import EVENT_TYPES
from fastapi.testclient import TestClient

import os

client = TestClient(app)

ADMIN_USERNAME = os.environ['ADMIN_USERNAME']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
TEST_EVENT = {
    'user_id': 'test',
    'event_type': 'invite_shared',
    'device_id': '1A2B-2B3C-3D4E-4F5G',
}
TEST_EVENT_CFG = EVENT_TYPES[TEST_EVENT['event_type']]


def test_get_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_get_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200


#-----------------#
# EVENTS ENDPOINT #
#-----------------#


def test_get_events():
    response = client.get("/events")
    assert response.status_code == 200


def test_create_event():
    response = client.post("/events",
                           auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
                           json=TEST_EVENT)
    assert response.status_code == 200
    json = response.json()
    assert json['barcode'] == None
    assert json['points'] == TEST_EVENT_CFG['points']


def test_create_event_unauthorized():
    response = client.post("/events", json=TEST_EVENT)
    assert response.status_code == 401


#-------------#
# LEADERBOARD #
#-------------#


def test_get_leaderboard():
    response = client.get("/leaderboard")
    assert response.status_code == 200


def test_get_badges():
    response = client.get('/badges')
    assert response.status_code == 200
