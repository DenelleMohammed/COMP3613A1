from App.database import db

class Stop(db.Model):
    stop_id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.drive_id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.resident_id'), nullable=False)  
    street_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='requested')  # 'requested', 'completed', etc.


    def __init__(self, resident_id, driver_id, drive_id, street_id, status='requested'):
        self.resident_id = resident_id # To be set when a resident requests the stop
        self.driver_id = driver_id  # To be set based on the drive's driver
        self.drive_id = drive_id
        self.street_id = street_id
        self.status = status

    def get_json(self):
        return {
            'resident_id': self.resident_id,
            'driver_id': self.driver_id,
            'stop_id': self.stop_id,
            'drive_id': self.drive_id,
            'street_id': self.street_id,
            'status': self.status
        }
    
    def __repr__(self):
        return f"<Stop {self.stop_id} for Drive {self.drive_id} on Street {self.street_id} - By: Resident {self.resident_id}>"