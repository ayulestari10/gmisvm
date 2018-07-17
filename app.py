from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from libs.GMI import GMI
import numpy as np
from PIL import Image
import zipfile
from time import gmtime, strftime
import os
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
 
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] 		= 'localhost'
app.config['MYSQL_DATABASE_USER'] 		= 'root'
app.config['MYSQL_DATABASE_PASSWORD'] 	= ''
app.config['MYSQL_DATABASE_DB'] 			= 'gmisvm'
mysql.init_app(app)

@app.route('/insert', methods = ['POST', 'GET'])
def insert():
	citra 		= os.listdir('data/training/')[1]
	cwd 		= os.getcwd()
	berkas 		= cwd + '\\data\\training\\' + citra

	im 			= Image.open(berkas)
	biner		= im.convert('L')
	pixel 		= np.array(biner)
	
	greyscale 	= Image.fromarray(pixel)
	greyscale.save('result/result_greyscale.jpg')

	threshold 	= 256 / 2
	binary 		= greyscale.point(lambda p: p > threshold and 255)
	binary.save('result/result_binary.jpg')
	pixel_binary= np.array(binary)

	gmi 		= GMI(pixel_binary)
	gmi.hitungMomenNormalisasi()
	ciri 		= gmi.hitungCiri()

	# ciri = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
	jenis_kelas = ['Marah', 'Bahagia']
		
	nilai_ciri1 = ciri[0]
	nilai_ciri2 = ciri[1]
	nilai_ciri3 = ciri[2]
	nilai_ciri4 = ciri[3]
	nilai_ciri5 = ciri[4]
	nilai_ciri6 = ciri[5]
	nilai_ciri7 = ciri[6]
	kelas 		= "Sedih"

	cur = mysql.get_db().cursor()
	cur.execute("INSERT INTO ciri (kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

	mysql.get_db().commit()
	print("Berhasil hoye")
	return redirect('home')


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
	# print(f"CWD: {os.getcwd()}")

	if request.method == 'POST':
		
		f = request.files['zip_file']
		filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
		f.save(filename)

		directory = strftime("%Y-%m-%d-%H-%M-%S")

		# if not os.path.exists(directory):
		# 	os.makedirs(directory)

		with open(filename, mode = 'r') as file:
			zip_file = zipfile.ZipFile(filename)
			files = [zip_file.extract(fl, 'data/training/' + directory) for fl in zip_file.namelist()]
			zip_file.close()
		os.remove(filename)

		# pelatihan disini
		dir1 		= os.listdir('data/training/' + directory)
		cwd 		= os.getcwd()

		for i in range(6):
			print(i)

			dir2		= os.listdir('data/training/' + directory + '/') [i]
			print("dir 2 = " + dir2)

			jenis_kelas = dir1[i]
			print("jenis kelas = " + jenis_kelas)

			file_name	= os.listdir('data/training/' + directory + '/' + dir2)[0]	
			print("file name = " + file_name)

			berkas 		= cwd + '\\data\\training\\' + directory + '\\' + dir2 + '\\' + file_name

			print("berkas = " + berkas)
			im 			= Image.open(berkas)
			# biner		= im.convert('L')
			# pixel 		= np.array(biner)
			
			# greyscale 	= Image.fromarray(pixel)
			# greyscale.save('result/result_greyscale.jpg')

			threshold 	= 256 / 2
			binary 		= im.point(lambda p: p > threshold and 255)
			binary.save('result/result_binary.jpg')
			pixel_binary= np.array(binary)

			gmi 		= GMI(pixel_binary)
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()

			nilai_ciri1 = ciri[0]
			nilai_ciri2 = ciri[1]
			nilai_ciri3 = ciri[2]
			nilai_ciri4 = ciri[3]
			nilai_ciri5 = ciri[4]
			nilai_ciri6 = ciri[5]
			nilai_ciri7 = ciri[6]
			kelas 		= jenis_kelas

			cur = mysql.get_db().cursor()
			cur.execute("INSERT INTO ciri (kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			print("INSERT INTO ciri (kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			mysql.get_db().commit()
		# print("Berhasil hoye")
		# return redirect('home')


		flash('Data pelatihan berhasil dilatih')
		return redirect(url_for('.pelatihan'))

	return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

@app.route('/pengujian')
def pengujian():
	return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'})