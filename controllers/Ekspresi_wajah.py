from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
from jinja2 import TemplateNotFound
import numpy as np
import zipfile
from time import gmtime, strftime
import os
from werkzeug.utils import secure_filename

from libs.Deteksi_wajah import Deteksi_wajah
from libs.GMI import GMI
from models.Database import Database
from libs.Klasifikasi import Klasifikasi

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
	def pelatihan_pengujian():
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

					if dir2 == "multiple_face":
						ekspresi = Ekspresi_wajah.Dw.deteksi_multi_face(berkas, directory)

					# openCV
					berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, directory, dir2)

					im 			= Image.open(berkas_citra)
					im			= im.convert('L')
					im 			= np.array(im)

					grayscale 	= Image.fromarray(im)
					threshold 	= 256 / 2
					binary 		= grayscale.point(lambda p: p > threshold and 255)
					binary.save('result/'+ file +'.png')
					pixel_binary= np.array(binary)

					gmi 		= GMI(pixel_binary) 
					gmi.hitungMomenNormalisasi()
					ciri 		= gmi.hitungCiri()
					kelas 		= jenis_kelas

					Ekspresi_wajah.Db.insert_ciri("ciri", kelas, ciri)

			flash('Data berhasil dilatih dan diuji')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})





	@page.route(f'{base}/pelatihan', methods=['GET', 'POST'])
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

					im 			= Image.open(berkas_citra)
					im			= im.convert('L')
					im 			= np.array(im)

					grayscale 	= Image.fromarray(im)
					threshold 	= 256 / 2
					binary 		= grayscale.point(lambda p: p > threshold and 255)
					binary.save('result/'+ file +'.png')
					pixel_binary= np.array(binary)

					gmi 		= GMI(pixel_binary) 
					gmi.hitungMomenNormalisasi()
					ciri 		= gmi.hitungCiri()
					kelas 		= jenis_kelas

					Ekspresi_wajah.Db.insert_ciri("ciri", kelas, ciri)

			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

	@page.route(f'{base}/pengujian', methods=['GET', 'POST'])
	def pengujian():
		hitung = 0

		if request.method == "POST":
			f = request.files['foto']
			
			directory = strftime("%Y-%m-%d-%H-%M-%S")

			# nama_file = f.filename

			# if nama_file.endswith('.png')
			# 	filename = 'data/testing/'+ directory + '/' + nama_file
			# 	f.save(filename)

			# elif nama_file.endswith('.jpg')
			# 	filename = 'data/testing/'+ directory + '/' + nama_file
			# 	f.save(filename)

			filename = 'data\\testing\\' + secure_filename(directory + '_' + f.filename)
			f.save(filename)

			os.makedirs(f'data/testing/{directory}')

			cwd = os.getcwd()

			# berkas 	= cwd + '\\' + filename
			berkas 		= cwd + '\\data\\testing\\' + secure_filename(directory + '_' + f.filename)
			print(berkas)

			# if not os.path.exists(cwd + "\\data\\testing\\" + directory + "\\coba"):
			# 	os.makedirs(cwd + "\\data\\testing\\" + directory + "\\coba")
			# 	print(cwd + "\\data\\testing\\" + directory + "\\coba")

			ekspresi = Ekspresi_wajah.Dw.deteksi_multi_face(berkas, directory)
			print(f'ini ekspresi : {ekspresi}')  

			# im 			= Image.open(berkas_citra)
			# im			= im.convert('L')
			# im 			= np.array(im)

			# grayscale 	= Image.fromarray(im)
			# threshold 	= 256 / 2
			# binary 		= grayscale.point(lambda p: p > threshold and 255)
			# pixel_binary= np.array(binary)

			# gmi 		= GMI(pixel_binary) 
			# gmi.hitungMomenNormalisasi()
			# ciri 		= gmi.hitungCiri()

			# Klasifikasi dengan Multi-SVM
			# kumpulan_ciri = Ekspresi_wajah.Db.select_ciri('ciri')
			# kumpulan_kelas= Ekspresi_wajah.Db.select_kelas('ciri')
			
			# kl 			= Klasifikasi(kumpulan_ciri, kumpulan_kelas)			
			# hitung 		= kl.classify([ciri])

			# flash('Data berhasil diuji!')			

		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'}, hasil = ekspresi )


	@page.route(f'{base}/cob', methods=['GET', 'POST'])
	def cob():
		Ekspresi_wajah.Dw.deteksi_wajah()

		return "hay"