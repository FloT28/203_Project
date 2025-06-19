from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os #libary used to import the Operating system - Upload image file for user
import psycopg2#database connection - postgreSQL 

app = Flask(__name__)
app.secret_key = "ShoezExpress"

#used for the connecting of images uploaded by user for profile image function
upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}


app.config['UPLOAD'] = upload_folder

#Database connection (2) - Users (sign-up * registered users)
def db_connection(): 
    conn = psycopg2.connect(host='localchost',
                            databse='users',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

#Database connection (2) - Contact Page
def database_connect(): 
    conn = psycopg2.connect(host='localhost',
                            database='contact',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn 

# Connect to the database
conn = psycopg2.connect(database="users", user="postgres",
                        password="flowers7*", host="localhost", port="5432")

# create a cursor
cur = conn.cursor()

# Connect to the database 2 
conn = psycopg2.connect(database="contact", user="postgres",
                        password="flowers7*", host="localhost",port="5432")

#cursor created 
cur = conn.cursor()

#TABLE CREATION - contact
@app.route('/db')
def db(): 
    try: 
        cur = conn.cursor() 
        cur.execute('''
                CREATE TABLE IF NOT EXISTS contact (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    message TEXT,)
                ''')
        conn.commit() 
        return "table created successfully!"
    except Exception as e: 
        conn.rollback() 
        return f"Error: {e}"

#TABLE CREATED - users database 
@app.route('/db2')
def db2(): 
    try:
        cur = conn.cursor() 
        cur.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    name text NOT NULL,
                    email text NOT NULL,
                    password text NOT NULL)
                ''')
        conn.commit() 
        return "table created successfully!"
    except Exception as e: 
        conn.rollback() 
        return f"Error: {e}"


@app.route('/')
def cart(): 
    return render_template('Cart.html')

@app.route('/contact_us', methods=['GET','POST'])
def contact_us(): 
    if request.method == "POST": 
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        #insert data into postgreSQL database
        cur.execute('INSERT INTO contact (name, email, message) ' 
                    'VALUES(%s, %s, %s)',
                    (name, email, message)
        )

            #commit changes
        conn.commit()
        return redirect(url_for('contact_us', name=name, email=email, message=message))
        
    cur.execute("SELECT * FROM contact")
    print(cur.fetchall())

    return render_template('contact_us.html')

#display name and message! 
@app.route('/confirm_mess')
def confirm_mess(): 
    cur = conn.cursor()
    cur.execute("SELECT * FROM contact")
    rows = cur.fetchall()
    return render_template('Confirm_mess.html', contact=rows)


#Sign-Up route page
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == "POST": 
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return "All fields are required", 400

        #insert data into postgreSQL database
        cur.execute('INSERT INTO users (name, email, password) ' 
                    'VALUES(%s, %s, %s)',
                    (name, email, password)
        )
            #commit changes
        conn.commit()
        return redirect(url_for('profile1', name=name))
    
    cur.execute("SELECT * FROM customers")
    print(cur.fetchall())

    return render_template('sign-up 1_1.html')

#Sign-in route page
@app.route('/sign_in',methods=['GET','POST'])
def sign_in(): 
    email = request.form.get('email')
    password = request.form.get('password')

    if email not in Users: 
        return render_template('sign-in 1 1.html', message = 'invalid email')
    elif password not in Users: 
        return render_template('sign-in 1 1.html', message = 'invalid password')
    else: 
        return render_template('profile 3.html')

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

#Registered Users
@app.route('/Users')
def Users():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return render_template("Users.html", users=rows)


# Cart route page
@app.route('/Cart/')
def Cart(): 
    return render_template('Cart.html')

#Payment page
@app.route('/Payment')
def Payment(): 
     return render_template('Payment.html')


if __name__ == '__main__':
    app.run(debug=True)