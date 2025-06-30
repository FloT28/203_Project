#MySQL database connection 
from flask_mysqldb import MySQL 
from Shoez_expresscopy import app 

mysql = MySQL() 

#MySQL Configurations 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ilikeflowers7*'
app.config['MYSQL_DATABASE_DB'] = 'roytuts'
app.config['MYSQL_DATABSE_HOST'] = 'localhost'
mysql.init_app(app)