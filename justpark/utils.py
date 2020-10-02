from random import randint

def generateTicketNumber():
    return str('T' + ''.join([str(randint(0, 9)) for i in range(0, 21)]))

def generateCustomerId():
    return str('C' + ''.join([str(randint(0, 9)) for i in range(0, 21)]))