from flask import Blueprint
from justpark import app, db, bcrypt
from time import time
from flask import jsonify, request
from sqlalchemy import and_, desc
from justpark.models import *
from justpark.log import VehicleLog
from justpark.utils import generateTicketNumber, generateCustomerID, generateVehicleID
from justpark.exceptions import DatabaseException
import datetime
import json
import math
from app.libs.flask_login_multi import login_user, current_user, logout_user, login_required

main = Blueprint("main", __name__)

@main.route('/getAmount/ticketNumber/<string:ticketNumber>', methods=['GET'])
def getAmountTicket(ticketNumber):
    ticket = Ticket.query.get(ticketNumber)
    print(ticket)
    if ticket is None:
        raise DatabaseException("This ticket does not exist")
    # time of ckecking aount of ticket for total hours
    checkTime = datetime.datetime.utcnow()
    timeDuration = checkTime - ticket.inTime 
    # converting time duration from seconds to hours
    timeDurationHours = math.ceil(timeDuration.total_seconds() / 3600)
    # get vehicle number for vehicle details
    vehicleNumber = ticket.vehicleNumber
    # object of vehicle of customer
    vehicleInfo = Vehicle.query.filter(and_(Vehicle.vehicleNumber == vehicleNumber and Vehicle.ticketNumber == ticketNumber)).first()
    vehicleType = vehicleInfo.vehicleType
    # parking fee rate set by admin for this particluar vehicle type
    rate = Rate.query.get(vehicleType)      
    # calculating total parking fee till checkout time
    parkingFee = rate.parkingRate * timeDurationHours
    chargingHours = 0
    chargingFee = 0
    # calculating charging fee if the vehicle type is electric car
    if vehicleType == 'Electric Car':
        # checking all the connections made with charging panel
        connections = LastConnection.query(LastConnection.connect, LastConnection.disconnect).filter_by(ticketNumber = ticketNumber).all()
        if connections is not None:
            for connect, disconnect in connection:
                # if the vehicle is still charging, giving a message that charging fee cant be calculated
                if disconnect is None:
                    return jsonify({'ticketNumber': ticketNumber,
                                    'vehicleNumber': vehicleNumber,
                                    'checkTime': checkTime,
                                    'totalParkingHours': timeDurationHours,
                                    'totalChargingHours': chargingHours, 
                                    'parkingFee': parkingFee, 
                                    'chargingFee': "Your electric car is connected to charging panel",
                                    'totalAmount': parkingFee + chargingFee})
                # calculating total charging hours from every connection
                chargingHours += math.ceil((disconnect - connect).total_seconds() / 3600)
        # getting rate of charging set by admin
        chargingRate = ChargingRate.query.filter_by(ChargingRate.vehicleType == vehicleType).one()
        # calculating total charging fee till checkout time
        chargingFee = chargingRate * chargingHours
    return jsonify({'ticketNumber': ticketNumber,
                    'vehicleNumber': vehicleNumber,
                    'checkTime': checkTime,
                    'totalParkingHours': timeDurationHours,
                    'totalChargingHours': chargingHours, 
                    'parkingFee': parkingFee, 
                    'chargingFee': chargingFee,
                    'totalAmount': parkingFee + chargingFee})

