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

@app.route('/enter/customer/<int:parkingLotID>/<int:floorNumber>/<int:entryNumber>/<int:spotID>', methods=['POST'])
def makeCustomerEntry(floorNumber, entryNumber):
    request_body = request.json
    ticketNumber = generateTicketNumber()
    inTime = datetime.datetime.utcnow()
    customerID = generateCustomerId()
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
    ticket = Ticket(ticketNumber = ticketNumber,
                    customerID = customerObj.customerID,
                    vehicleNumber = customerObj.vehicleNumber,
                    parkingAttendantID = None,
                    inTime = inTime,
                    outTime = None,
                    chargingFee = None)
    db.session.add(ticket)
    vehicle = Vehicle(vehicleNumber = customerObj.vehicleNumber,
                      ticketNumber = ticketNumber,
                      customerID = customerObj.customerID,
                      vehicleType =  request_body['vehicleType'])
    db.session.add(vehicle)
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