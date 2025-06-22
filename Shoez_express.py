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

#Database connection (2) - Users (registered users)
def db_connection(): 
    conn = psycopg2.connect(host='localchost',
                            databse='users',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD']
                            )
    return conn


# Connect to the database
conn1 = psycopg2.connect(dbname="users", user="postgres",
                        password="flowers7*", host="localhost", port="5432")

# create a cursor
cur1 = conn1.cursor()


#Database connection (2) - Contact Page
def database_connect(): 
    conn = psycopg2.connect(host='localhost',
                            database='contact',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn 

# Connect to the database 2 
conn2 = psycopg2.connect(database="contact", user="postgres",
                        password="flowers7*", host="localhost",port="5432")

#cursor created 
cur2 = conn2.cursor()

#TABLE CREATED - users database 
@app.route('/db2')
def db2(): 
    try:
        #postgreSQL database connection
        conn = psycopg2.connect(dbname="users", #database name
                                user="postgres",#database user
                                password="flowers7*",
                                host="localhost",
                                port="5432")
        print("Succeffully connected to PostgreSQL database!")
    except psycopg2.Error as e: 
        print(f"Error in connecting with database: {e}")
        exit()

#TABLE CREATION - contact
@app.route('/db')
def db(): 
    try: 
        cur = conn2.cursor() 
        cur.execute('''
                CREATE TABLE IF NOT EXISTS contact (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    message TEXT,)
                ''')
        conn2.commit() 
        return "table created successfully!"
    except Exception as e: 
        conn2.rollback() 
        return f"Error: {e}"

#home page
@app.route('/')
def layout(): 
    return render_template('layout.html')

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
    email = request.form.get('email')
    password = request.form.get('password')

    return render_template('sign-in 1 1.html')

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