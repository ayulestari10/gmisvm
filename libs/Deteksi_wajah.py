from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
import cv2, numpy as np, random


class Deteksi_wajah:

	page = Blueprint('Deteksi_wajah_page', __name__, template_folder = 'templates')
	base = '/deteksi-wajah'

	def __init__(self):
		self.rectColor = {
			'bahagia': (0, 153, 204),
			'sedih': (51, 51, 51),
			'jijik': (51, 153, 0),
			'takut': (0, 0, 0),
			'natural': (255, 255, 255),
			'marah': (255, 0, 0)
		}

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
			## ekspresi = classifier.predict(face_file_name)



			## end - klasifikasi

			# cv2.rectangle(img, (x,y), (x+w, y+h), self.rectColor[ekspresi]) 

			# return face_file_name




			
		cv2.imwrite(f'data/testing/{directory}/img.jpg', img)

