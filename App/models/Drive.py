from App.database import db

class Drive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    #time = db.Column(db.Time, nullable=False, default=db.func.current_time())
    stops = db.relationship('Stop', backref='drive', lazy=True)

    def __init__(self, driver_id, street_id, date):
        self.driver_id = driver_id
        self.street_id = street_id
        self.date = date

    def get_json(self):
        return {
            'drive_id': self.drive_id,
            'driver_id': self.driver_id,
            'street_id': self.street_id,
            'date': self.date
        }
    
    def __repr__(self):
        from App.models.Driver import Driver  # Import here to avoid circular imports
        driver = Driver.query.filter_by(driver_id=self.driver_id).first()
        driver_name = driver.driver_name if driver else "Unknown"
        return f"<Drive {self.drive_id} by Driver {self.driver_id} {driver_name.upper()} on Street {self.street_id} at {self.date} >"