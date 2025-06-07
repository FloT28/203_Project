from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.utils import secure_filename
import os #libary used to import the Operating system - Upload image file for user
from flask_session import Session #

app = Flask(__name__)
app.secret_key = "ShoezExpress"

upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}


app.config['UPLOAD'] = upload_folder

@app.route('/')
def layout(): 
    return render_template('Layout.html')

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
    return render_template('sign-up 1_1.html')

#Profile route page
@app.route('/profile_1', methods=['GET','POST'])
def profile(): 
    if request.method == 'POST':
        file = request.files['img']#type of file requesting
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('profile 3.html', img=img)#return to the original html page (profile)
    return render_template('profile 3.html')

# Cart route page
@app.route('/Cart/')
def cart(): 
    return render_template('Cart1.html')

if __name__ == '__main__':
    app.run(debug=True)