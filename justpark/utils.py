from random import randint

def generateTicketNumber():
    return str('T' + ''.join([str(randint(0, 9)) for i in range(0, 21)]))

def generateCustomerID():
    return str('C' + ''.join([str(randint(0, 9)) for i in range(0, 21)]))

def generateVehicleID():
    return str('V' + ''.join([str(randint(0, 9)) for i in range(0, 21)]))

    