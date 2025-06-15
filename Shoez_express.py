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

def db_connection(): 
    conn = psycopg2.connect(host='localchost',
                            databse='users',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

# Connect to the database
conn = psycopg2.connect(database="users", user="postgres",
                        password="flowers7*", host="localhost", port="5432")

# create a cursor
cur = conn.cursor()

@app.route('/')
def contact(): 
    return render_template('contact_us.html')#add home page once finished testing code!

#user1.html - new file to store and display user information

#database trial only! - connection with real database coming soon!
database = {
        'Florence@gmail.com': 'flowers',
        'Lily@gmail.com': 'flow',
        'Laura@gmail.com': 'abc',
        }

#Sign-in route page
@app.route('/sign_in',methods=('GET','POST'))
def sign_in(): 
    #connecting with user input from (sign-in 1 1.html page)
    #eml = request.form['Email']#error to fix 404 bad request! 
    #pwrd = request.form['Password']
    #if pwrd not in database: 
     #   return render_template('sign-in 1 1.html', message = 'invalid')
    #else: 
     #   if database[eml] != pwrd:
      #      return render_template('sign-in 1 1.html', message = "invalid password")
       # else: 
    return render_template('sign-in 1 1.html')

#Sign-Up route page
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == "POST": 
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return "All fields are required", 400

        #insert data into postgreSQL database
        cur.execute('INSERT INTO users (username, email, password) ' 
                    'VALUES(%s, %s, %s)',
                    (username, email, password)
        )
            #commit changes
        conn.commit()
        return redirect(url_for('profile1', username=username))
    
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())

    return render_template('sign-up 1_1.html')

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

@app.route('/profile_settings')
def profile_settings(): 
    return render_template('profile_settings.html')

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

@app.route('/Payment')
def Payment(): 
     return render_template('Payment.html')

if __name__ == '__main__':
    app.run(debug=True)