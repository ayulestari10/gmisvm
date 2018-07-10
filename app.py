from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from libs.GMI import GMI
import numpy as np
from PIL import Image


app = Flask(__name__)

@app.route('/')
def index():
	matrix = np.array([
	    [1, 4, 3],
	    [5, 2, 4],
	    [9, 7, 8]
	])

	path = "D:\\Citra Lena.jpg"

	im = Image.open(path).convert('L')
	pixel = np.array(im)
	greyscale = Image.fromarray(pixel)
	greyscale.save('foto/result_greyscale.jpg')

	threshold = 256 / 2
	binary = greyscale.point(lambda p: p > threshold and 255)
	binary.save('foto/result_binary.jpg')

	gmi = GMI(pixel)
	gmi.hitungMomenNormalisasi()
	ciri = gmi.hitungCiri()
	return str(ciri)

@app.route('/hasil')
def hasil():
	return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if valid_login( request.form['username'],
						request.form['password']):
			return log_the_user_in(request.form['username']) 
		else:
			error = 'Invalid username or password'

	return render_template('login.html', error = error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		f.save('foto/' + secure_filename(f.filename))
	return render_template('upload.html')
