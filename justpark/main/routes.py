from flask import Blueprint
from justpark import app, db, bcrypt
from time import time
from flask import jsonify, request
from sqlalchemy import and_
from justpark.models import *
from justpark.log import VehicleLog
from justpark.utils import generateTicketNumber, generateCustomerId
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
    vehicleInfo = Vehicle.query.get(vehicleNumber)
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
                    'totalParkingHours': timeDurationHours,
                    'totalChargingHours': chargingHours, 
                    'parkingFee': parkingFee, 
                    'chargingFee': chargingFee,
                    'totalAmount': parkingFee + chargingFee})

@main.route('/getAmount/vehicleNumber/<string:vehicleNumber>', methods=['GET'])
def getAmountVehicle(vehicleNumber):
    # getting vehicle object for the gien vehicle number
    vehicleInfo = Vehicle.query.get(vehicleNumber)
    if vehicleInfo is None:
        raise DatabaseException("This vehicle is not inside this parking lot")
    # getting ticket object for the given vehicle number
    ticket = Ticket.query.filter_by(vehicleNumber = vehicleNumber).first()
    # time of checking the amount of ticket
    checkTime = datetime.datetime.utcnow()
    timeDuration = checkTime - ticket.inTime
    # converting total time duration in hours from seconds
    timeDurationHours = math.ceil(timeDuration.total_seconds() / 3600)
    vehicleType = vehicleInfo.vehicleType
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
                    'totalParkingHours': timeDurationHours,
                    'totalChargingHours': chargingHours, 
                    'parkingFee': parkingFee, 
                    'chargingFee': chargingFee,
                    'totalAmount': parkingFee + chargingFee})


@main.route('/getFreeSpots/<int:parkingLotID>/<int:floorNumber>/<string:vehicleType>', methods=['GET'])
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

@main.route('/enter/customer/<int:parkingLotID>/<int:floorNumber>/<int:entryNumber>/<int:spotID>', methods=['POST'])
def makeCustomerEntry(parkingLotID, spotID, floorNumber, entryNumber):
    request_body = request.json
    ticketNumber = generateTicketNumber()
    inTime = datetime.datetime.utcnow()
    customerID = generateCustomerId()
    # add customer info
    customerObj = Customer(customerID = customerID,
                           firstName = request_body['firstName'],
                           middleName = request_body['middleName'] if 'middleName' in request_body.keys() else "",
                           lastName = request_body['lastName'],
                           contactNumber = request_body['contactNumber'],
                           vehicleNumber = request_body['vehicleNumber'],
                           vehicleType = request_body['vehicleType'],
                           ticketNumber = ticketNumber)
    db.session.add(customerObj)
    # add ticket info
    ticket = Ticket(ticketNumber = ticketNumber,
                    customerID = customerObj.customerID,
                    vehicleNumber = customerObj.vehicleNumber,
                    parkingAttendantID = None,
                    inTime = inTime,
                    outTime = None,
                    isPaid = False,
                    spotID = spotID)
    db.session.add(ticket)
    # add vehicle info
    vehicle = Vehicle(vehicleNumber = customerObj.vehicleNumber,
                      ticketNumber = ticketNumber,
                      customerID = customerObj.customerID,
                      vehicleType =  request_body['vehicleType'])
    db.session.add(vehicle)
    # update free spot
    db.session.query(ParkingSpot).filter(and_(ParkingSpot.spotID == spotID,
                                              ParkingSpot.parkingLotID == parkingLotID,
                                              ParkingSpot.floorNumber == floorNumber,
                                              ParkingSpot.spotType == request_body['vehicleType'])).update({'status': True})
    # add vehicle info in log table
    logger = VehicleLog(vehicleNumber = customerObj.vehicleNumber,
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
                                'ticketNumber': ticket.ticketNumber,
                                'customerId': ticket.customerID,
                                'vehicleNumber': ticket.vehicleNumber,
                                'inTime': inTime
                              }
                    }
                   )

@main.route('/isPaid/vehicleNumber/<string:vehicleNumber>', methods=['GET'])
def isPaidThroughVehicleNumber(vehicleNumber):
    vehicle = Vehicle.query.filter_by(vehicleNumber = vehicleNumber).first()
    ticket = Ticket.query.filter_by(ticketNumber = vehicle.ticketNumber).first()
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
    # getting ticket object for given ticket number
    ticket = Ticket.query.get(ticketNumber)
    if ticket.isPaid == True:
        return jsonify({'status': 200, 'isPaid': ticket.isPaid})
    # updating paid status of ticket
    ticket.isPaid = True
    db.session.commit()
    return jsonify({'status': 200, 'isPaid': ticket.isPaid})

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
