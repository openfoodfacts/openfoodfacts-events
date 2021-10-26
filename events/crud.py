from sqlalchemy.orm import Session

from . import models, schemas


def get_user_events(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(
        models.Event.user_id == user_id).offset(skip).limit(limit).all()


def count_user_events(db: Session, user_id: str, event_type: str):
    return db.query(
        models.Event).filter(models.Event.user_id == user_id,
                             models.Event.event_type == event_type).count()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def count_events(db: Session, event_type: str):
    return db.query(
        models.Event).filter(models.Event.event_type == event_type).count()


def create_event(db: Session, event: schemas.Event):
    db_item = models.Event(**event.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
