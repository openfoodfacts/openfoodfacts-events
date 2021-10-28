from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from sqlalchemy import desc

from . import models, schemas, database


#--------#
# EVENTS #
#--------#
def _get_base_query(db: Session,
                    model: database.Base,
                    user_id: str = None,
                    device_id: str = None,
                    query=None):
    if not query:
        query = db.query(model)
    if user_id:
        query = query.filter(model.user_id == user_id)
    elif device_id:
        query = query.filter(model.device_id == device_id)
    return query


def get_events(db: Session,
               user_id: str = None,
               device_id: str = None,
               skip: int = 0,
               limit: int = 100):
    query = _get_base_query(db, models.Event, user_id, device_id)
    return query.offset(skip).limit(limit).all()


def count_events(db: Session,
                 user_id: str = None,
                 device_id: str = None,
                 event_type: str = None):
    query = _get_base_query(db, models.Event, user_id, device_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    return query.count()


def create_event(db: Session, event: schemas.EventCreate):
    db_item = models.Event(**event.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#--------#
# BADGES #
#--------#
def get_badges(db: Session, user_id: str = None, device_id: str = None):
    query = _get_base_query(db,
                            models.Badge,
                            user_id=user_id,
                            device_id=device_id)
    return query.all()


def create_or_update_user_badge(db: Session,
                                badge_name: str,
                                level: int,
                                user_id: str = None,
                                device_id: str = None):
    try:
        query = _get_base_query(db,
                                models.Badge,
                                user_id=user_id,
                                device_id=device_id)
        db_item = query.filter(models.Badge.badge_name == badge_name).one()
        db_item.level = level
    except NoResultFound:
        db_item = models.Badge(user_id=user_id,
                               device_id=device_id,
                               badge_name=badge_name,
                               level=level)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


#-------------#
# LEADERBOARD #
#-------------#
def get_scores(db: Session,
               user_id: str = None,
               device_id: str = None,
               event_type: str = None):
    query = db.query(func.sum(models.Event.points).label("total_score"))
    query = _get_base_query(db,
                            models.Event,
                            user_id=user_id,
                            device_id=device_id,
                            query=query)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    total_score = query.one().total_score or 0
    return {"score": total_score}


def get_leaderboard(db: Session, event_type: str = None):
    query = db.query(
        func.sum(models.Event.points).label("total_score"),
        models.Event.user_id, models.Event.device_id)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    query = query.group_by(models.Event.user_id, models.Event.device_id)
    results = query.order_by(desc('total_score')).all()
    return [{'score': r.total_score, 'user_id': r.user_id} for r in results]
