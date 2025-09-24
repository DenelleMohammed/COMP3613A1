from App.database import db
from App.models.Drive import Drive
from App.models.Stop import Stop
from App.models.user import User 

class Driver(User):
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    driver_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active', 'inactive', etc.
    street_id = db.Column(db.Integer, nullable=False)
    drives = db.relationship('Drive', backref='driver', lazy=True)
    stop = db.relationship('Stop', backref='driver', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'driver',
    }

    def __init__(self, username, password, status, street_id):
        super().__init__(username, password, user_type='driver')
        self.driver_name = username
        self.status = status
        self.street_id = street_id

    def get_json(self):
        data = super().get_json()
        data.update({
            'diver_id': self.driver_id,
            'name': self.driver_name,
            'status': self.status,
            'street_id': self.street_id
        })
    
    def schedule_drive(self, driver_id, street_id, date):
        """Schedule a new drive for the driver."""
        new_drive = Drive(driver_id=driver_id, street_id=street_id, date=date)
        self.drives.append(new_drive)
        db.session.add(new_drive)
        db.session.commit()
        return new_drive
        