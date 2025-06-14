from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os #libary used to import the Operating system - Upload image file for user

app = Flask(__name__)
app.secret_key = "ShoezExpress"

upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}


app.config['UPLOAD'] = upload_folder

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
@app.route('/sign_up/', methods=('GET','POST'))
def sign_up():
    #if request.method == 'POST': 
     #   username = request.form['username']
      #  email = request.form['email']
       # password = request.form['password']

    #if username not username: 
     #   print("Username is required")
    #elif not email: 
     #   print("Email is required!")
    #else: 
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

    #Account_Settings check
    #Email = request.form['Email']#required

    #if not Email: 
     #   flash('Email is required')
    #else: 
     #   return redirect(url_for('/profile_1'))
   # return render_template('profile_1.html')



# Cart route page
@app.route('/Cart/')
def Cart(): 
    return render_template('Cart.html')

@app.route('/Payment')
def Payment(): 
     return render_template('Payment.html')

if __name__ == '__main__':
    app.run(debug=True)