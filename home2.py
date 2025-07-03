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


app = Flask(__name__)

app.secret_key = 'your_secret_key'#secre_key


def init_accounts_db(app):
#MySQL database connections
    app.config['MYSQL_HOST'] = 'localhost'#MySQL Host
    app.config['MYSQL_USER'] = 'root'#MySQL User
    app.config['MYSQL_PASSWORD'] = 'Ilikeflowers7*'  #MySQL password 
    app.config['MYSQL_DB'] = 'accounts' #MySQL database


#used for the connecting of images uploaded by user for profile image function
upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}

#app.configuration defined path used for an upload folder
app.config['UPLOAD'] = upload_folder

init_accounts_db(app)
init_products_db(app)

#initial home route - home page (1)
@app.route('/')

#MySQL database connection
@app.route('/products')
def products():
	#try/except error check 
    try:
		#
        conn = MySQLdb.connect(
            host='localhost',
            user='FTael',
            passwd='Ilovemango7',
            db='products'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('products_1.html', products=rows)
    except Exception as e:
        print("Error while loading products:", e)
        return "Error loading products", 500

		
@app.route('/add', methods=['POST'])
def add_product_to_cart():
	conn = None
	cursor = None
	try:
		_quantity = int(request.form['quantity'])
		_code = request.form['code']
		# validate the received values
		if _quantity and _code and request.method == 'POST':
			#MySQL database connection
			conn = mysql_products.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			#MySQL query connection with the products table
			cursor.execute("SELECT * FROM products WHERE code=%s", _code)
			row = cursor.fetchone()
			
			itemArray = { row['code'] : {
				'name' : row['name'], 
				'code' : row['code'],
				'price' : row['price'], 
				'image' : row['image'], 
				'total_price': _quantity * row['price']}}
			#check the amount of items
			print("Cart Items:", session['cart_item'])

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
							session['cart_item'][key]['total_price'] = total_quantity * row['price']
				else:
					session['cart_item'] = array_merge(session['cart_item'], itemArray)

				for key, value in session['cart_item'].items():
					individual_quantity = int(session['cart_item'][key]['quantity'])
					individual_price = float(session['cart_item'][key]['total_price'])
					all_total_quantity = all_total_quantity + individual_quantity
					all_total_price = all_total_price + individual_price
			else:
				session['cart_item'] = itemArray
				all_total_quantity = all_total_quantity + _quantity
				all_total_price = all_total_price + _quantity * row['price']
			
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
			
			return render_template('products_1.html', products=products, cart_item=session.get('cart_item'))
		else:			
			return 'Error while adding item to cart'
	except Exception as e:
		print(e)
		return f"Error while adding item to cart: {str(e)}"
	finally:
		if cursor is not None: 
			cursor.close() 
		if conn is not None:
			conn.close()
		

@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.clear()
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		
		#return redirect('/')
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		

if __name__ == '__main__':
    app.run(debug=True)