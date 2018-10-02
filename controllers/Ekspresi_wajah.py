from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
from jinja2 import TemplateNotFound
import numpy as np
import zipfile
from time import gmtime, strftime
import os
from werkzeug.utils import secure_filename
import cv2

from libs.Deteksi_wajah import Deteksi_wajah
from libs.GMI import GMI
from models.Database import Database
from libs.Klasifikasi import Klasifikasi
from libs.Praproses import Praproses

class Ekspresi_wajah:

	page = Blueprint('Ekspresi_wajah_page', __name__, template_folder = 'templates')
	base = '/ekspresi-wajah'
	Db = Database('localhost', 'root', '', 'gmisvm')
	Dw = Deteksi_wajah()

	@page.route(f'{base}/')
	def home():
		try:
			return render_template('home.html')
		except TemplateNotFound:
			abort(404)

	@page.route(f'{base}/pelatihan', methods=['GET', 'POST'])
	def pelatihan():
		if request.method == 'POST':
		
			f = request.files['zip_file']
			filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			f.save(filename)

			directory = strftime("%Y-%m-%d-%H-%M-%S")

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/training/' + directory) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			# pelatihan disini
			dir1 		= os.listdir('data/training/' + directory)
			cwd 		= os.getcwd()

			for i in range(len(dir1)):
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
					berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, directory, dir2)

					pra = Praproses()
					pixel_binary = pra.biner(berkas_citra)

					gmi 		= GMI(pixel_binary) 
					gmi.hitungMomenNormalisasi()
					ciri 		= gmi.hitungCiri()
					kelas 		= jenis_kelas

					Ekspresi_wajah.Db.insert_ciri("ciri_ck_setara", kelas, ciri)

			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

	@page.route(f'{base}/pelatihan2', methods=['GET', 'POST'])
	def pelatihan2():
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

			for i in range(len(dir1)):
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
					berkas_citra = Ekspresi_wajah.Dw.deteksi_single(berkas, directory, jenis_kelas)

			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan2'})

	@page.route(f'{base}/pelatihan3', methods=['GET', 'POST'])
	def pelatihan3():
		if request.method == 'POST':
			# f = request.files['zip_file']
			# filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			# f.save(filename)

			selected_label = request.form.get('label')
			time = strftime("%Y-%m-%d-%H-%M-%S")
			directory = time + '/' + selected_label

			if not os.path.exists('data/training/' + directory):
				os.makedirs('data/training/' + directory)

			# with open(filename, mode = 'r') as file:
			# 	zip_file = zipfile.ZipFile(filename)
			# 	files = [zip_file.extract(fl, 'data/training/' + directory) for fl in zip_file.namelist()]
			# 	zip_file.close()
			# os.remove(filename)
			Ekspresi_wajah.upload_multiple_files('zip_file[]', 'data/training/' + directory)

			# pelatihan disini
			dir1 		= os.listdir('data/training/' + directory)
			cwd 		= os.getcwd()

			for file in dir1:
				berkas = cwd + '\\data\\training\\' + directory + '\\' + file
				face = Ekspresi_wajah.Dw.deteksi(berkas, time, selected_label)
				praproses = Praproses()
				pixel_binary = praproses.biner(face)
				gmi 		= GMI(pixel_binary) 
				gmi.hitungMomenNormalisasi()
				ciri 		= gmi.hitungCiri()
				kelas 		= selected_label

				Ekspresi_wajah.Db.insert_ciri("ciri_ck_setara", kelas, ciri)

			# for i in range(len(dir1)):
			# 	print(i)

			# 	dir2		= os.listdir('data/training/' + directory + '/') [i]
			# 	print("dir 2 = " + dir2)

			# 	jenis_kelas = dir1[i]
			# 	print("jenis kelas = " + jenis_kelas)

			# 	file_name	= os.listdir('data/training/' + directory + '/' + dir2)[0]	
			# 	print("file name = " + file_name)
			# 	files	= os.listdir('data/training/' + directory + '/' + dir2)
			# 	for file in files:

			# 		berkas 		= cwd + '\\data\\training\\' + directory + '\\' + dir2 + '\\' + file

			# 		print("berkas = " + berkas)

			# 		# openCV
			# 		berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, directory, dir2)

			# 		# im 			= Image.open(berkas_citra)
			# 		# im			= im.convert('L')
			# 		# im 			= np.array(im)

			# 		# grayscale 	= Image.fromarray(im)
			# 		# threshold 	= 256 / 2
			# 		# binary 		= grayscale.point(lambda p: p > threshold and 255)
			# 		# binary.save('result/'+ file +'.png')
			# 		# pixel_binary= np.array(binary)

			# 		pra = Praproses()
			# 		pixel_binary = pra.biner(berkas_citra)

			# 		gmi 		= GMI(pixel_binary) 
			# 		gmi.hitungMomenNormalisasi()
			# 		ciri 		= gmi.hitungCiri()
			# 		kelas 		= jenis_kelas

			# 		Ekspresi_wajah.Db.insert_ciri("ciri", kelas, ciri)

			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan3', 'title' : 'Pelatihan'})

	@page.route(f'{base}/pengujian', methods=['GET', 'POST'])
	def pengujian():
		hitung = 0
		ekspresi = ""
		jarak = {}
		ciri = []
		ciricv = []
		rata_rata_ciri = {}
		directory = ""

		if request.method == "POST":
			f = request.files['foto']
			
			directory = strftime("%Y-%m-%d-%H-%M-%S")

			filename = 'data\\testing\\' + secure_filename(directory + '_' + f.filename)
			f.save(filename)

			os.makedirs(f'data/testing/{directory}')

			cwd = os.getcwd()

			berkas 		= cwd + '\\data\\testing\\' + secure_filename(directory + '_' + f.filename)
			print(berkas)

			ekspresi, jarak, ciri, ciricv, rata_rata_ciri = Ekspresi_wajah.Dw.deteksi_multi_face(berkas, directory)
		
		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'}, hasil = ekspresi, jarak = jarak, ciri = ciri, ciricv = ciricv, rata_rata_ciri = rata_rata_ciri, directory = directory)



	@page.route(f'{base}/latih-uji', methods=['GET', 'POST'])
	def latih_uji():
		if request.method == 'POST':
		
			f = request.files['zip_file']
			filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			f.save(filename)

			directory = strftime("%Y-%m-%d-%H-%M-%S")

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/latih_uji/' + directory) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			Ekspresi_wajah.latih(files, directory)

			return redirect(url_for('.latih_uji'))
			

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pelatihan dan Pengujian'})


	def latih(files, directory):
		dir1 		= os.listdir('data/latih_uji/' + directory)
		cwd 		= os.getcwd()

		for i in range(len(dir1)):
			print(i)

			dir2		= os.listdir('data/latih_uji/' + directory + '/') [i]
			print("dir 2 = " + dir2)

			jenis_kelas = dir1[i]
			print("jenis kelas = " + jenis_kelas)

			file_name	= os.listdir('data/latih_uji/' + directory + '/' + dir2)[0]	
			print("file name = " + file_name)
			files	= os.listdir('data/latih_uji/' + directory + '/' + dir2)
			for file in files:

				berkas 		= cwd + '\\data\\latih_uji\\' + directory + '\\' + dir2 + '\\' + file

				print("berkas = " + berkas)

				berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, directory, dir2)

				pra = Praproses()
				pixel_binary = pra.biner(berkas_citra)

				gmi 		= GMI(pixel_binary) 
				gmi.hitungMomenNormalisasi()
				ciri 		= gmi.hitungCiri()
				kelas 		= jenis_kelas
				Ekspresi_wajah.Db.insert_ciri('ciri_pelatihan', kelas, ciri, 'S')

				momen = cv2.moments(pixel_binary)
				ciricv 		= cv2.HuMoments(momen).flatten()

				Ekspresi_wajah.Db.insert_ciri('ciri_pelatihan', kelas, ciricv, 'O')

		return True

	@page.route(f'{base}/uji', methods=['GET', 'POST'])
	def uji():
		hitung = 0
		ekspresi = ""
		jarak = {}
		ciri = []
		ciricv = []
		rata_rata_ciri = {}
		directory = ""

		data_uji = Ekspresi_wajah.Db.select_data_uji()
		jumlah_data = len(data_uji)
		file_name = []
		for i in range(jumlah_data):
			file_name = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], data_uji[i][1])
			file_name = Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], data_uji[i][1])

		print(f"File name = {file_name}")
		# return Ekspresi_wajah.Dw.deteksi_multi_face('bahagia.png')

		return "Ayu Cantik"

		# dir1 		= os.listdir('data/uji/' + directory)
		# cwd 		= os.getcwd()

		# for i in range(len(dir1)):
		# 	print(i)

		# 	dir2		= os.listdir('data/uji/' + directory + '/') [i]
		# 	print("dir 2 = " + dir2)

		# 	jenis_kelas = dir1[i]
		# 	print("jenis kelas = " + jenis_kelas)

		# 	file_name	= os.listdir('data/uji/' + directory + '/' + dir2)[0]	
		# 	print("file name = " + file_name)
		# 	files	= os.listdir('data/uji/' + directory + '/' + dir2)
		# 	for file in files:

		# 		berkas 		= cwd + '\\data\\uji\\' + directory + '\\' + dir2 + '\\' + file

		# 		print("berkas = " + berkas)

		# 		berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, directory, dir2)

		# 		pra = Praproses()
		# 		pixel_binary = pra.biner(berkas_citra)

		# 		gmi 		= GMI(pixel_binary) 
		# 		gmi.hitungMomenNormalisasi()
		# 		ciri 		= gmi.hitungCiri()
		# 		kelas 		= jenis_kelas

		# 		Ekspresi_wajah.Db.insert_ciri("ciri_pengujian", kelas, ciri)

		# if request.method == "POST":
		# 	f = request.files['foto']
			
		# 	directory = strftime("%Y-%m-%d-%H-%M-%S")

		# 	filename = 'data\\testing\\' + secure_filename(directory + '_' + f.filename)
		# 	f.save(filename)

		# 	os.makedirs(f'data/testing/{directory}')

		# 	cwd = os.getcwd()

		# 	berkas 		= cwd + '\\data\\testing\\' + secure_filename(directory + '_' + f.filename)
		# 	print(berkas)

		# 	ekspresi, jarak, ciri, ciricv, rata_rata_ciri = Ekspresi_wajah.Dw.deteksi_multi_face(berkas, directory)
		
		# return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'}, hasil = ekspresi, jarak = jarak, ciri = ciri, ciricv = ciricv, rata_rata_ciri = rata_rata_ciri, directory = directory)