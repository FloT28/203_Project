from flask import Flask, render_template, request, redirect, url_for, session #library for sign-up/sign-in, messages, redirect user to new pages
from flask_mysqldb import MySQL#library to import and use mysql database into project
import MySQLdb.cursors#library used in order to create an cursor method and also an con
import re# RegEx Module - used to check an valid email address and username input is correct
        #checking the sequence of characted from an assigned search pattern
import os# operating system module - used to check 
import MySQLdb#MySQL database module - used for the connection of queries and user data with the selected MySQL database
from werkzeug.utils import secure_filename
#secure_filename is an function under werkzeug.utils module 
#used to enforce and store secure filenames before being placed into servers
import pymysql
from app import app #from app.py import app
#MySQL database configuration connection for 2 databases used accounts & products!
from db_config_accounts import mysql_accounts, init_accounts_db
from db_config_products import mysql_products, init_products_db
import MySQLdb

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'


#used for the connecting of images uploaded by user for profile image function
upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}

#app.configuration defined path used for an upload folder
app.config['UPLOAD'] = upload_folder

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ilikeflowers7*'  # Enter your MySql password 
app.config['MYSQL_DB'] = 'accounts'

mysql = MySQL(app)

@app.route('/')
def home(): 
    return render_template('home.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('profile 3.html', msg='Logged in successfully!')
        else:
            msg = 'Incorrect username/password!'
    return render_template('sign_in1.html', msg=msg)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    return render_template('sign_up1.html', msg=msg)


#Profile route page
@app.route('/profile_1', methods=['GET','POST'])
def profile(): 

    #image profile management 
    if request.method == 'POST':
        file = request.files['img']#type of file requesting
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('profile 3.html', img=img)#return to the original html page (profile)
    return render_template('profile 3.html')

#redirect user to profile page (newly created)
@app.route('/profile1')
def profile1(): 
    #collect user input (username)
    username = request.args.get('username')


    #redirect user to original main profile page (have user links in a squared section)
    return render_template('profile 3.html', username=username)

#Profile Settings Page
@app.route('/profile_settings')
def profile_settings(): 
    return render_template('profile_settings.html')

#contact us page - not working as of data being saved
@app.route('/contact_us')
def contact_us():
   return render_template('contact_us.html')

@app.route('/products')
def products(): 
   return render_template('products_1.html')

if __name__ == '__main__':
    app.run(debug=True)
