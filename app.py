from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from libs.GMI import GMI
import numpy as np
from PIL import Image
import zipfile
from time import gmtime, strftime
import os
from flaskext.mysql import MySQL
import cv2
from sklearn.svm import SVC, LinearSVC
from sklearn.multiclass import OneVsRestClassifier
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
 
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] 		= 'localhost'
app.config['MYSQL_DATABASE_USER'] 		= 'root'
app.config['MYSQL_DATABASE_PASSWORD'] 	= ''
app.config['MYSQL_DATABASE_DB'] 			= 'gmisvm'
mysql.init_app(app)


@app.route('/')
def index():
	print(app.root_path)
	print("ayu")

	matrix = np.array([
	    [1, 4, 3], 
	    [5, 2, 4],
	    [9, 7, 8]
	])

	# path = "D:\\Citra Lena.jpg"

	# im = Image.open(path).convert('L')
	# pixel = np.array(im)
	# greyscale = Image.fromarray(pixel)
	# greyscale.save('foto/result_greyscale.jpg')

	# threshold = 256 / 2
	# binary = greyscale.point(lambda p: p > threshold and 255)
	# binary.save('foto/result_binary.jpg')

	gmi = GMI(matrix)
	gmi.hitungMomenNormalisasi()
	ciri = gmi.hitungCiri()
	return str(ciri)


@app.route('/home')
def home():
	return render_template('home.html')


# Berhubungan dengan database
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
	pixel_binary= np.array(binary.point(lambda p : p > threshold and 1))

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

@app.route('/select_ciri')
def select_ciri():
	cur = mysql.get_db().cursor()
	cur.execute("SELECT * FROM ciri")

	# mysql.get_db().commit()
	data = cur.fetchall()
	print(f"SELECTED: {data}")
	x = np.array(data)
	print(x[:,1])
	ciri = x[:, 2:]
	kum_ciri = ciri.astype(np.float64)

	return kum_ciri

@app.route('/select_kelas')
def select_kelas():
	cur = mysql.get_db().cursor()
	cur.execute("SELECT * FROM ciri")

	# mysql.get_db().commit()
	data = cur.fetchall()

	x = np.array(data)
	kelas = x[:, 1]

	return str(kelas)

def select_kelasV2():
	cur = mysql.get_db().cursor()
	cur.execute("SELECT * FROM ciri")

	# mysql.get_db().commit()
	data = cur.fetchall()

	x = np.array(data)
	kelas = x[:, 1]

	return kelas

@app.route('/deteksi_wajah')
def deteksi_wajah(proses, image, dir1, dir2):
	
	face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	img = cv2.imread(image)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	# cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	global face_file_name
	
	for f in faces:
		x, y, w, h = [v for v in f]
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255))
		sub_face = img[y:y+h, x:x+w]

		face_file_name = "data/" + proses + "/" + dir1 + "/" + dir2 + "/" + "01.jpg"
		cv2.imwrite(face_file_name, sub_face)

	return face_file_name


@app.route('/pelatihan', methods=['GET', 'POST'])
def pelatihan():

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

		for i in range(7):
			print(i)

			dir2		= os.listdir('data/training/' + directory + '/') [i]
			print("dir 2 = " + dir2)

			jenis_kelas = dir1[i]
			print("jenis kelas = " + jenis_kelas)

			file_name	= os.listdir('data/training/' + directory + '/' + dir2)[0]	
			print("file name = " + file_name)
			files	= os.listdir('data/training/' + directory + '/' + dir2)
			for file in files:

				berkas 		= cwd + '\\data\\training\\' + directory + '\\' + dir2 + '\\' + file

				print("berkas = " + berkas)

				# openCV
				berkas_citra = deteksi_wajah("training", berkas, directory, dir2)

				im 			= Image.open(berkas_citra)
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
				print(f"ini ciri sebelum = {ciri}")

				ciri = -np.sign(ciri) * np.log10(np.abs(ciri))

				# HU OpenCV
				# ciri 		= cv2.HuMoments(cv2.moments(pixel_binary)).flatten()
				print(f"ini ciri sesudah = {ciri}")

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

		flash('Data pelatihan berhasil dilatih')
		return redirect(url_for('.pelatihan'))

	return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})


