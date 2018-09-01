from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image


class Deteksi_wajah:

	page = Blueprint('Deteksi_wajah_page', __name__, template_folder = 'templates')
	base = '/deteksi-wajah'


	# @page.route(f'{base}/')
	def index(proses, image, dir1, dir2):
		
		face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

		img = cv2.imread(image)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		global face_file_name
		
		for f in faces:
			x, y, w, h = [v for v in f]
			cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255))
			sub_face = img[y:y+h, x:x+w]

			face_file_name = "data/" + proses + "/" + dir1 + "/" + dir2 + "/" + "01.jpg"
			cv2.imwrite(face_file_name, sub_face)

		return face_file_name


	@page.route(f'{base}/login')
	def login():
		return 'login nih'

