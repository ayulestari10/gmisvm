from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
import cv2, numpy as np, random
from libs.GMI import GMI
from libs.Praproses import Praproses
from models.Database import Database
from libs.Klasifikasi import Klasifikasi
import MySQLdb
import os
from time import gmtime, strftime
from collections import Counter


class Deteksi_wajah:

	page = Blueprint('Deteksi_wajah_page', __name__, template_folder = 'templates')
	base = '/deteksi-wajah'
	Db 	 = Database('localhost', 'root', '', 'gmisvm')

	def __init__(self):
		self.rectColor = {
			
			'bahagia': (0, 255, 255),	# kuning
			'sedih': (255, 0, 0),		# biru
			'jijik': (0, 255, 0),		# hijau
			'takut': (238,130,238),		# ungu
			'natural': (255, 255, 255),	# putih
			'marah': (0, 0, 255),  	# pink
			'kaget' : (0, 0, 0)			# hitam
		}
		self.waktu_s = ""

	# fungsi untuk mengambil piksel sub window
	def get_sliding_window(self, matrix, x, y, size = 24):
		return matrix[x:x+size, y:y+size]

	def rectangle_a(self, sliding_window, x, y, size=(1, 2)):
		A = sliding_window[x - 1, y - 1]
		B = sliding_window[x - 1, (y + size[1]  - 1) // 2]
		C = sliding_window[x + size[0] - 1, y - 1]
		D = sliding_window[x + size[0] - 1, (y + size[1] - 1) // 2]

		black = D + A - (B + C)

		A = sliding_window[x - 1, ((y + size[1]) - 1) // 2]
		B = sliding_window[x - 1, (y + size[1]) - 1]
		C = sliding_window[x + size[0] - 1, ((y + size[1]) - 1) // 2]
		D = sliding_window[x + size[0] - 1, (y + size[1]) - 1]

		white = D + A - (B + C)

		return abs(black - white)

	def rectangle_b(self, sliding_window, x, y, size=(2, 1)):
		A = sliding_window[x - 1, y - 1]
		B = sliding_window[x - 1, y + size[1]  - 1]
		C = sliding_window[(x + size[0] - 1) // 2, y - 1]
		D = sliding_window[(x + size[0] - 1) // 2, y + size[1] - 1]

		black = D + A - (B + C)

		A = sliding_window[(x + size[0] - 1) // 2, y - 1]
		B = sliding_window[(x + size[0] - 1) // 2, y + size[1] - 1]
		C = sliding_window[x + size[0] - 1, y - 1]
		D = sliding_window[x + size[0] - 1, (y + size[1]) - 1]

		white = D + A - (B + C)

		return abs(black - white)

	def rectangle_c(self, sliding_window, x, y, size=(1, 3)):
		chunk_size = size[1] // 3

		ul_x = x - 1
		ul_y = y - 1
		ur_x = x - 1
		ur_y = y + chunk_size - 1
		bl_x = x + size[0] - 1
		bl_y = y - 1
		br_x = x + size[0] - 1
		br_y = y + chunk_size - 1

		A = sliding_window[ul_x, ul_y]
		B = sliding_window[ur_x, ur_y]
		C = sliding_window[bl_x, bl_y]
		D = sliding_window[br_x, br_y]

		black = D + A - (B + C)

		A = sliding_window[ul_x, ul_y + chunk_size]
		B = sliding_window[ur_x, ur_y + chunk_size]
		C = sliding_window[bl_x, bl_y + chunk_size]
		D = sliding_window[br_x, br_y + chunk_size]

		white = D + A - (B + C)

		A = sliding_window[ul_x, ul_y + (chunk_size * 2)]
		B = sliding_window[ur_x, ur_y + (chunk_size * 2)]
		C = sliding_window[bl_x, bl_y + (chunk_size * 2)]
		D = sliding_window[br_x, br_y + (chunk_size * 2)]

		black += D + A - (B + C)

		return abs(black - white)

	def rectangle_d(self, sliding_window, x, y, size=(2, 2)):
		chunk_x = size[0] // 2
		chunk_y = size[1] // 2

		ul_x = x - 1
		ul_y = y - 1
		ur_x = x - 1
		ur_y = y + chunk_y - 1
		bl_x = x + chunk_x - 1
		bl_y = y - 1
		br_x = x + chunk_x - 1
		br_y = y + chunk_y - 1

		A = sliding_window[ul_x, ul_y]
		B = sliding_window[ur_x, ur_y]
		C = sliding_window[bl_x, bl_y]
		D = sliding_window[br_x, br_y]

		black = D + A - (B + C)

		A = sliding_window[ul_x, ul_y + chunk_y]
		B = sliding_window[ur_x, ur_y + chunk_y]
		C = sliding_window[bl_x, bl_y + chunk_y]
		D = sliding_window[br_x, br_y + chunk_y]

		white = D + A - (B + C)

		A = sliding_window[ul_x + chunk_x, ul_y]
		B = sliding_window[ur_x + chunk_x, ur_y]
		C = sliding_window[bl_x + chunk_x, bl_y]
		D = sliding_window[br_x + chunk_x, br_y]

		white += D + A - (B + C)

		A = sliding_window[ul_x + chunk_x, ul_y + chunk_y]
		B = sliding_window[ur_x + chunk_x, ur_y + chunk_y]
		C = sliding_window[bl_x + chunk_x, bl_y + chunk_y]
		D = sliding_window[br_x + chunk_x, br_y + chunk_y]

		black += D + A - (B + C)
		print(f"black: {D} + {A} - ({B} + {C})")

		return abs(black - white)

	def deteksi_vj(self):
		# Praproses Ke Gray Scale

		image = "D:\\bahagia.png"

		# im = self.resize_image(image)

		# im 	= Image.open(image)
		# im	= im.convert('L') 
		# im 	= np.array(im)

		# im = np.random.randint(255, size=(24, 24))
		# print(im)
		# sliding_window = self.get_sliding_window(im, 0, 0)
		# integral_image = self.integral_image(sliding_window)

		im = np.array([
			[2, 6, 13, 18, 26],
			[3, 12, 20, 32, 47],
			[8, 23, 40, 57, 78],
			[16, 40, 67, 90, 118],
			[26, 62, 97, 123, 157]
		])

		print(self.rectangle_d(im, 1, 1, (2, 2)))


		# im2 = np.array([
		# 	[228,	10, 	10]
		# 	[30, 	10, 	228],
		# 	[128, 	20, 	220],
		# 	[111, 	20, 	218],
		# ])

		# # Fitur Haar
		# im_haar = self.haar_feature(im2)

		# # Integral Image
		# im_integral = self.integral_image(im)
		# print(im_integral)		


		# Algoritma Adaboost


		# Cascade Classifier

	# jika nilai mendekati 255 maka terdapat haar feature / threshold
	# def haar_feature(self, im):
	# 	for x in 25:
	# 		for y, col in enumerate(row):


	def integral_image(self, im):
		for x, row in enumerate(im):
			for y, col in enumerate(row):
				if x > 0: im[x][y] += im[x - 1][y]
				if y > 0: im[x][y] += im[x][y - 1]
				if x > 0 and y > 0: im[x][y] -= im[x - 1][y - 1]
		return im

	def resize_image(self, im):
		size = 288, 384

		img = Image.open(im)
		img = np.array(img)
		img.resize((384, 288), Image.ANTIALIAS)

		path = "data/training/resize/hasil_resize.png"
		cv2.imwrite(path, img)

		return img



	def deteksi(self, image, dir1, dir2):
		
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		global face_file_name
		
		for f in faces:
			x, y, w, h = [v for v in f]
			sub_face = img[y:y+h, x:x+w]

			face_file_name = "data/latih_uji/" + dir1 + "/" + dir2 + "/" + "01.png"
			cv2.imwrite(face_file_name, sub_face)

		return face_file_name

	def deteksi_multi_face_sendiri(self, id_file, image):
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		dir_image 	= 'C:\\xampp\\htdocs\\gmisvm\\data\\uji\\' + image
		img 		= cv2.imread(dir_image)
		gray 		= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces 		= face_cascade.detectMultiScale(gray, 1.3, 5)
		ekspr 		= list(self.rectColor.values())

		global face_file_name

		print(f"Ini jumlah face = {len(faces)}")

		# ciri dan kelas sendiri
		kumpulan_ciri_s 	= Deteksi_wajah.Db.select_ciri('ciri_pelatihan', 'S')
		kumpulan_kelas_s 	= Deteksi_wajah.Db.select_kelas('ciri_pelatihan', 'S')

		rata_rata_ciri_s 	= {}
		for kelas_s in kumpulan_kelas_s:
			rata_rata_ciri_s[kelas_s] = Deteksi_wajah.Db.select_avg('ciri_pelatihan', kelas_s)

		for i, f in enumerate(faces):
			x, y, w, h 		= np.array([v for v in f], dtype=np.int64)

			sub_face 		= img[y:y+h, x:x+w]
			face_file_name 	= 'data/uji/' + str(i) + '.png'
			cv2.imwrite(face_file_name, sub_face)

			## start - klasifikasi
			
			pra 		= Praproses()
			sub_face 	= pra.biner(face_file_name)
			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()

			momen 		= cv2.moments(sub_face)
			ciricv 		= cv2.HuMoments(momen).flatten()
			
			# klasifikasi sendiri
			kl_s 		= Klasifikasi(kumpulan_ciri_s, kumpulan_kelas_s)			
			ekspresi_s 	= kl_s.classify([ciri])
			print(f"Ekspresi Sendiri = {ekspresi_s}")


			cv2.rectangle(img, (x,y), (x+w, y+h), self.rectColor[ekspresi_s])
			cv2.rectangle(img, (x, y - 30), (x + 100, y), self.rectColor[ekspresi_s], -1)
			cv2.putText(img, ekspresi_s, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

			Deteksi_wajah.Db.insert_ciri('ciri_pengujian', ciri, 'S')
			data_pengujian_s	= Deteksi_wajah.Db.select_first_row()
			id_ciri_pengujian_s	= str(data_pengujian_s[0][0])

			# insert pengujian
			self.waktu_s = strftime("%Y-%m-%d_%H-%M-%S")

			data_pengujian 	= {
				'id_file'				: str(id_file),
				'id_ciri_pengujian_s'	: id_ciri_pengujian_s,
				'waktu'					: self.waktu_s,
				'hasil_sendiri'			: ekspresi_s
			}
			pengujian = Deteksi_wajah.Db.insert_pengujian(data_pengujian)

			# Jarak Setiap Ciri Koding Sendiri
			jarak_bahagia_s = []
			for i in range(7):
				jarak_bahagia_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['bahagia'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'bahagia', jarak_bahagia_s)

			jarak_sedih_s = []
			for i in range(7):
				jarak_sedih_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['sedih'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'sedih', jarak_sedih_s)

			jarak_marah_s = []
			for i in range(7):
				jarak_marah_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['marah'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'marah', jarak_marah_s)

			jarak_jijik_s = []
			for i in range(7):
				jarak_jijik_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['jijik'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'jijik', jarak_jijik_s)

			jarak_kaget_s = []
			for i in range(7):
				jarak_kaget_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['kaget'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'kaget', jarak_kaget_s)

			jarak_takut_s = []
			for i in range(7):
				jarak_takut_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['takut'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'takut', jarak_takut_s)

			jarak_natural_s = []
			for i in range(7):
				jarak_natural_s.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['natural'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'natural', jarak_natural_s)
				

		# select data hasil pengujian sendiri dan insert hasil sendiri
		hasil_s 	= Deteksi_wajah.Db.select_hasil('hasil_sendiri', str(id_file), self.waktu_s)
		hitung_s 	= Counter(elem[0] for elem in hasil_s)

		hasil_all_s = {
			'id_file'	: id_file,
			'ket'		: 'S', 
			'wajah' 	: len(faces),
			'bahagia'	: hitung_s['bahagia'],
			'sedih'		: hitung_s['sedih'],
			'marah'		: hitung_s['marah'],
			'jijik'		: hitung_s['jijik'],
			'kaget'		: hitung_s['kaget'],
			'takut'		: hitung_s['takut'],
			'natural'	: hitung_s['natural']
		}
		Deteksi_wajah.Db.insert_hasil(hasil_all_s)

		cwd = os.getcwd()
		dir_file_name 	= 'static/data/latih_uji/' + self.waktu_s + '_Hasil_Sendiri.png'
		print(f"dir = {dir_file_name}")
		file_name 		= self.waktu_s + '_Hasil_Sendiri.png'
		print(f"file name = {file_name}")
		cv2.imwrite(dir_file_name, img)

		return file_name

	def deteksi_multi_face_opencv(self, id_file, image):
		face_cascade= cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		dir_image 	= 'C:\\xampp\\htdocs\\gmisvm\\data\\uji\\' + image
		img 		= cv2.imread(dir_image)
		gray 		= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces 		= face_cascade.detectMultiScale(gray, 1.3, 5)
		ekspr 		= list(self.rectColor.values())

		global face_file_name

		print(f"Ini jumlah face = {len(faces)}")

		# ciri dan kelas openCV
		kumpulan_ciri_o 	= Deteksi_wajah.Db.select_ciri('ciri_pelatihan', 'O')
		kumpulan_kelas_o 	= Deteksi_wajah.Db.select_kelas('ciri_pelatihan', 'O')

		rata_rata_ciri_o 	= {}
		for kelas_o in kumpulan_kelas_o:
			rata_rata_ciri_o[kelas_o] = Deteksi_wajah.Db.select_avg('ciri_pelatihan', kelas_o)

		ekspresi_openCV = []

		for i, f in enumerate(faces):
			x, y, w, h = np.array([v for v in f], dtype=np.int64)

			sub_face = img[y:y+h, x:x+w]

			face_file_name = 'data/uji/' + str(i) + '__.png'
			cv2.imwrite(face_file_name, sub_face)

			## start - klasifikasi
			
			pra 		= Praproses()
			sub_face 	= pra.biner(face_file_name)
			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()

			momen 		= cv2.moments(sub_face)
			ciricv 		= cv2.HuMoments(momen).flatten()
			
			# klasifikasi hasil ciri openCV
			kl_o 		= Klasifikasi(kumpulan_ciri_o, kumpulan_kelas_o)
			ekspresi_o 	= kl_o.classify([ciricv])
			print(f"Ekspresi OpenCV = {ekspresi_o}")

			cv2.rectangle(img, (x,y), (x+w, y+h), self.rectColor[ekspresi_o])
			cv2.rectangle(img, (x, y - 30), (x + 100, y), self.rectColor[ekspresi_o], -1)
			cv2.putText(img, ekspresi_o, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

			Deteksi_wajah.Db.insert_ciri('ciri_pengujian', ciricv, 'O')
			data_pengujian_o	= Deteksi_wajah.Db.select_first_row()
			id_ciri_pengujian_o = str(data_pengujian_o[0][0])

			# insert pengujian
			data_pengujian 	= {
				'id_file'				: str(id_file),
				'id_ciri_pengujian_o'	: id_ciri_pengujian_o,
				'hasil_opencv'			: ekspresi_o,
				'waktu'					: self.waktu_s
			}
			pengujian = Deteksi_wajah.Db.update_pengujian(data_pengujian)

			# Jarak Setiap Ciri OpenCV

			jarak_bahagia_o = []
			for i in range(7):
				jarak_bahagia_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['bahagia'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'bahagia', jarak_bahagia_o)

			jarak_sedih_o = []
			for i in range(7):
				jarak_sedih_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['sedih'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'sedih', jarak_sedih_o)

			jarak_marah_o = []
			for i in range(7):
				jarak_marah_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['marah'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'marah', jarak_marah_o)

			jarak_jijik_o = []
			for i in range(7):
				jarak_jijik_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['jijik'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'jijik', jarak_jijik_o)

			jarak_kaget_o = []
			for i in range(7):
				jarak_kaget_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['kaget'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'kaget', jarak_kaget_o)

			jarak_takut_o = []
			for i in range(7):
				jarak_takut_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['takut'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'takut', jarak_takut_o)

			jarak_natural_o = []
			for i in range(7):
				jarak_natural_o.append(Deteksi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_o['natural'][i]))
			Deteksi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'natural', jarak_natural_o)

		# select data hasil pengujian openCV dan insert hasil openCV
		hasil_o = Deteksi_wajah.Db.select_hasil('hasil_opencv', str(id_file), self.waktu_s)
		hitung_o = Counter(elem[0] for elem in hasil_o)

		hasil_all_o = {
			'id_file'	: id_file,
			'ket'		: 'O',
			'wajah' 	: len(faces),
			'bahagia'	: hitung_o['bahagia'],
			'sedih'		: hitung_o['sedih'],
			'marah'		: hitung_o['marah'],
			'jijik'		: hitung_o['jijik'],
			'kaget'		: hitung_o['kaget'],
			'takut'		: hitung_o['takut'],
			'natural'	: hitung_o['natural']
		}
		Deteksi_wajah.Db.insert_hasil(hasil_all_o)

		cwd = os.getcwd()
		dir_file_name 	= 'static/data/latih_uji/' + self.waktu_s + '_Hasil_OpenCV.png'
		file_name 		= self.waktu_s + '_Hasil_OpenCV.png'
		cv2.imwrite(dir_file_name, img)

		return file_name


	def deteksi2(self, image, dir1, dir2):
		
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		global face_file_name
		
		for f in faces:
			x, y, w, h = [v for v in f]
			sub_face = img[y:y+h, x:x+w]

			face_file_name = "data/training/" + dir1 + "/" + dir2 + "/" + "01.png"
			cv2.imwrite(face_file_name, sub_face)

		return face_file_name


	def deteksi_single(self, image, directory, ekspresi):
		
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		ekspr = list(self.rectColor.values())

		global face_file_name
		for i, f in enumerate(faces):
			x, y, w, h = np.array([v for v in f], dtype=np.int64)
			sub_face = img[y:y+h, x:x+w]

			face_file_name = 'data/training/' + directory + '/' + str(i) + ".png"
			cv2.imwrite(face_file_name, sub_face)
			
			pra = Praproses()
			sub_face = pra.biner(face_file_name)

			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()
			# print(f"ciri data ke-{i} = {ciri}")
			
			Deteksi_wajah.Db.insert_ciri2("ciri_ck_setara", ekspresi, ciri)


		cwd = os.getcwd()
		dir_file_name = 'static\\data\\training\\'+ directory + ' Hasil.png'
		file_name = directory + ' Hasil.png'
		cv2.imwrite(dir_file_name, img)

		return file_name


	def deteksi_multi_face2(self, image, directory):
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		ekspr = list(self.rectColor.values())

		global face_file_name

		kumpulan_ciri = Deteksi_wajah.Db.select_ciri('ciri_ck_setara')
		kumpulan_kelas = Deteksi_wajah.Db.select_kelas('ciri_ck_setara')

		rata_rata_ciri = {}
		for kelas in kumpulan_kelas:
			rata_rata_ciri[kelas] = Deteksi_wajah.Db.select_avg('ciri_ck_setara', kelas)
		
		for i, f in enumerate(faces):
			x, y, w, h = np.array([v for v in f], dtype=np.int64)

			sub_face = img[y:y+h, x:x+w]

			face_file_name = 'data/testing/' + directory + '/' + str(i) + '.png'
			cv2.imwrite(face_file_name, sub_face)

			dir_file_name = 'static\\data\\testing\\'+ directory + '_' + str(i) + '.png'
			cv2.imwrite(dir_file_name, sub_face)

			## start - klasifikasi
			
			pra = Praproses()
			sub_face = pra.biner(face_file_name)
			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()

			momen = cv2.moments(sub_face)
			ciricv = cv2.HuMoments(momen).flatten()
			
			kl 			= Klasifikasi(kumpulan_ciri, kumpulan_kelas)			
			ekspresi 	= kl.classify([ciri])
			print(f"Ekspresi = {ekspresi}")

			cv2.rectangle(img, (x,y), (x+w, y+h), self.rectColor[ekspresi])
			cv2.rectangle(img, (x, y - 30), (x + 100, y), self.rectColor[ekspresi], -1)
			cv2.putText(img, ekspresi, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
			
			#simpan gambar yang telah dilabel, dicrop

			distance = Deteksi_wajah.distance(rata_rata_ciri[ekspresi], ciri)

			Deteksi_wajah.Db.insert_ciri_pengujian("ciri_pengujian", ekspresi, ciri)
			data_satu = Deteksi_wajah.Db.select_first_row()
			id_tes = data_satu[0][0]

			jarak_natural	= Deteksi_wajah.distance(rata_rata_ciri['natural'], ciri)
			jarak_bahagia 	= Deteksi_wajah.distance(rata_rata_ciri['bahagia'], ciri)
			jarak_sedih		= Deteksi_wajah.distance(rata_rata_ciri['sedih'], ciri)
			jarak_jijik		= Deteksi_wajah.distance(rata_rata_ciri['jijik'], ciri)
			jarak_marah		= Deteksi_wajah.distance(rata_rata_ciri['marah'], ciri)
			jarak_takut		= Deteksi_wajah.distance(rata_rata_ciri['takut'], ciri)
			jarak_kaget		= Deteksi_wajah.distance(rata_rata_ciri['kaget'], ciri)
			
			data_jarak = np.array([jarak_marah, jarak_jijik, jarak_takut, jarak_bahagia, jarak_sedih, jarak_kaget, jarak_natural])

			Deteksi_wajah.Db.insert_jarak(data_jarak, id_tes)

			id_tes 		= str(id_tes)
			jarak_min 	= Deteksi_wajah.Db.insert_jarak_min(id_tes, data_jarak)
			print(f"Jarak min = {jarak_min}")

			jarak = {
				'marah'		: jarak_marah,
				'sedih'		: jarak_sedih,
				'takut'		: jarak_takut,
				'jijik'		: jarak_jijik,
				'kaget'		: jarak_kaget,
				'bahagia'	: jarak_bahagia,
				'jarak_min'	: jarak_min
			}

			ciri = np.array(ciri)
			# print(f"Ciri Data Uji = {ciri}")
			# print(f"Rata-rata ciri {ekspresi} = {rata_rata_ciri[ekspresi]}")
			# print(f"Jarak ciri = {distance}")
			# print("______")
			print(f"Ciri GMI: {ciri}")
			print(f"Ciri CV: {ciricv}")

			error = self.hitung_error(ciricv, ciri)

			print('________________________________________')
			print(f"Momen CV: {momen}")
			print(f"Tipe Momen CV: {type(momen['m00'])}")
			x = momen['m10']/momen['m00']
			y = momen['m01']/momen['m00']
			print(f"Xbar = {x}")
			print(f"Ybar = {y}")

			# print(f"Jarak GMI - CV: {Deteksi_wajah.distance(ciri, ciricv)}")

			# end - klasifikasi

		cwd = os.getcwd()
		dir_file_name = 'static\\data\\testing\\'+ directory + ' Hasil.png'
		file_name = directory + ' Hasil.png'
		cv2.imwrite(dir_file_name, img)

		return file_name, jarak, ciri, ciricv, rata_rata_ciri

	def distance(data1, data2):
		data1 = np.array(data1)
		data2 = np.array(data2)
		return np.linalg.norm(data1 - data2)

	def hitung_jarak(data1, data2):
		return abs(data1-data2)

	def hitung_error(self, data1, data2):
		# MAE (Mean Absolute Error)
		E = (np.sum(np.abs(data1 - data2)) )/ 7
		print(f"Nilai Mean Absolute Error = {E}")


