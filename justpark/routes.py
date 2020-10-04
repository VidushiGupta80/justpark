from justpark import app, db
from time import time
from flask import jsonify, request
from justpark.models import Customer, Ticket
from justpark.log import VehicleLog
from justpark.utils import generateTicketNumber, generateCustomerId
from justpark.exceptions import DatabaseException
import datetime

@app.route('/ispaid/<string:ticketNumber>', methods=['GET'])
def isPaid(ticketNumber):
    ticketPaid = True if time()%10 < 5 else False
    return jsonify({'status': 200, 'isPaid': ticketPaid})

@app.route('/getfreespots/<int:parkingLoyID>/<int:floorNumber>/<string:vehicleType>', methods=['GET'])
def getFreeSpots(parkingLotID, floorNumber, vehicleType):
    allSpots = ParkingSpot.query.filter_by(and_(ParkingSpot.parkingLotID = parkingLotID, ParkingSpot.floorNumber = floorNumber, ParkingSpot.spotType = vehicleType)).all()
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

@app.route('/enter/customer/<int:parkingLotID>/<int:floorNumber>/<int:entryNumber>/<int:spotID>', methods=['POST'])
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
                           address = request_body['address'],
                           city = request_body['city'],
                           state = request_body['state'],
                           country = request_body['country'],
                           pincode = request_body['pincode'],
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
                    chargingFee = None)
    db.session.add(ticket)
    # add vehicle info
    vehicle = Vehicle(vehicleNumber = customerObj.vehicleNumber,
                      ticketNumber = ticketNumber,
                      customerID = customerObj.customerID,
                      vehicleType =  request_body['vehicleType'])
    db.session.add(vehicle)
    # update free spot
    spot = ParkingSpot.query.get(spotID = spotID, parkingLotID = parkingLotID, floorNumber = floorNumber, spotType = request_body['vehicleType'])
    spot.status = True
    # add vehicle info in log table
    logger = VeicleLog(vehicleNumber = customerObj.vehicleNumber,
                    inTime = inTime,
                    entryPoint = entryNumber,
                    vehicleType = request_body['vehicleType'],
                    spotID = spotID,
                    parkingLotID = parkingLotID,
                    floorNumber = floorNumber)
    db.session.add(logger)
    db.session.commit()
    return jsonify({'status': 200, 'ticket': {
                        'ticketNumber': ticket.ticketNumber,
                        'customerId': ticket.customerID,
                        'vehicleNumber': ticket.vehicleNumber,
                        'inTime': inTime
                        }})
                        