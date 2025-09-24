from App.database import db
from App.models.Drive import Drive
from App.models.Stop import Stop
from App.models.Driver import Driver
from App.models.user import User

class Resident(User):
    resident_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    resident_name = db.Column(db.String(50), nullable=False)
    street_id = db.Column(db.Integer, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity' :  'resident',
    }

    def __init__(self, username, password, street_id):
        super().__init__(username, password, user_type='resident')
        self.resident_name = username
        self.street_id = street_id

    def get_json(self):
        data = super().get_json()
        data.update({
            'resident_id': self.resident_id,
            'resident_name': self.resident_name,
            'street_id': self.street_id
        })
        return data
    
    def view_inbox(self, street_id):
        """Fetch all messages for the resident's street."""
        return Drive.query.filter_by(street_id = street_id).all()
    
    def request_stop(self, resident_id, drive_id, street_id):
        """Request a stop from a driver on the resident's street."""
        stop = Stop.query.filter_by(resident_id=resident_id, drive_id=drive_id, street_id=street_id).first()
        if stop:
            print("Stop already requested.")
            return None

        resident = Resident.query.filter_by(resident_id=resident_id).first()
        if resident.street_id != street_id:
            print("Resident can only request stops on their own street.")
            return None
        
        new_drive = Drive.query.filter_by(drive_id=drive_id, street_id=street_id).first()
        if not new_drive:
            print("No drive found for the specified driver and street.")
            return None
        else:
            stop = Stop(resident_id = resident_id, driver_id = new_drive.driver_id, drive_id = drive_id, street_id = street_id)
            db.session.add(stop)
            db.session.commit()
            return stop
        
    def view_driver(self, driver_id):
        """Fetch driver details."""
        driver = Driver.query.filter_by(id=driver_id, user_type='driver').first()
        if driver:
            return {
                'driver_id': driver.driver_id,
                'name': driver.driver_name,
                'status': driver.status,
                'location': driver.street_id
            }
        return None