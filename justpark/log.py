from justpark import db

class VehicleLog(db.Model):
    __tablename__ = "vehicleLog"
    vehicleNumber = db.Column(db.String, primary_key = True)
    inTime = db.Column(db.DateTime, primary_key = True)
    