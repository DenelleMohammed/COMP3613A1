from App.models import User
from App.database import db
from App.models.Resident import Resident
from App.models.Driver import Driver

def create_user(username, password, user_type='resident', **kwargs):
    if user_type not in ['resident', 'driver']:
        raise ValueError("user_type must be either 'resident' or 'driver'")
    if user_type == 'resident':
        street_id = kwargs.get('street_id')
        newuser = Resident(username, password, street_id)
    elif user_type == 'driver':
        status = kwargs.get('status', 'active')
        street_id = kwargs.get('street_id')
        newuser = Driver(username, password, status, street_id)
    else:
        newuser = User(username, password, user_type)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
