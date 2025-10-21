from functools import wraps
from flask import session, redirect, url_for, render_template, g
from src.services.item_service import ItemService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+mysqlconnector://root:1234@localhost/online-store-python'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_owner(f):
    @wraps(f)
    def decorated_function(item_id, *args, **kwargs):
        db = SessionLocal()
        try:
            item = ItemService.get_item(db, item_id)
            user_id = session.get('user_id')
            if item and item.owner_id == user_id:
                return f(item_id, *args, **kwargs)
            else:
                return render_template('404.html', error='You are not authorized'), 403
        finally:
            db.close()
    return decorated_function


def check_not_owner(f):
    @wraps(f)
    def decorated_function(item_id, *args, **kwargs):
        db = SessionLocal()
        try:
            item = ItemService.get_item(db, item_id)
            user_id = session.get('user_id')
            if item and item.owner_id != user_id:
                return f(item_id, *args, **kwargs)
            else:
                return render_template('404.html', error='You are not authorized'), 403
        finally:
            db.close()
    return decorated_function
