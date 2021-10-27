from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from sqlalchemy import desc

from . import models, schemas


#--------#
# EVENTS #
#--------#
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


#--------#
# BADGES #
#--------#
def get_user_badges(db: Session, user_id: str):
    return db.query(models.Badge).filter(models.Badge.user_id == user_id).all()


def create_or_update_user_badge(db: Session, user_id: str, badge_name: str,
                                level: int):
    try:
        db_item = db.query(models.Badge).filter(
            models.Badge.user_id == user_id,
            models.Badge.badge_name == badge_name).one()
        db_item.level = level
    except NoResultFound:
        db_item = models.Badge(user_id=user_id,
                               badge_name=badge_name,
                               level=level)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#-------------#
# LEADERBOARD #
#-------------#
def get_user_score(db: Session, user_id: str, event_type: str = None):
    query = db.query(func.sum(models.Event.points).label("total_score")).filter(
        models.Event.user_id == user_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    total_score = query.one().total_score or 0
    return {"score": total_score}


def get_leaderboard(db: Session, event_type: str = None):
    query = db.query(
        func.sum(models.Event.points).label("total_score"),
        models.Event.user_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    query = query.group_by(models.Event.user_id)
    results = query.order_by(desc('total_score')).all()
    return [{"score": r.total_score, "user_id": r.user_id} for r in results]
