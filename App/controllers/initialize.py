from .user import create_user
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', user_type = 'resident', street_id = 10)
    create_user('alice', 'alicepass', user_type = 'driver', status = 'active', street_id = 20)
    create_user('rob', 'robpass', user_type = 'resident', street_id = 30)
    create_user('eve', 'evepass', user_type = 'driver', status = 'inactive', street_id = 40)
    create_user('mallory', 'mallorypass', user_type = 'resident', street_id = 50)
    create_user('trent', 'trentpass', user_type = 'driver', status = 'active', street_id = 60)

