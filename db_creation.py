from justpark import db
from justpark.models import *
import csv
db.create_all()
def main():
    p = open("startingParkingLot.csv")
    p_reader = csv.reader(p)
    for id, city, state, country, pincode in p_reader:
        parkingLot = ParkingLot(id = id,
                                city = city,
                                state  = state,
                                country = country,
                                pincode = pincode)
        db.session.add(parkinglot)

    c = open("startingCapacity.csv")
    c_reader = csv.reader(c)
    for floorNumber, totalFloors, parkingLotID, carSpots, bikeSpots, truckSpots, electricCarSpots in c_reader:
        capacity = Capacity(floorNumber = floorNumber,
                            totalFloors = totalFloors,
                            parkingLotID =   parkingLotID,
                            carSpots = carSpots,
                            bikeSpots = bikeSpots,
                            truckSpots = truckSpots,
                            electricCarSpots = electricCarSpots)
        db.session.add(capacity)

    s = open("startingParkingSpots.csv")
    s_reader = csv.reader(s)
    for spotID, parkingLotID, floorNumber, spotType, status, rowNumber, columnNumber in s_reader:
        parkingSpot = ParkingSpot(spotID = spotID,
                                  parkingLotID = parkingLotID,
                                  floorNumber = floorNumber,
                                  spotType = spotType,
                                  status = status,
                                  rowNumber = rowNumber,
                                  columnNumber = columnNumber)
        db.session.add(parkingSpot)
        
    entry = open("startingEntryPoints.csv")
    entry_reader = csv.reader(entry)
    for  id, floorNumber, vehicleCount, displayID, parkingLotID in entry_reader:
        entryPoint = EntryPoint(id = id,
                                floorNumber = floorNumber,
                                vehicleCount = vehicleCount,
                                displayID = displayID,
                                parkingLotID = parkingLotID)
        db.session.add(entryPoint)

    exitt = open("startingExitPoints.csv")
    exit_reader = csv.reader(exitt)
    for id, floorNumber, vehicleCount, displayID, parkingLotID in exit_reader:
        exityPoint = ExitPoint(id = id,
                                floorNumber = floorNumber,
                                vehicleCount = vehicleCount,
                                displayID = displayID,
                                parkingLotID = parkingLotID)
        db.session.add(exitPoint)

    display = open("startingDisplayBoard.csv")
    display_reader = csv.reader(display)
    for id, parkingLotID, floorNumber, message, userID, timeStamp, entryPointID, exitPointID in display_reader:
        displayBoard = DisplayBoard(id = id,
                                    parkingLotID = parkingLotID,
                                    floorNumber = floorNumber,
                                    message = message,
                                    userID = userID,
                                    timeStamp = timeStamp,
                                    entryPointID = entryPointID,
                                    exitPointID = exitPointID)
        db.session.add(displayBoard)

    rates = open("startingRate.csv")
    rates_reader = csv.reader(rates)
    for vehicleType, parkingRates in rates_reader:
        addRate = Rate(vehicleType = vehicleType,
                       parkingRates = parkingRates)
        db.session.add(addRate)

    charging = open("startingChargingRate.csv")
    charging_reader = csv.reader(charging)
    for vehicleType, rate in charging_reader:
        addRate = ChargingRate(vehicleType = vehicleType,
                               rate = rate)
        db.session.add(addRate)    
 db.session.commit()
