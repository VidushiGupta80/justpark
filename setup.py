from justpark import db
from justpark.models import *
from justpark.log import *
import csv

def main():
    # Since all models are imported, create table for all models
    db.create_all()
    parkingLotInitFile = open("data/startingParkingLot.csv")
    parkingLotReader = csv.reader(parkingLotInitFile)
    for index, line in enumerate(parkingLotReader):
        # Skipping the first header line from the csv, doing the same everywhere
        # Factory methodology can be used here since there is code repetition
        # Not forcing here in favor of saving time
        if index == 0: continue
        id, city, state, country, pincode = line
        parkingLot = ParkingLot(id = id,
                                city = city,
                                state  = state,
                                country = country,
                                pincode = pincode)
        db.session.add(parkingLot)

    capacityInitFile = open("data/startingCapacity.csv")
    capacityReader = csv.reader(capacityInitFile)
    for index, line in enumerate(capacityReader):
        if index == 0: continue
        floorNumber, totalFloors, parkingLotID, carSpots, bikeSpots, truckSpots, electricCarSpots = line
        capacity = Capacity(floorNumber = floorNumber,
                            totalFloors = totalFloors,
                            parkingLotID =   parkingLotID,
                            carSpots = carSpots,
                            bikeSpots = bikeSpots,
                            truckSpots = truckSpots,
                            electricCarSpots = electricCarSpots)
        db.session.add(capacity)

    parkingSpotsInitFile = open("data/startingParkingSpots.csv")
    parkingSpotsReader = csv.reader(parkingSpotsInitFile)
    for index, line in enumerate(parkingSpotsReader):
        if index == 0: continue
        spotID, parkingLotID, floorNumber, spotType, status, rowNumber, columnNumber = line
        parkingSpot = ParkingSpot(spotID = spotID,
                                  parkingLotID = parkingLotID,
                                  floorNumber = floorNumber,
                                  spotType = spotType,
                                  status = True if status.lower() == 'true' else False,
                                  rowNumber = rowNumber,
                                  columnNumber = columnNumber)
        db.session.add(parkingSpot)
        
    entryPointsInitFile = open("data/startingEntryPoints.csv")
    entryPointsReader = csv.reader(entryPointsInitFile)
    for index, line in enumerate(entryPointsReader):
        if index == 0: continue
        id, floorNumber, vehicleCount, displayID, parkingLotID = line
        entryPoint = EntryPoint(id = id,
                                floorNumber = floorNumber,
                                vehicleCount = vehicleCount,
                                displayID = displayID,
                                parkingLotID = parkingLotID)
        db.session.add(entryPoint)

    exitPointsInitFile = open("data/startingExitPoints.csv")
    exitPointsReader = csv.reader(exitPointsInitFile)
    for index, line in enumerate(exitPointsReader):
        if index == 0: continue
        id, floorNumber, vehicleCount, displayID, parkingLotID = line
        exitPoint = ExitPoint(id = id,
                                floorNumber = floorNumber,
                                vehicleCount = vehicleCount,
                                displayID = displayID,
                                parkingLotID = parkingLotID)
        db.session.add(exitPoint)

    displayBoardInitFile = open("data/startingDisplayBoard.csv")
    displayBoardReader = csv.reader(displayBoardInitFile)
    for index, line in enumerate(displayBoardReader):
        if index == 0: continue
        id, parkingLotID, floorNumber, message, userID, timeStamp, entryPointID, exitPointID = line
        displayBoard = DisplayBoard(id = id,
                                    parkingLotID = parkingLotID,
                                    floorNumber = floorNumber,
                                    message = None if message.lower() == 'none' else message,
                                    userID = None if userID.lower() == 'none' else userID,
                                    timeStamp = None if timeStamp.lower() == 'none' else timeStamp,
                                    entryPointID = None if entryPointID.lower() == 'none' else entryPointID,
                                    exitPointID = None if exitPointID.lower() == 'none' else exitPointID)
        db.session.add(displayBoard)

    ratesInitFile = open("data/startingRate.csv")
    ratesReader = csv.reader(ratesInitFile)
    for index, line in enumerate(ratesReader):
        if index == 0: continue
        vehicleType, parkingRate = line
        addRate = Rate(vehicleType = vehicleType,
                       parkingRate = parkingRate)
        db.session.add(addRate)

    chargingRateInitFile = open("data/startingChargingRate.csv")
    chargingRateReader = csv.reader(chargingRateInitFile)
    for index, line in enumerate(chargingRateReader):
        if index == 0: continue
        vehicleType, rate = line
        addRate = ChargingRate(vehicleType = vehicleType,
                               rate = rate)
        db.session.add(addRate)    
    db.session.commit()

if __name__ == '__main__':
    main()