@app.route('/pengujian', methods=['GET', 'POST'])
def pengujian():

	if request.method == "POST":
		f = request.files['foto']
		
		directory = strftime("%Y-%m-%d-%H-%M-%S")

		filename = 'data/testing/' + secure_filename(directory + '_' + f.filename)
		f.save(filename)

		cwd = os.getcwd()

		# file_name	= os.listdir('data/testing/' + directory)[0]	
		# 	print("file name = " + file_name)

		berkas 		= cwd + "\\data\\testing\\" + secure_filename(directory + '_' + f.filename)
		print("berkas = " + berkas)

		if not os.path.exists(cwd + "\\data\\testing\\" + directory + "\\coba"):
			os.makedirs(cwd + "\\data\\testing\\" + directory + "\\coba")
			print(cwd + "\\data\\testing\\" + directory + "\\coba")

		berkas_citra = deteksi_wajah("testing", berkas, directory, "coba")

		im 			= Image.open(berkas_citra)
		biner		= im.convert('L')
		pixel 		= np.array(biner)
		
		greyscale 	= Image.fromarray(pixel)
		greyscale.save('result/result_greyscale.jpg')

		threshold 	= 256 / 2
		binary 		= greyscale.point(lambda p: p > threshold and 255)
		binary.save('result/result_binary.jpg')
		pixel_binary= np.array(binary)

		print(pixel_binary)
		print(pixel_binary[2])

		gmi 		= GMI(pixel_binary)
		gmi.hitungMomenNormalisasi()
		ciri 		= gmi.hitungCiri()
		print(ciri)

		# Klasifikasi dengan svm

		kumpulan_ciri = select_ciri()
		print("Ini ciri")
		print(kumpulan_ciri)
		kumpulan_kelas= select_kelasV2()
		print(f"Features: {kumpulan_ciri.shape}")
		lin_clf = SVC(gamma= 0.1, C=10000, kernel='linear')
		lin_clf.fit(kumpulan_ciri, encode_class(kumpulan_kelas))

		# dec = lin_clf.decision_function(kumpulan_ciri)
		# hasil = dec.shape[1]
		# print(f"Ini hasilnya = {hasil}")
		result = lin_clf.predict([ciri])
		print(f"Kelas: {decode_class(kumpulan_kelas, result)}")

	return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'})


def encode_class(labels):
	dct = {
		"bahagia": 0,
		"jijik": 1,
		"kaget": 2,
		"marah": 3,
		"penghinaan": 4,
		"sedih": 5,
		"takut": 6
	}
	return [dct[str(label)] for label in labels]

def decode_class(labels, indices):
	return [labels[idx] for idx in indices]

















# percobaan pembuatan fungsi


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

@app.route('/deteksi3')
def deteksi3():
	
	face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	# eye_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_eye.xml')
	img = cv2.imread('D:\\coba2.jpg')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    # eyes = eye_cascade.detectMultiScale(roi_gray)
	    # for (ex,ey,ew,eh) in eyes:
	    #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	for f in faces:
		x, y, w, h = [v for v in f]
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255))
		sub_face = img[y:y+h, x:x+w]

		face_file_name = "result/face_" + str(y) + ".jpg"
		cv2.imwrite(face_file_name, sub_face)

	return redirect('home')

	# if __name__ :  
	# 	facechop("D:\\lena.jpg")

	# 	while(True):
	# 		key = cv2.waitKey(20)
	# 		if key in [27, ord('Q'), ord('q')]:
	# 			break

