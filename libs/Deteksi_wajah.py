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

	def deteksi_wajah(self):
		# Praproses Ke Gray Scale

		image = "D:\\bahagia.png"

		im = self.resize_image(image)

		print(im)

		# im 	= Image.open(image)
		# im	= im.convert('L') 
		# im 	= np.array(im)

		# im = np.array([
		# 	[1, 2, 3],
		# 	[2, 3, 4],
		# 	[4, 5, 1]
		# ])

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

