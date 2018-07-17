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

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
 
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] 		= 'localhost'
app.config['MYSQL_DATABASE_USER'] 		= 'root'
app.config['MYSQL_DATABASE_PASSWORD'] 	= ''
app.config['MYSQL_DATABASE_DB'] 			= 'gmisvm'
mysql.init_app(app)

@app.route('/deteksi')
def deteksi():
	face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
	eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
	img = cv.imread('D:\\lena.jpg')
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    eyes = eye_cascade.detectMultiScale(roi_gray)
	    for (ex,ey,ew,eh) in eyes:
	        cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	cv.imshow('img',img)
	cv.waitKey(0)
	cv.destroyAllWindows()

@app.route('/deteksi2')
def deteksi2():
	
	face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	eye_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_eye.xml')
	img = cv2.imread('D:\\lena.jpg')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    eyes = eye_cascade.detectMultiScale(roi_gray)
	    for (ex,ey,ew,eh) in eyes:
	        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	facecnt = len(faces)
	print("Detected faces: %d" % facecnt)
	i = 0
	height, width = img.shape[:2]

	for (x, y, w, h) in faces:
		r = max(w, h) / 2
		centerx = x + w / 2
		centery = y + h / 2
		nx = int(centerx - r)
		ny = int(centery - r)
		nr = int(r * 2)

		faceimg = img[ny:ny+nr, nx:nx+nr]
		lastimg = cv2.resize(faceimg, (32, 32))
		i += 1
		cv2.imwrite("image%d.jpg" % i, lastimg)

		if __name__ == '__main__':
			args = sys.argv
			argc = len(args)

			if (argc != 2):
			    print('Usage: %s [image file]' % args[0])
			    quit()

			detecter = FaceCropper()
			detecter.generate(args[1], True)


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

@app.route('/deteksi_wajah')
def deteksi_wajah(image, dir1, dir2):
	
	face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	img = cv2.imread(image)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	for f in faces:
		x, y, w, h = [v for v in f]
		cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255))
		sub_face = img[y:y+h, x:x+w]

		face_file_name = "data/training/" + dir1 + "/" + dir2 + "/" + "01.jpg"
		cv2.imwrite(face_file_name, sub_face)

	return face_file_name

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

			# openCV
			berkas_citra = deteksi_wajah(berkas, directory, dir2)

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