"""
[[ 2.61513918e-03,  1.01227846e-07,  2.59610000e-09,
 2.64212955e-10, -1.20510417e-19, -5.45843923e-14,
 1.38975825e-20],
[ 2.60701507e-03,  1.29615030e-07,  5.28535000e-10,
 8.73370411e-11,  9.36996803e-21,  2.19705008e-14,
 5.04007345e-22],
[ 2.61371669e-02,  5.34799642e-04,  1.21576000e-05,
 1.92784247e-05,  2.95118266e-10,  4.45770765e-07,
-1.42867223e-10],
[ 3.10404048e-03,  2.88522503e-07,  1.05351000e-08,
 2.10084227e-09, -9.72172599e-18,  4.46220958e-13,
 4.78163606e-19],
[ 2.20064832e-03,  1.73860781e-07,  4.42980000e-09,
 2.42987387e-10, -2.15700444e-19,  4.27169143e-14,
 1.08646152e-20],
[ 2.80683267e-03,  7.20717838e-08,  5.49436000e-09,
 3.29614713e-10,  3.24776196e-19, -8.67832146e-14,
-2.81513366e-20],
[ 2.61513918e-03,  1.01227846e-07,  2.59610000e-09,
 2.64212955e-10, -1.20510417e-19, -5.45843923e-14,
 1.38975825e-20],
[ 2.02296702e-03,  1.23815302e-07,  9.91890000e-10,
 1.22685996e-10, -3.43312840e-20, -4.30056085e-14,
-5.49825189e-21],
[ 1.23161772e-03,  3.06799827e-08,  3.54556000e-10,
 6.71244957e-11,  5.05725423e-21, -1.12923273e-14,
-3.47894090e-21],
[ 2.60701507e-03,  1.29615030e-07,  5.28535000e-10,
 8.73370411e-11,  9.36996803e-21,  2.19705008e-14,
 5.04007345e-22],
[ 1.89171317e-02,  2.83715699e-04,  4.71068000e-06,
 7.29416108e-06,  4.27482233e-11,  1.22853212e-07,
-2.06690139e-11],
[ 2.61371669e-02,  5.34799642e-04,  1.21576000e-05,
 1.92784247e-05,  2.95118266e-10,  4.45770765e-07,
-1.42867223e-10],
[ 2.12646400e-03,  1.74429999e-07,  1.20689000e-09,
 8.60275430e-11, -1.91560916e-20, -3.49390329e-14,
-2.98889957e-21],
[ 1.41319004e-03,  1.78077273e-07,  3.21226000e-10,
 6.52200122e-12,  6.32986740e-23, -2.29077561e-15,
-6.27709492e-23],
[ 3.10404048e-03,  2.88522503e-07,  1.05351000e-08,
 2.10084227e-09, -9.72172599e-18,  4.46220958e-13,
 4.78163606e-19],
[ 1.67220185e-03,  1.42004109e-08,  2.39098000e-09,
 1.41725811e-10, -3.41724438e-20, -6.22537197e-15,
-2.06677264e-21],
[ 1.06687821e-03,  7.66043953e-09,  6.56881000e-11,
 1.31887819e-11,  3.49400488e-22, -7.02943620e-16,
-4.37584214e-23],
[ 2.20064832e-03,  1.73860781e-07,  4.42980000e-09,
 2.42987387e-10, -2.15700444e-19,  4.27169143e-14,
 1.08646152e-20],
[ 2.26563781e-03,  1.58437216e-07,  3.14787000e-09,
 3.82814497e-10, -3.71130403e-19, -1.51252604e-13,
-4.04884526e-20],
[ 1.10278732e-03,  8.11407466e-09,  4.98049000e-11,
 2.48266538e-11,  8.34708047e-22, -8.79271931e-16,
-2.27539818e-22],
[ 2.80683267e-03,  7.20717838e-08,  5.49436000e-09,
 3.29614713e-10,  3.24776196e-19, -8.67832146e-14,
-2.81513366e-20],
[ 2.37452373e-03,  1.73025955e-07,  2.93595000e-09,
 7.26402732e-11, -2.82839097e-20, -2.97836009e-14,
-1.22064388e-22],
[ 1.20426376e-03,  1.15823780e-09,  3.81610000e-11,
 2.61757655e-11,  4.31147650e-22,  8.38968408e-16,
-6.06179791e-23],
[ 2.61513918e-03,  1.01227846e-07,  2.59610000e-09,
 2.64212955e-10, -1.20510417e-19, -5.45843923e-14,
 1.38975825e-20],
[ 2.61513918e-03,  1.01227846e-07,  2.59610000e-09,
 2.64212955e-10, -1.20510417e-19, -5.45843923e-14,
 1.38975825e-20],
[ 2.02296702e-03,  1.23815302e-07,  9.91890000e-10,
 1.22685996e-10, -3.43312840e-20, -4.30056085e-14,
-5.49825189e-21],
[ 1.23161772e-03,  3.06799827e-08,  3.54556000e-10,
 6.71244957e-11,  5.05725423e-21, -1.12923273e-14,
-3.47894090e-21],
[ 2.60701507e-03,  1.29615030e-07,  5.28535000e-10,
 8.73370411e-11,  9.36996803e-21,  2.19705008e-14,
 5.04007345e-22],
[ 1.89171317e-02,  2.83715699e-04,  4.71068000e-06,
 7.29416108e-06,  4.27482233e-11,  1.22853212e-07,
-2.06690139e-11],
[ 2.61371669e-02,  5.34799642e-04,  1.21576000e-05,
 1.92784247e-05,  2.95118266e-10,  4.45770765e-07,
-1.42867223e-10],
[ 2.12646400e-03,  1.74429999e-07,  1.20689000e-09,
 8.60275430e-11, -1.91560916e-20, -3.49390329e-14,
-2.98889957e-21],
[ 1.41319004e-03,  1.78077273e-07,  3.21226000e-10,
 6.52200122e-12,  6.32986740e-23, -2.29077561e-15,
-6.27709492e-23],
[ 3.10404048e-03,  2.88522503e-07,  1.05351000e-08,
 2.10084227e-09, -9.72172599e-18,  4.46220958e-13,
 4.78163606e-19],
[ 1.67220185e-03,  1.42004109e-08,  2.39098000e-09,
 1.41725811e-10, -3.41724438e-20, -6.22537197e-15,
-2.06677264e-21],
[ 1.06687821e-03,  7.66043953e-09,  6.56881000e-11,
 1.31887819e-11,  3.49400488e-22, -7.02943620e-16,
-4.37584214e-23],
[ 2.20064832e-03,  1.73860781e-07,  4.42980000e-09,
 2.42987387e-10, -2.15700444e-19,  4.27169143e-14,
 1.08646152e-20],
[ 2.26563781e-03,  1.58437216e-07,  3.14787000e-09,
 3.82814497e-10, -3.71130403e-19, -1.51252604e-13,
-4.04884526e-20],
[ 1.10278732e-03,  8.11407466e-09,  4.98049000e-11,
 2.48266538e-11,  8.34708047e-22, -8.79271931e-16,
-2.27539818e-22],
[ 2.80683267e-03,  7.20717838e-08,  5.49436000e-09,
 3.29614713e-10,  3.24776196e-19, -8.67832146e-14,
-2.81513366e-20],
[ 2.37452373e-03,  1.73025955e-07,  2.93595000e-09,
 7.26402732e-11, -2.82839097e-20, -2.97836009e-14,
-1.22064388e-22],
[ 1.20426376e-03,  1.15823780e-09,  3.81610000e-11,
 2.61757655e-11,  4.31147650e-22,  8.38968408e-16,
-6.06179791e-23]]

labels = ['bahagia', 'jijik', 'kaget', 'marah', 'penghinaan', 'sedih', 'bahagia', 'bahagia', 'bahagia', 'jijik', 'jijik', 'kaget', 'kaget', 'kaget', 'marah', 'marah', 'marah', 'penghinaan', 'penghinaan', 'penghinaan', 'sedih', 'sedih', 'sedih', 'bahagia', 'bahagia', 'bahagia', 'bahagia', 'jijik', 'jijik', 'kaget', 'kaget', 'kaget', 'marah', 'marah', 'marah', 'penghinaan', 'penghinaan', 'penghinaan', 'sedih', 'sedih', 'sedih']
"""