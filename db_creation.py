from justpark import db
from justpark.models import *
import csv
db.create_all()
parkingLot = ParkingLot(id = 1,
                       city = chandigarh,
                       state  = chandigarh,
                       country = India,
                       pincode = 160047)
db.session.add(parkinglot)
def main():
    c = open("startingCapacity.csv")
    c_reader = csv.reader(c)
    for floorNumber, totalFloors, parkingLotID, carSpots, bikeSpots, heavyWeightSpots, electricCarSpots in c_reader:
        capacity = Capacity(floorNumber = floorNumber,
                            totalFloors = totalFloors,
                            parkingLotID =   parkingLotID,
                            carSpots = carSpots,
                            bikeSpots = bikeSpots,
                            heavyWeightSpots = heavyWeightSpots,
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
 db.session.commit()