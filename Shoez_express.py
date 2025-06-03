from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os #libary used to import the Operating system - Upload image file for user


app = Flask(__name__)

upload_folder = os.path.join('static', 'upload')
allowed_extensions = {'png','jpg','jpeg','gif'}


app.config['UPLOAD'] = upload_folder

@app.route('/')
def layout(): 
    return render_template('Layout.html')

#Sign-in route page
@app.route('/sign-in/',methods=('GET','POST'))
def sign_in(): 
    
    return render_template('sign-in2.html')

#Sign-Up route page
@app.route('/sign-up/',methods=('GET','POST'))
def sign_up():
    return render_template('sign-up2.html')

#Profile route page
@app.route('/profile_1', methods=['GET','POST'])
def profile(): 
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        return render_template('profile 3.html', img=img)
    return render_template('profile 3.html')

# Cart route page
@app.route('/Cart/')
def cart(): 
    return render_template('Cart1.html')


if __name__ == '__main__':
    app.run(debug=True)