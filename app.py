from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from libs.GMI import GMI
import numpy as np
from PIL import Image
import zipfile
from time import gmtime, strftime
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
	print(app.root_path)
	print("ayu")

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

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		f.save('foto/' + secure_filename(f.filename))
	return render_template('upload.html')

@app.route('/coba')
def coba():
	return render_template('layout.html', data = { 'view' : 'upload', 'params': { 'nama': 'h3h3' } })

@app.route('/home')
def home():
	return render_template('home.html')

# https://stackoverflow.com/questions/41965026/extracting-all-the-files-of-a-selected-extension-from-a-zipped-file
@app.route('/pelatihan', methods=['GET', 'POST'])
def pelatihan():
	print(f"CWD: {os.getcwd()}")

	if request.method == 'POST':
		
		f = request.files['zip_file']
		filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
		f.save(filename)

		directory = strftime("%Y-%m-%d-%H-%M-%S")

		if not os.path.exists(directory):
			os.makedirs(directory)

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/training/' + directory) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			# pelatihan disini



			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

	return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

@app.route('/pengujian')
def pengujian():
	return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'})