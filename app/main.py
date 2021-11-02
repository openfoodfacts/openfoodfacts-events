from typing import List

from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session
from starlette_exporter import PrometheusMiddleware, handle_metrics

from . import crud, models, schemas, constants
from .database import SessionLocal, engine

import os
import secrets

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

security = HTTPBasic()

ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# --------#
# EVENTS #
# --------#
@app.post("/events", response_model=schemas.EventBase)
def create_event(
    event: schemas.EventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username),
):
    event.points = 0
    if event.event_type in constants.EVENT_TYPES:
        event.points = constants.EVENT_TYPES[event.event_type]["points"]
    item = crud.create_event(db=db, event=event)
    background_tasks.add_task(compute_user_badges, db=db, event=event)
    return item


@app.get("/events", response_model=List[schemas.EventBase])
def get_events(
    user_id: str = None,
    device_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = crud.get_events(
        db, user_id=user_id, device_id=device_id, skip=skip, limit=limit
    )
    return items


@app.get("/events/count")
def get_events_count(
    user_id: str = None, device_id: str = None, db: Session = Depends(get_db)
):
    items = {}
    for event_type in constants.EVENT_TYPES:
        items[event_type] = crud.count_events(
            db, event_type=event_type, user_id=user_id, device_id=device_id
        )
    return items


# --------#
# BADGES #
# --------#
def compute_user_badges(event: schemas.EventCreate, db: Session = Depends(get_db)):
    query = db.query(models.Event).filter(models.Event.event_type == event.event_type)
    if event.user_id:
        query = query.filter(models.Event.user_id == event.user_id)
    elif event.device_id:
        query = query.filter(models.Event.device_id == event.device_id)
    count = query.count()
    event_config = constants.EVENT_TYPES.get(event.event_type)
    if not event_config:
        app.logger.warning(
            f"Event type {event.event_type} is not configured in "
            f"constants.EVENT_TYPES."
        )
        return
    if count == 1:
        badge_name = constants.EVENT_TYPES[event.event_type]["init_badge"]
        level = 0
    elif count >= 10:
        badge_name = constants.EVENT_TYPES[event.event_type]["badge"]
        level = int(count / 10)
    else:
        return
    return crud.create_or_update_user_badge(
        db=db,
        user_id=event.user_id,
        device_id=event.device_id,
        badge_name=badge_name,
        level=level,
    )


@app.get("/badges", response_model=List[schemas.BadgeBase])
def get_badges(
    user_id: str = None, device_id: str = None, db: Session = Depends(get_db)
):
    return crud.get_badges(db, user_id=user_id, device_id=device_id)


@app.get("/scores")
def get_scores(
    user_id: str = None,
    device_id: str = None,
    event_type: str = None,
    db: Session = Depends(get_db),
):
    return crud.get_scores(
        db, user_id=user_id, device_id=device_id, event_type=event_type
    )


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db), event_type: str = None):
    return crud.get_leaderboard(db, event_type=event_type)
