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

			ekspresi, jarak, ciri, ciricv, rata_rata_ciri = Ekspresi_wajah.Dw.deteksi_multi_face2(berkas, directory)
		
		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'}, hasil = ekspresi, jarak = jarak, ciri = ciri, ciricv = ciricv, rata_rata_ciri = rata_rata_ciri, directory = directory)



	@page.route(f'{base}/latih-uji', methods=['GET', 'POST'])
	def latih_uji(): 
		file_hasil = []

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
			file_hasil = Ekspresi_wajah.uji()
			flash('Data berhasil dilatih dan diuji!')

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pelatihan dan Pengujian'}, hasil = file_hasil)


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
				Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciri, 'S')

				momen = cv2.moments(pixel_binary)
				ciricv 		= cv2.HuMoments(momen).flatten()

				Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciricv, 'O')

		return True

	def uji():
		jarak_s = {}
		jarak_o = {}
		jarak = {}
		files = {}
		file_name_s = []
		file_name_o = []

		data_uji 	= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data = len(data_uji)
		file_name 	= []
		for i in range(jumlah_data):
			file_name_s, jarak_s = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], data_uji[i][1])
			file_name_o, jarak_o = Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], data_uji[i][1])

		
		print(f"file name = {file_name_s} dan tipe = {type(file_name_s)}")
		print(f"file name len = {len(file_name_s)} dan tipe = {type(file_name_s)}")


		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o
		}

		jarak = {
			'jarak_all_s'			: jarak_s,
			'jumlah_jarak_all_s'	: len(jarak_s),
			'jarak_all_o'			: jarak_o,
			'jumlah_jarak_all_o'	: len(jarak_o)  
		}

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files)

	def uji2():
		jarak_s = {}
		jarak_o = {}
		jarak = {}
		files = {}
		file_name_s = []
		file_name_o = []

		data_uji = Ekspresi_wajah.Db.select_data_uji()
		jumlah_data = len(data_uji)
		file_name = []
		for i in range(jumlah_data):
			file_name.append(Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], data_uji[i][1]))
			file_name.append(Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], data_uji[i][1]))

		print(f"File name = {file_name} dan tipe = {type(file_name)}")

		return file_name
	

	@page.route(f'{base}/lakukan-uji', methods=['GET', 'POST'])
	def lakukan_uji():
		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_s 	= []
		file_name_o 	= []
		directory 		= []
		hasil_all_s 	= []
		hasil_final_s 	= []
		hasil_all_o 	= []
		hasil_final_o 	= []
		target 			= []

		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		# print(f"Data uji = {data_uji} dan tipe = {type(data_uji)}") 
		# print(f"Data uji1 = {data_uji[1]} dan tipe = {type(data_uji[1])}")
		# print(f"Data uji w = {data_uji[1][2]} dan tipe = {type(data_uji[1][2])}")

		jumlah_data = len(data_uji)

		for i in range(jumlah_data):
			file_name__s, jarak_s, directory, hasil_all_s = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], data_uji[i][1])
			file_name_s.append(file_name__s)
			hasil_final_s.append({
				'WS'	: hasil_all_s['wajah'],
				'B'		: hasil_all_s['bahagia'],
				'S'		: hasil_all_s['sedih'],
				'M'		: hasil_all_s['marah'],
				'J'		: hasil_all_s['jijik'],
				'K'		: hasil_all_s['kaget'],
				'T'		: hasil_all_s['takut'],
				'N'		: hasil_all_s['natural']
			})
 
			file_name_o, jarak_o, hasil_all_o= Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], data_uji[i][1], directory)
			hasil_final_o.append({
				'WO'	: hasil_all_o['wajah'],
				'B'		: hasil_all_o['bahagia'],
				'S'		: hasil_all_o['sedih'],
				'M'		: hasil_all_o['marah'],
				'J'		: hasil_all_o['jijik'],
				'K'		: hasil_all_o['kaget'],
				'T'		: hasil_all_o['takut'],
				'N'		: hasil_all_o['natural']
			})

		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o,
			'jumlah_data'			: jumlah_data,
			'data_uji'				: data_uji
		}

		# print(f"File = {files['file_s']} dan tipe = {type(files['file_s'])}")
		# print(f"File pertama = {files['file_s'][0]} dan tipe = {type(files['file_s'][0])}")

		jarak = {
			'jarak_all_s'			: jarak_s,
			'jumlah_jarak_all_s'	: len(jarak_s),
			'jarak_all_o'			: jarak_o,
			'jumlah_jarak_all_o'	: len(jarak_o)  
		}

		# print(f"Hasil all = {hasil_final_s} dan tipe = {type(hasil_final_s)}")
		# print(f"Hasil all = {hasil_final_s[0]} dan tipe = {type(hasil_final_s[0])}")
		# print(f"Jumlah hasil all = {len(hasil_final_s)} ")
		# print(f"Jumlah hasil all s = {len(hasil_final_s[0])} ")


		for i in range(jumlah_data):
			target.append({
				'WT'	: data_uji[i][2],
				'B'		: data_uji[i][3],
				'S'		: data_uji[i][4],
				'M'		: data_uji[i][5],
				'J'		: data_uji[i][6],
				'K'		: data_uji[i][7],
				'T'		: data_uji[i][8],
				'N'		: data_uji[i][9]
			})

		# for i in range(jumlah_data):
		# 	for key, value in target[i].items():
		# 		if value != 0:
		# 			y = key + '=' + str(value)
		# 			h.update(y)  

		# print(f"H all = {h} dan tipe = {type(h)}")

		# print(f"Target = {target} dan tipe = {type(target)}")
		# print(f"Len Target = {len(target)}")
		# print(f"Target 0= {target[0]} dan tipe = {type(target[0])}")	
		# print(f"Target ke-0 = {target[0]['WT']} dan tipe = {type(target[0]['WT'])}")	

		# for i in range(len(target)):
		# 	for key, value in target[i].items():
		# 		if value != 0:
		# 			data_target_uji = key + ':' + str(value)
	
		# print(f"Target data = {data_target_uji} dan tipe = {type(data_target_uji)}")
		# print(f"Target data 0= {data_target_uji[0]} dan tipe = {type(data_target_uji)[0]}")


		# print(f"Jarak all s = {jarak} dan tipe = {type(jarak)}")
		# print(f"Jarak bahagia jmlh = {jarak['jumlah_jarak_all_s']} dan tipe = {type(jarak['jumlah_jarak_all_s'])}")

		# print(f"Jarak [0]= {jarak['jarak_all_s'][0]} dan tipe = {type(jarak['jarak_all_s'][0])}")
		# print(f"Jarak bahagia = {jarak['jarak_all_s'][0]['bahagia']} dan tipe = {type(jarak['jarak_all_s'][0]['bahagia'])}")

		# print(f"File = {files} dan tipe = {type(files)}")
		# print(f"File jmlh = {files['jumlah_file_name_s']} dan tipe = {type(files['jumlah_file_name_s'])}")

		# print(f"File-file = {files['file']} dan tipe = {type(files['file'])}")
		# print(f"File-file = {files['file'][0]} dan tipe = {type(files['file'][0])}")

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, hasil_all_s = hasil_final_s, hasil_all_o = hasil_final_o)

	@page.route(f'{base}/hasil', methods=['GET', 'POST'])
	def hasil():
		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'})

	@page.route(f'{base}/hasil_detail', methods=['GET', 'POST'])
	def hasil_detail():
		return render_template('layout.html', data = { 'view' : 'detail', 'title' : 'Pengujian dan Pelatihan'})