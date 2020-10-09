from justpark import db

class VehicleLog(db.Model):
    __tablename__ = "vehicleLog"
    vehicleNumber = db.Column(db.String, primary_key = True)
    inTime = db.Column(db.DateTime, primary_key = True)
    entryPoint = db.Column(db.Integer, nullable = False)
    exitPoint = db.Column(db.Integer, nullable = True)
    vehicleType = db.Column(db.String, nullable = False)
    outTime = db.Column(db.DateTime, nullable = True)
    spotID = db.Column(db.Integer, nullable = False)
    parkingLotID = db.Column(db.Integer, nullable = False)
    floorNumber = db.Column(db.Integer, nullable = False)
    parkingAttendantID = db.Column(db.Integer, nullable = True)
    