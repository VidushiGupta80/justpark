from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login_multi.login_manager import LoginManager   
from justpark.config import config



app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.blueprint_login_views = {  
        'parkingAttendant':  "parkingAttendant.loginParkingAttendant",  
        'admin': "admin.loginAdmin",  
        'main': "main.loginCustomer"
    }  
from justpark.admin.routes import admin
from justpark.main.routes import main
from justpark.parkingAttendant.routes import parkingAttendant
app.register_blueprint(admin, url_prefix = "/admin")
app.register_blueprint(parkingAttendant, url_prefix = "/parkingAttendant")
app.register_blueprint(main, url_prefix = "/main")

