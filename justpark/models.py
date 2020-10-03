from justpark import db

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
    floorNumber = db.Column(db.Integer, primary_key = True)
    vehicleCount = db.Column(db.Integer, nullable = False)    
    displayID = db.Column(db.Integer, db.ForeignKey("displayBoard.id"), nullable = False)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)

class EntryPoint(db.Model):
    __tablename__ = "entryPoint"
    id = db.Column(db.Integer, primary_key = True)
    floorNumber = db.Column(db.Integer, primary_key = True)
    vehicleCount = db.Column(db.Integer, nullable = False)
    displayID = db.Column(db.Integer, db.ForeignKey("displayBoard.id"), nullable = False)    
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)

class Customer(db.Model):
    __tablename__ = "customer"
    customerID = db.Column(db.String, primary_key = True)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    vehicleType = db.Column(db.String, nullable = False)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.ticketNumber"), nullable = False)   
    firstName = db.Column(db.String, nullable = False)
    middleName = db.Column(db.String, nullable = True)
    lastName = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state  = db.Column(db.String, nullable = False)
    country = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    contactNumber = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        idLine = "Customer ID: %s" % (self.customerID)
        nameLine = "First Name: %s, Middle Name: %s, Last Name: %s" % (self.firstName, self.middleName, self.lastName)
        address = "Address: %s, City: %s, State: %s, Country: %s, Pincode: %s" % (self.address, self.city, self.state, self.country, self.pincode)
        contactNumber = "Contact Number: %s" % (self.contactNumber)
        vehicleInfo = "Vehicle Number: %s, Vehicle Type: %s, ticketNumber: %s" % (self.vehicleNumber, self.vehicleType, self.ticketNumber)
        return '\n'.join([idLine, nameLine, address, contactNumber, vehicleInfo])

class Admin(db.Model):
    __tablename__ = "admin"
    adminID = db.Column(db.Integer, autoincrement = True, primary_key = True)
    password = db.Column(db.String, nullable = False)
    emailID = db.Column(db.String, nullable = False)
    salary = db.Column(db.Integer, nullable = False)
   
    firstName = db.Column(db.String, nullable = False)
    middleName = db.Column(db.String, nullable = True)
    lastName = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state  = db.Column(db.String, nullable = False)
    country = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    contactNumber = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        idLine = "Admin ID: %s" % (self.adminID)
        nameLine = "First Name: %s, Middle Name: %s, Last Name: %s" % (self.firstName, self.middleName, self.lastName)
        address = "Address: %s, City: %s, State: %s, Country: %s, Pincode: %s" % (self.address, self.city, self.state, self.country, self.pincode)
        contactNumber = "Contact Number: %s" % (self.contactNumber)
        adminInfo = "Password: password thodi dikha denge :), emailId: %s, salary: %s" % (self.emailID, self.salary)
        return '\n'.join([idLine, nameLine, address, contactNumber, adminInfo])

class ParkingAttendant(db.Model):
    __tablename__ = "parkingAttendant"
    parkingAttendantId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    joiningDate = db.Column(db.DateTime, nullable = False)
    leavingDate = db.Column(db.DateTime, nullable = True)
    floor = db.Column(db.Integer, nullable = False)
    emailID = db.Column(db.String, nullable = False)
    salary = db.Column(db.Integer, nullable = False)
    firstName = db.Column(db.String, nullable = False)
    middleName = db.Column(db.String, nullable = True)
    lastName = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    state  = db.Column(db.String, nullable = False)
    country = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    contactNumber = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        idLine = "Parking Attendant ID: %s" % (self.parkingAttendantId)
        nameLine = "First Name: %s, Middle Name: %s, Last Name: %s" % (self.firstName, self.middleName, self.lastName)
        address = "Address: %s, City: %s, State: %s, Country: %s, Pincode: %s" % (self.address, self.city, self.state, self.country, self.pincode)
        contactNumber = "Contact Number: %s" % (self.contactNumber)
        paInfo = "Joining Date: %s, Leaving Date: %s, Stationed At: %s, EmailId: %s, Salary: %s" % (self.joiningDate, self.leavingDate, self.floor, self.emailID, self.salary)
        return '\n'.join([idLine, nameLine, address, contactNumber, paInfo])

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    vehicleNumber = db.Column(db.String, primary_key = True)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.ticketNumber"), nullable = False)
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"), nullable = False)
    vehicleType = db.Column(db.String, nullable = False)

class Ticket(db.Model):
    __tablename__ = "ticket"
    ticketNumber = db.Column(db.String, primary_key = True)
    customerID = db.Column(db.Integer, db.ForeignKey("customer.customerID"), nullable = False)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = False)
    parkingAttendantID = db.Column(db.Integer, db.ForeignKey("parkingAttendant.parkingAttendantId"), nullable = True)
    inTime = db.Column(db.DateTime, nullable = False)
    outTime = db.Column(db.DateTime, nullable = True)
    chargingFee = db.Column(db.Integer, nullable = True)

class ChargingPanel(db.Model):
    __tablename__ = "chargingPanel"
    spotID = db.Column(db.Integer, primary_key = True)
    floorNumber = db.Column(db.Integer, primary_key = True)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)
    rate = db.Column(db.Integer, nullable = False)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.ticketNumber"), nullable = True)
    vehicleNumber = db.Column(db.String, db.ForeignKey("vehicle.vehicleNumber"), nullable = True)
    lastConnectionID = db.Column(db.Integer, db.ForeignKey("lastConnection.id"),  primary_key = True)

class LastConnection(db.Model):
    __tablename__ = "lastConnection"
    id = db.Column(db.Integer, primary_key = True)
    floorNumber = db.Column(db.Integer, primary_key = True)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)
    connect = db.Column(db.DateTime, nullable = False)
    disconnect = db.Column(db.DateTime, nullable = True)
    spotID = db.Column(db.Integer, db.ForeignKey("chargingPanel.spotID"), primary_key = True)
    ticketNumber = db.Column(db.String, db.ForeignKey("ticket.ticketNumber"), nullable = False)

class DisplayBoard(db.Model):
    __tablename__ = "displayBoard"
    id = db.Column(db.Integer, primary_key = True)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)
    floorNumber = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String, nullable = True)
    userID = db.Column(db.Integer, db.ForeignKey("parkingAttendant.parkingAttendantId"), nullable = True)
    timeStamp = db.Column(db.DateTime, nullable = True)
    entryPointID = db.Column(db.Integer, db.ForeignKey("entryPoint.id"), nullable = True)
    exitPointID = db.Column(db.Integer, db.ForeignKey("exitPoint.id"), nullable = True)

class ParkingSpot(db.Model):
    __tablename__ = "parkingSpot"
    spotID = db.Column(db.Integer, primary_key = True)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True)
    floorNumber = db.Column(db.Integer, primary_key = True)
    spotType = db.Column(db.String, primary_key = True)
    status = db.Column(db.Boolean, nullable = False)
    rowNumber = db.Column(db.Integer, nullable = False)
    columnNumber = db.Column(db.Integer, nullable = False)

class Capacity(db.Model):
    __tablename__ = "capacity"
    floorNumber = db.Column(db.Integer, primary_key = True)
    totalFloors = db.Column(db.Integer, nullable = False)
    parkingLotID = db.Column(db.Integer, db.ForeignKey("parkingLot.id"), primary_key = True, nullable = False)    
    carSpots = db.Column(db.Integer, nullable = False)
    bikeSpots = db.Column(db.Integer, nullable = False)
    TruckSpots = db.Column(db.Integer, nullable = False)
    electricCarSpots = db.Column(db.Integer, nullable = False)



