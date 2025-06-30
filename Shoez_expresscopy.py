from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os #libary used to import the Operating system - Upload image file for user
import psycopg2#database connection - postgreSQL
import pymysql#library to allow the usage of mysql 

#ERROR HERE 
from db_config import mysql #connection between db_config and msql
#ERROR HERE ^ 

#from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ShoezExpress"

#used for the connecting of images uploaded by user for profile image function
upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}


app.config['UPLOAD'] = upload_folder

#MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ilikeflowers7*'  # Enter your MySql password 
app.config['MYSQL_DB'] = 'accounts'

mysql = MySQL(app)

#home page
@app.route('/')
def home(): 
    return render_template('home.html')

#add product to cart link 
@app.route('/add', methods=['POST'])
def add_product_to_cart(): 
    cursor = None 
    try: 
        _quantity = int(request.form['quantity'])#quantity of the product (user-choice)
        _code = request.form['code']#code for product 
        #validation for the received values 
        if _quantity and _code and request.method == 'POST': 
            conn = mysql.connect() 
            cursor = conn.cursor(pymsql.cursors.DictCursor)
            cursor.execute("SELECT * FROM product WHERE code=%s, _code")
            row = cursor.fetchone() 

            itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price':_quantity * row['price']}}

            #total price intial start 
            all_total_price = 0
            all_total_quantity = 0

            session.modified = True 
            if 'cart_item' in session: 
                if row['code'] in session['cart_item']: 
                    for key, value in session['cart_item'].items(): 
                     if row['code'] == key: 
                        #session.modified = True 
                        #if session['cart_item'][key]['quantity'] is not None:
							#	session['cart_item'][key]['quantity'] = 0
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity 
                        session['cart_item'][key]['quantity'] = total_quantity 
                        session['cart_iem'][key]['total_price'] = total_quantity * row['price']
                else: 
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)
                    
                for key, value in session['cart_item'].items(): 
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity 
                    all_total_price = all_total_price + individual_price 
            else: 
                session['cart_item'] = itemArray 
            all_total_quantity - all_total_quantity + _quantity
            all_total_price = all_total_price + _quantity * row['price']

            session['all_total_quantity'] = all_total_quantity 
            session['all_total_price'] = all_total_price

            return redirect(url_for('.products'))
        else: 
            return 'Error while trying to add item to Cart'
    except Exception as e: 
        print(e)
    finally: 
        cursor.close()
        conn.close() 

#empty cart page 
@app.route('/empty')
def empty_cart(): 
    try: 
        session.clear() 
        return redirect(url_for('.products'))
    except Exception as e: 
        print(e)

#delete product inside cart 
@app.route('/delete/<string:code>')
def delete_product(code): 
    try: 
        all_total_price = 0
        all_total_quantity = 0 
        session.modified = True 

        for item in session['cart_item'].items(): 
            if item[0] == code: 
                session['cart_item'].pop(item[0], None)
                if 'cart_itm' in session: 
                    for key, value in session['cart_item'].items(): 
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity 
                        all_total_pric = all_total_price + individual_price 
                break

        if all_total_quantity == 0: 
            session.clear() 
        else: 
            session['all_total_quantity'] = all_total_quantity 
            session['all_total_price'] = all_total_price 

        return redirect(url_for('.products'))
    except Exception as e: 
        print(e)

def array_merge( first_array, second_array ):
    if isintance( first_array, list ) and isintance( second_array, list ):
        return first_array + second_array
    elif isintance( first_array, dict) and isintance( second_array, dict ):
        return dict( list( first_array.items()) + list( second_array.items() ) )
    elif isinstance( first_array, set ) and isintance( second_array, set ):
        return first_array.union ( second_array )
        return False 

#contact page
@app.route('/contact_us', methods=['GET','POST'])
def contact_us(): 
    #collect user input from form 
    if request.method == "POST": 
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        #insert data into postgreSQL database
        cur2.execute('INSERT INTO contact (name, email, message) ' 
                    'VALUES(%s, %s, %s)',
                    (name, email, message)
        )

        #commit changes to database
        conn2.commit()
        #redirect user to another page
        return redirect(url_for('confirm_mess', name=name, email=email, message=message))
        
    cur2.execute("SELECT * FROM contact")
    print(cur2.fetchall())

    return render_template('contact_us.html')

#display name and message! 
@app.route('/confirm_mess')
def confirm_mess(): 
    cur = conn2.cursor()
    cur.execute("SELECT * FROM contact")
    rows = cur.fetchall()
    return render_template('Confirm_mess.html', contact=rows)

#Sign-Up route page
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    #Collect user input from form 
    if request.method == 'POST': 
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Username: {username}, Email: {email}, Password: {password}")

        #insert data into postgreSQL database
        cur1.execute('INSERT INTO users (username, email, password) ' 
                    'VALUES(%s, %s, %s)',
                    (username, email, password)
        )
        
        #commit changes
        conn1.commit()
        #redirect user to profile page 
        return redirect(url_for('profile1', username=username))

    cur1.execute("SELECT * FROM users")
    print(cur1.fetchall())

    return render_template('sign-up 1_1.html')

#Registered Users
@app.route('/Users')
def Users():
    cur = conn1.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return render_template("Users.html", users=rows)

#Future Implementation!
#Sign-in route page
@app.route('/sign_in',methods=['GET','POST'])
def sign_in(): 
    msg=''#default message variable to use
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s',(username, password))
        account = cursor.fetchone()
        if account: 
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_Template('profile3.html',msg='Logged in Successfully!')
        else:
            msg='Incorrect username/password!'
    return render_template('sign-in 1 1.html')

@app.route('/sign-out')
def logout(): 
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('sign_in'))

@app.route('/sign_up',methods=['GET','POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE ')
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

#Products Page 
@app.route('/products', methods=['GET','POST'])
def products(): 
    return render_template('products1.html')

# Cart route page
@app.route('/cart')
def cart(): 
    return render_template('Cart.html')

#Payment page
@app.route('/Payment')
def Payment(): 
    return render_template('Payment.html')


if __name__ == '__main__':
    app.run(debug=True)