from flask import Blueprint
from justpark import app, db, bcrypt
from time import time
from flask import jsonify, request
from sqlalchemy import and_
from justpark.models import *
from justpark.log import VehicleLog
from justpark.exceptions import DatabaseException
import datetime
import json
import math
from app.libs.flask_login_multi import login_user, current_user, logout_user, login_required

parkingAttendant = Blueprint("parkingAttendant", __name__)

@parkingAttendant.route('/exit/customer/<string:ticketNumber>', methods = ['POST'])
@login_required
def exitCustomer(ticketNumber):
    if current_user.is_authenticated is False:
        raise DatabaseException("Login required")
    parkingAttendantID = current_user.get_id()
    requestBody = request.json
    outTime = datetime.datetime.utcnow()
    ticket = Ticket.query.get(ticketNumber)
    if ticket is None:
        raise DatabaseException("Invalid ticket")
    if ticket.outTime is not None:
        return jsonify({'status': 200, 'message': 'Vehicle already exited.'})
    # checking time limit of 15 mins to exit from parking lot
    if ticket.isPaid and (outTime - ticket.checkTime).total_seconds() > 900:
        ticket.isPaid = False
        ticket.checkTime = None
        db.session.commit()
        raise DatabaseException('You have exceeded the time limit to exit the parking lot. Please pay again')
    # updating ticket
    ticket.outTime = outTime
    ticket.parkingAttendantID = parkingAttendantID
    # updating exit point vehicle count
    exitPoint = ExitPoint.query.filter(and_(ExitPoint.id == requestBody['exitNumber'],
                                            ExitPoint.floorNumber == requestBody['floorNumber'],
                                            ExitPoint.parkingLotID == requestBody['parkingLotID'])).first()
    exitPoint.vehicleCount += 1
    # updating free spots
    spotID = ticket.spotID
    vehicle = Vehicle.query.filter_by(ticketNumber = ticketNumber).first()
    parkingSpot = ParkingSpot.query.filter(and_(ParkingSpot.spotID == spotID,
                                                ParkingSpot.parkingLotID == requestBody['parkingLotID'],
                                                ParkingSpot.floorNumber == requestBody['floorNumber'],
                                                ParkingSpot.spotType == vehicle.vehicleType)).first()
    parkingSpot.status = False
    # updating vehicle log
    logger = VehicleLog.query.filter(and_(VehicleLog.vehicleNumber == vehicle.vehicleNumber,
                                          VehicleLog.inTime == ticket.inTime)).first()
    logger.exitPoint = requestBody['exitNumber']
    logger.outTime = outTime
    logger.parkingAttendantID = parkingLotID
    if ticket.isPaid == False:
        ticket.isPaid = True    
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Thank you for letting us be of service.'})

@parkingAttendant.route('/register', methods = ['GET', 'POST'])
def registerParkingAttendant():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
     # check for exisiting userID and email ID in both admin and parking attendant class
    ID = Admin.query.filter(Admin.adminID ==  requestBody['adminID'])
    if ID:
        raise DatabaseException('User ID already exists. Use different ID')
    ID = ParkingAttendant.query.filter(ParkingAttendant.parkingAttendantID ==  requestBody['adminID'])
    if ID:
        raise DatabaseException('User ID already exists. Use different ID')
    email = ParkingAttendant.query.filter(ParkingAttendant.emailID == requestBody['emailID'])
    if email:
        raise DatabaseException('Email ID already taken. Use different Email ID')
    email = Admin.query.filter(Admin.emailID == requestBody['emailID'])
    if email:
        raise DatabaseException('Email ID already taken. Use different Email ID')
    # hashing password
    hashedPassword = bcrypt.generate_password_hash(requestBody['password']).decode('utf-8')
    attendant = ParkingAttendant(parkingAttendantID = requestBody['parkingAttendantID'],
                  password = hashedPassword,
                  joiningDate = requestBody['joiningDate'],
                  leavingDate = None;
                  floor = requestBody['floor']
                  emailID = requestBody['emailID'],
                  salary = requestBody['salary'],   
                  firstName = requestBody['firstName'],
                  middleName = requestBody['middleName'],
                  lastName = requestBody['lastName'],
                  address = requestBody['address'],     
                  city = requestBody['city'],
                  state  = requestBody['state'],
                  country = requestBody['country'],
                  pincode = requestBody['pincode'],
                  contactNumber = requestBody['ContactNumber'])
    db.session.add(admin)
    db.session.commit()
    return jsonify({'status' : 200,
                    'message': 'You have been successfully registered as parking attendant'})


@parkingAttendant.route('/login', methods = ['GET', 'POST'])
def loginParkingAttendant():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
    parkingAttendant = ParkingAttendant.query.get(requestBody['parkingAttendantID'])
    if parkingAttendant and bcrypt.check_password_hash(parkingAttendant.password, requestBody['password']):
        login_user(parkingAttendant)
        return jsonify({'status': 200, 
                        'message': 'Login successful'})
    else:
        return jsonify({'status': ,
                        'message': 'Login unsuccessful. Please try again'})

@parkingAttendant.route('/logout')
def logoutParkingAttendant():
    logout_user()
    return jsonify({'status': 200,
                    'message': 'You have succesfully logged out'})


