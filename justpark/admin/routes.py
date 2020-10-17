from flask import Blueprint
from justpark import app, db, bcrypt
from time import time
from flask import jsonify, request
from sqlalchemy import and_
from justpark.models import *
from justpark.log import VehicleLog
from justpark.exceptions import DatabaseException
import datetime
import json
import math
from app.libs.flask_login_multi import login_user, current_user, logout_user, login_required

admin = Blueprint("admin", __name__)

@admin.route('/register', methods = ['GET', 'POST'])
def registerAdmin():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
    # check for exisiting userID and email ID in both admin and parking attendant class
    ID = Admin.query.filter(Admin.adminID ==  requestBody['adminID'])
    if ID:
        raise DatabaseException('User ID already exists. Use different ID')
    ID = ParkingAttendant.query.filter(ParkingAttendant.parkingAttendantID ==  requestBody['adminID'])
    if ID:
        raise DatabaseException('User ID already exists. Use different ID')
    email = ParkingAttendant.query.filter(ParkingAttendant.emailID == requestBody['emailID'])
    if email:
        raise DatabaseException('Email ID already taken. Use different Email ID')
    email = Admin.query.filter(Admin.emailID == requestBody['emailID'])
    if email:
        raise DatabaseException('Email ID already taken. Use different Email ID')
    # hashing password
    hashedPassword = bcrypt.generate_password_hash(requestBody['password']).decode('utf-8')
    admin = Admin(adminID = requestBody['adminID'],
                  password = hashedPassword,
                  emailID = requestBody['emailID'],
                  salary = requestBody['salary'],   
                  firstName = requestBody['firstName'],
                  middleName = requestBody['middleName'],
                  lastName = requestBody['lastName'],
                  address = requestBody['address'],     
                  city = requestBody['city'],
                  state  = requestBody['state'],
                  country = requestBody['country'],
                  pincode = requestBody['pincode'],
                  contactNumber = requestBody['ContactNumber'])
    db.session.add(admin)
    db.session.commit()
    return jsonify({'status' : 200,
                    'message': 'You have been successfully registered as Admin'})

@admin.route('/login', methods = ['GET', 'POST'])
def loginAdmin():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'})
    requestBody = request.json
    admin = Admin.query.get(requestBody['adminID'])
    if admin and bcrypt.check_password_hash(admin.password, requestBody['password']):
        login_user(admin)
        return jsonify({'status': 200, 
                        'message': 'Login successful'})
    else:
        return jsonify({'status': ,
                        'message': 'Login unsuccessful. Please try again'})

@admin.route('/logout')
def logout():
    logout_user()
    return jsonify({'status': 200,
                    'message': 'You have succesfully logged out'})



