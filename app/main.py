from typing import List

from fastapi import Depends, FastAPI, BackgroundTasks
from time import sleep
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from starlette_exporter import PrometheusMiddleware, handle_metrics

from . import crud, models, schemas, constants
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#--------#
# EVENTS #
#--------#
@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.Event,
                 background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db)):
    event.points = constants.EVENT_TYPES[event.event_type]["points"]
    item = crud.create_event(db=db, event=event)
    background_tasks.add_task(compute_user_badges, db=db, event=event)
    return item


@app.get("/events/", response_model=List[schemas.Event])
def get_events(user_id: str = None,
               device_id: str = None,
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db)):
    items = crud.get_events(db,
                            user_id=user_id,
                            device_id=device_id,
                            skip=skip,
                            limit=limit)
    return items


@app.get("/events/count")
def get_events_count(user_id: str = None,
                     device_id: str = None,
                     db: Session = Depends(get_db)):
    items = {}
    for event_type in constants.EVENT_TYPES:
        items[event_type] = crud.count_events(db,
                                              event_type=event_type,
                                              user_id=user_id,
                                              device_id=device_id)
    return items


#--------#
# BADGES #
#--------#
def compute_user_badges(event: schemas.Event, db: Session = Depends(get_db)):
    query = db.query(
        models.Event).filter(models.Event.event_type == event.event_type)
    if event.user_id:
        query = query.filter(models.Event.user_id == event.user_id)
    elif event.device_id:
        query = query.filter(models.Event.device_id == event.device_id)
    count = query.count()
    if count == 1:
        badge_name = constants.EVENT_TYPES[event.event_type]["init_badge"]
        level = 0
    else:
        badge_name = constants.EVENT_TYPES[event.event_type]["badge"]
        level = count / 10
    return crud.create_or_update_user_badge(db=db,
                                            user_id=event.user_id,
                                            device_id=event.device_id,
                                            badge_name=badge_name,
                                            level=level)


@app.get("/badges")
def get_badges(user_id: str = None,
               device_id: str = None,
               db: Session = Depends(get_db)):
    return crud.get_badges(db, user_id=user_id, device_id=device_id)


@app.get("/scores")
def get_scores(user_id: str = None,
               device_id: str = None,
               event_type: str = None,
               db: Session = Depends(get_db)):
    return crud.get_scores(db,
                           user_id=user_id,
                           device_id=device_id,
                           event_type=event_type)


@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db), event_type: str = None):
    return crud.get_leaderboard(db, event_type=event_type)
