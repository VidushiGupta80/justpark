from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr


db = SQLAlchemy()

class ParkingLot(db.Model):
    __tablename__ = "parkingLot"
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String, nullable = False)
    state  = db.Column(db.String, nullable = False)
    country = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)

class ExitPoint(db.Model):
    __tablename__ = "exitPoint"
    id = db.Column(db.Integer, primary_key = True)
    floorNumber = db.Column(db.Integer, nullable = False)
    vehicleCount = db.Column(db.Integer, nullable = False)
    displayID = db.Column(db.Integer, db.ForeignKey("displayBoard.id"), nullable = False)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), nullable = False)

class EntryPoint(db.Model):
    __tablename__ = "entryPoint"
    id = db.Column(db.Integer, primary_key = True)
    floorNumber = db.Column(db.Integer, nullable = False)
    vehicleCount = db.Column(db.Integer, nullable = False)
    displayID = db.Column(db.Integer, db.ForeignKey("displayBoard.id"), nullable = False)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), nullable = False)

class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String, nullable = False)
    MiddleName = db.Column(db.String, nullable = True)
    LastName = db.Column(db.String, nullable = False)
    houseNumber = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state  = db.Column(db.String, nullable = False)
    country = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    personType = db.Column(db.String, nullable = False)
    contactNumber = db.Column(db.Integer, nullable = False)
    __mapper_args__ = {'polymorphic_on': personType}

class Customer(Person):
    __mapper_args__ = {'polymorphic_identity': 'customer'}
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    vehicleType = db.Column(db.String, nullable = False)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.number"), nullable = False)

class Admin(Person):
    __mapper_args__ = {'polymorphic_identity' : 'admin'}
    password = db.Column(db.String, nullable = False)

    @declared_attr
    def emailID(cls):
        return Person.__table__.c.get('emailID', Column(String))

    @declared_attr
    def salary(cls):
        return Person.__table__.c.get('salary', Column(Integer))

class ParkingAttendant(Person):
    __mapper_args__ = {'polymorphic_identity' : 'parkingAttendant'}
    joiningDate = db.Column(db.DateTime, nullable = False)
    leavingDate = db.Column(db.DateTime, nullable = True)
    floor = db.Column(db.Integer, nullable = False)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.number"), nullable = False)

    @declared_attr
    def emailID(cls):
        return Person.__table__.c.get('emailID', Column(String))

    @declared_attr
    def salary(cls):
        return Person.__table__.c.get('salary', Column(Integer))

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    vehicleNumber = db.Column(db.String, primary_key = True)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.number"), nullable = False)
    customerID = db.Column(db.Integer, db.ForeignKey("person.id"), nullable = False)
    wheels = db.Column(db.Integer, nullable = False)
    vehicleType = db.Column(db.String, nullable = False)

class Ticket(db.Model):
    __tablename__ = "ticket"
    ticketNumber = db.Column(db.String, primary_key = True)
    customerID = db.Column(db.Integer, db.ForeignKey("person.id"), nullable = False)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    ParkingAttendantID = db.Column(db.Integer, db.ForeignKey("person.id"), nullable = True)
    inTime = db.Column(db.DateTime, nullable = False)
    outTime = db.Column(db.DateTime, nullable = True)
    chargingFee = db.Column(db.Integer, nullable = True)

class ChargingPanel(db.Model):























