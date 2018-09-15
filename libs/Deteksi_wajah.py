from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
import cv2, numpy as np, random
from libs.GMI import GMI
from libs.Praproses import Praproses
from models.Database import Database
from libs.Klasifikasi import Klasifikasi
import MySQLdb
import os


class Deteksi_wajah:

	page = Blueprint('Deteksi_wajah_page', __name__, template_folder = 'templates')
	base = '/deteksi-wajah'
	Db 	 = Database('localhost', 'root', '', 'gmisvm')

	def __init__(self):
		self.rectColor = {
			'bahagia': (0, 153, 204),
			'sedih': (51, 51, 51),
			'jijik': (51, 153, 0),
			'takut': (0, 0, 0),
			'natural': (255, 255, 255),
			'marah': (255, 0, 0)
		}

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

	def deteksi_wajah(self):
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

	# @page.route(f'{base}/')
	def deteksi(self, image, dir1, dir2):
		
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		global face_file_name
		
		for f in faces:
			x, y, w, h = [v for v in f]
			cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255))
			sub_face = img[y:y+h, x:x+w]

			face_file_name = "data/training/" + dir1 + "/" + dir2 + "/" + "01.jpg"
			cv2.imwrite(face_file_name, sub_face)

		return face_file_name


	def deteksi_multi_face(self, image, directory):
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		ekspr = list(self.rectColor.values())

		global face_file_name
		for i, f in enumerate(faces):
			x, y, w, h = np.array([v for v in f], dtype=np.int64)

			# color = random.choice(ekspr)
			# print(color)
			# cv2.rectangle(img, (x,y), (x+w, y+h), color)
			sub_face = img[y:y+h, x:x+w]

			face_file_name = 'data/testing/' + directory + '/' + str(i) + ".png"
			cv2.imwrite(face_file_name, sub_face)

			## start - klasifikasi
			
			pra = Praproses()
			sub_face = pra.biner(face_file_name)
			print(f"Praproses = {sub_face}")

			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()

			kumpulan_ciri = Deteksi_wajah.Db.select_ciri('ciri')
			kumpulan_kelas= Deteksi_wajah.Db.select_kelas('ciri')
			
			kl 			= Klasifikasi(kumpulan_ciri, kumpulan_kelas)			
			ekspresi 	= kl.classify([ciri])
			print(f'Klasifikasi = {ekspresi}')

			cv2.rectangle(img, (x,y), (x+w, y+h), self.rectColor[ekspresi]) 
			
			Ekspresi_wajah.Db.insert_ciri("ciri", kelas, ciri)
			# end - klasifikasi

		cwd = os.getcwd()
		dir_file_name = 'static\\data\\testing\\'+ directory + ' Hasil.png'
		file_name = directory + ' Hasil.png'
		cv2.imwrite(dir_file_name, img)

		# file = cwd + file_name

		return file_name

