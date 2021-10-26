from typing import List

from fastapi import Depends, FastAPI, BackgroundTasks
from time import sleep
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def compute_user_score(event: schemas.Event):
    print("Executing compute user score ...")
    sleep(10)
    print("Done computing user score ...")
    pass


def compute_user_badges(event: schemas.Event):
    print("Executing compute user badges ...")
    sleep(10)
    print("Done computing user badges ...")
    pass


@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.Event,
                 background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db)):
    item = crud.create_event(db=db, event=event)
    background_tasks.add_task(compute_user_score, event=event)
    background_tasks.add_task(compute_user_badges, event=event)
    return item


@app.get("/events/", response_model=List[schemas.Event])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_events(db, skip=skip, limit=limit)
    return items


@app.get("/users/{user_id}/events/", response_model=List[schemas.Event])
def get_user_events(user_id: str,
                    skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(get_db)):
    items = crud.get_user_events(db, user_id=user_id, skip=skip, limit=limit)
    return items