@main.route('/getAmount/vehicleNumber/<string:vehicleNumber>', methods=['GET'])
def getAmountVehicle(vehicleNumber):
    # getting vehicle object for the gien vehicle number
    ticket = Ticket.query.filter(and_(Ticket.vehicleNumber == vehicleNumber and Ticket.outTime == None).first()
    if ticket is None:
        raise DatabaseException("This vehicle is not inside this parking lot")
    # time of checking the amount of ticket
    checkTime = datetime.datetime.utcnow()
    timeDuration = checkTime - ticket.inTime
    # converting total time duration in hours from seconds
    timeDurationHours = math.ceil(timeDuration.total_seconds() / 3600)
    vehicleType = ticket.vehicleType
    # getting parking rate set by admin of the vehicle type 
    rate = Rate.query.get(vehicleType) 
    # calculting total parking fee till check time  
    parkingFee = rate.parkingRate * timeDurationHours
    chargingHours = 0
    chargingFee = 0
    # calculating charging fee if the vehicle type is electric car
    if vehicleType == 'Electric Car':
        # getting all connections made by the vehicle with the charging panel
        connections = LastConnection.query(LastConnection.connect, LastConnection.disconnect).filter_by(ticketNumber = ticket.ticketNumber).all()
        if connections is not None:
            for connect, disconnect in connection:
                # sending a message if the vehicle is still connected to the charging panel
                if disconnect is None:
                   return jsonify({'ticketNumber': ticket.ticketNumber,
                                    'vehicleNumber': vehicleNumber,
                                    'checkTime': checkTime,
                                    'totalParkingHours': timeDurationHours,
                                    'totalChargingHours': chargingHours, 
                                    'parkingFee': parkingFee, 
                                    'chargingFee': "Your electric car is connected to charging panel",
                                    'totalAmount': parkingFee + chargingFee})
                # calculating total hours of charging
                chargingHours += math.ceil((disconnect - connect).total_seconds() / 3600)
        # getting charging rate set by admin
        chargingRate = ChargingRate.query.filter_by(ChargingRate.vehicleType == vehicleType).one()
        # calculating total charging fee till check time
        chargingFee = chargingRate * chargingHours
    return jsonify({'ticketNumber': ticket.ticketNumber,
                    'vehicleNumber': vehicleNumber,
                    'checkTime': checkTime,
                    'totalParkingHours': timeDurationHours,
                    'totalChargingHours': chargingHours, 
                    'parkingFee': parkingFee, 
                    'chargingFee': chargingFee,
                    'totalAmount': parkingFee + chargingFee})


@main.route('/getFreeSpots/<int:parkingLotID>/<int:floorNumber>/<string:vehicleType>',methods=['GET'])
def getFreeSpots(parkingLotID, floorNumber, vehicleType):
    # getting all designed parkingspots of the given vehicle type for given floor number and parking ID
    allSpots = ParkingSpot.query.filter(and_(ParkingSpot.parkingLotID == parkingLotID, ParkingSpot.floorNumber == floorNumber, ParkingSpot.spotType == vehicleType)).all()
    # converting the result of above query to a list of dictionaries to finally convert it to json object
    spotsAsDict = []
    for spot in allSpots:
        spotDict = {
            'spotID': spot.spotID,
            'status': spot.status,
            'rowNumber': spot.rowNumber,
            'columnNumber': spot.columnNumber
        }
        spotsAsDict.append(spotDict)
    return json.dumps(spotsAsDict)

@main.route('/enter/customer/guest/<int:parkingLotID>/<int:floorNumber>/<int:entryNumber>/<int:spotID>', methods=['POST'])
def makeCustomerEntryAsGuest(parkingLotID, spotID, floorNumber, entryNumber):
    request_body = request.json
    ticketNumber = generateTicketNumber()
    inTime = datetime.datetime.utcnow()
    customerID = generateCustomerID()
    vehcileID = generateVehicleID()
    # add customer info
    customerObj = Customer(customerID = customerID,
                           vehicleID = vehicleID,
                           firstName = request_body['firstName'],
                           middleName = request_body['middleName'] if 'middleName' in request_body.keys() else "",
                           lastName = request_body['lastName'],
                           contactNumber = request_body['contactNumber'],
                           ticketNumber = ticketNumber)
    db.session.add(customerObj)
    # add ticket info
    ticket = Ticket(ticketNumber = ticketNumber,
                    customerID = customerID,
                    vehicleNumber = request_body['vehicleNumber'],
                    parkingAttendantID = None,
                    inTime = inTime,
                    outTime = None,
                    isPaid = False,
                    spotID = spotID)
    db.session.add(ticket)
    # add vehicle info
    vehicle = Vehicle(vehicleID = vehicleID,
                      vehicleNumber = request_body['vehicleNumber'],
                      ticketNumber = ticketNumber,
                      customerID = customerID,
                      vehicleType =  request_body['vehicleType'])
    db.session.add(vehicle)
    # update free spot
    db.session.query(ParkingSpot).filter(and_(ParkingSpot.spotID == spotID,
                                              ParkingSpot.parkingLotID == parkingLotID,
                                              ParkingSpot.floorNumber == floorNumber,
                                              ParkingSpot.spotType == request_body['vehicleType'])).update({'status': True})
    # add vehicle info in log table
    logger = VehicleLog(vehicleNumber = request_body['vehicleNumber'],
                        inTime = inTime,
                        entryPoint = entryNumber,
                        vehicleType = request_body['vehicleType'],
                        spotID = spotID,
                        parkingLotID = parkingLotID,
                        floorNumber = floorNumber)
    db.session.add(logger)
    # updating entry point vehicle count
    entryPoint = EntryPoint.query.filter(and_(EntryPoint.id == entryNumber,
                                                 EntryPoint.floorNumber == floorNumber,
                                                 EntryPoint.parkingLotID == parkingLotID)).first()
    entryPoint.vehicleCount += 1
    db.session.commit()
    return jsonify({'status': 200,
                    'ticket': {
                                'ticketNumber': ticketNumber,
                                'customerId': customerID,
                                'vehicleNumber': request_body['vehicleNumber'],
                                'inTime': inTime
                              }
                    }
                   )

@main.route('/isPaid/vehicleNumber/<string:vehicleNumber>', methods=['GET'])
def isPaidThroughVehicleNumber(vehicleNumber):
    ticket = Ticket.query.filter(Ticket.vehicleNumber == vehicleNumber).order_by(Ticket.inTime.desc()).first()
    return jsonify({'status': 200, 'isPaid': ticket.isPaid})

@main.route('/isPaid/ticketNumber/<string:ticketNumber>', methods=['GET'])
def isPaidThroughTicketNumber(ticketNumber):
    ticket = Ticket.query.filter_by(ticketNumber = ticketNumber).first()
    return jsonify({'status': 200, 'isPaid': ticket.isPaid})

@main.route('/pay', methods=['POST'])
def checkOutTicket():
    requestBody = request.json
    ticketNumber = requestBody['ticketNumber']
    amount = requestBody['amount']
    mode = requestBody['mode']
    checkTime = requestBody['checkTime']
    # getting ticket object for given ticket number
    ticket = Ticket.query.get(ticketNumber)
    ticket.checkTime = checkTime
    if ticket.isPaid == True:
        return jsonify({'status': 200, 'message': 'Ticket already paid'})
    # updating paid status of ticket
    ticket.isPaid = True
    db.session.commit()
    return jsonify({'status': 200, 
                    'message': 'Ticket paid successfully'})

@main.route('/electricUseStart/<string:ticketNumber>', methods = ['POST'])
def startCharging(ticketNumber):
    connectTime = datetime.datetime.utcnow()
    ticket = Ticket.query.get(ticketNumber)
    logger = VehicleLog.query.filter(and_(VehicleLog.vehicleNumber == ticket.vehicleNumber,
                                          VehicleLog.inTime == ticket.inTime)).first()
    # create an entry in last connection table
    connection = LastConnection(floorNumber = logger.floorNumber,
                                parkingLotID = logger.parkingLotID,
                                spotID = logger.spotID,
                                connect = connectTime,      
                                ticketNumber = ticketNumber)
    db.session.add(connection)
    # charging panel add
    panel = ChargingPanel(spotID = logger.spotID,
                          floorNumber = logger.floorNumber,
                          parkingLotID = logger.parkingLotID,
                          lastConnectionID = connection.id,
                          ticketNumber = ticketNumber,
                          vehicleNumber = ticket.vehicleNumber)
    db.session.add(panel)
    db.session.commit()
    return jsonify({'status': 200, 'message': 'Your vehicle is now charging'})

@main.route('/electricUseStop/<string:ticketNumber>', methods = ['POST'])
def stopCharging(ticketNumber):
    disconnectTime = datetime.datetime.utcnow()
    connection = LastConnection.query.filter(and_(LastConnection.ticketNumber == ticketNumber,
                                                  LastConnection.disconnect == None)).first()
    connection.disconnect = disconnectTime
    # calculating duration of charging in hours
    duration = math.ceil((disconnectTime - connection.connect).total_seconds()/3600)
    db.session.commit()
    return jsonify({'status': 200, 
                    'message': 'Your vehicle is now disconnected',
                    'duration': duration})

@main.route('/register', methods = ['GET','POST'])
def registerCustomer():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
    # check for exisiting contact number 
    customer = Customer.query.filter(and_(Customer.contactNumber == requestBody['contactNumber'], Customer.password is not None)).first()    
    if customer:
        raise DatabaseException('Account already exists. Please login')
    # hashing password
    hashedPassword = bcrypt.generate_password_hash(requestBody['password']).decode('utf-8')
    customerID = generateCustomerID()
    vehicleID = generateVehicleID()
    customer = Customer(customerID = customerID,
                        vehicleID = vehicleID,
                        password = hashedPassword,                     
                        firstName = requestBody['firstName'],
                        middleName = requestBody['middleName'],
                        lastName = requestBody['lastName'],                  
                        contactNumber = requestBody['ContactNumber'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'status' : 200,
                    'customerID': customerID,
                    'vehicleID': vehicleID,
                    'message': 'You have been successfully registered as customer'})

@main.route('/login', methods = ['GET', 'POST'])
def loginCustomer():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
    customer = Customer.query.filter(and_(Customer.contactNumber == requestBody['contactNumber'], Customer.password is not None)).first()
    if customer and bcrypt.check_password_hash(admin.password, requestBody['password']):
        login_user(customer)
        return jsonify({'status': 200, 
                        'message': 'Login successful'})
    else:
        return jsonify({'status': ,
                        'message': 'Login unsuccessful. Please try again'})

@main.route('/logout')
def logoutCustomer():
    logout_user()
    return jsonify({'status': 200,
                    'message': 'You have succesfully logged out'})


@main.route('/enter/customer/login/<int:parkingLotID>/<int:floorNumber>/<int:entryNumber>/<int:spotID>', methods=['POST'])
@login_required
def makeCustomerEntryAsLogin(parkingLotID, spotID, floorNumber, entryNumber):
    if current_user.is_authenticated is False:
        raise DatabaseException("Login required")
    customerID = current_user.get_id()
    request_body = request.json
    ticketNumber = generateTicketNumber()
    inTime = datetime.datetime.utcnow()
    customer = Customer.query.get(customerID)
    # add ticket number to customer object
    customer.ticketNumber = ticketNumber
    # add ticket info
    ticket = Ticket(ticketNumber = ticketNumber,
                    customerID = customerID,
                    vehicleNumber = request_body['vehicleNumber'],
                    parkingAttendantID = None,
                    inTime = inTime,
                    outTime = None,
                    isPaid = False,
                    spotID = spotID)
    db.session.add(ticket)
    # add vehicle info
    vehicle = Vehicle(vehicleID = customer.vehicleID,
                      vehicleNumber = request_body['vehicleNumber']
                      ticketNumber = ticketNumber,
                      customerID = customerID,
                      vehicleType =  request_body['vehicleType'])
    db.session.add(vehicle)
    # update free spot
    db.session.query(ParkingSpot).filter(and_(ParkingSpot.spotID == spotID,
                                              ParkingSpot.parkingLotID == parkingLotID,
                                              ParkingSpot.floorNumber == floorNumber,
                                              ParkingSpot.spotType == request_body['vehicleType'])).update({'status': True})
    # add vehicle info in log table
    logger = VehicleLog(vehicleNumber = request_body['vehicleNumber'],
                        inTime = inTime,
                        entryPoint = entryNumber,
                        vehicleType = request_body['vehicleType'],
                        spotID = spotID,
                        parkingLotID = parkingLotID,
                        floorNumber = floorNumber)
    db.session.add(logger)
    # updating entry point vehicle count
    entryPoint = EntryPoint.query.filter(and_(EntryPoint.id == entryNumber,
                                                 EntryPoint.floorNumber == floorNumber,
                                                 EntryPoint.parkingLotID == parkingLotID)).first()
    entryPoint.vehicleCount += 1
    db.session.commit()
    return jsonify({'status': 200,
                    'ticket': {
                                'ticketNumber': ticketNumber,
                                'customerId': customerID,
                                'vehicleNumber': request_body['vehicleNumber'],
                                'inTime': inTime
                              }
                    }
                   )
