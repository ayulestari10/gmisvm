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
from libs.OpenCV import OpenCV

class Ekspresi_wajah:

	page 	= Blueprint('Ekspresi_wajah_page', __name__, template_folder = 'templates')
	base 	= '/ekspresi-wajah'
	Db 		= Database('localhost', 'root', '', 'gmisvm')
	Dw 		= Deteksi_wajah()
	pra 	= Praproses()
	OC 		= OpenCV()

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

			direktori = strftime("%Y-%m-%d-%H-%M-%S")

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/training/' + direktori) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			# pelatihan disini
			dir1 		= os.listdir('data/training/' + direktori)
			cwd 		= os.getcwd()

			for i in range(len(dir1)):
				print(i)

				dir2		= os.listdir('data/training/' + direktori + '/') [i]
				print("dir 2 = " + dir2)

				jenis_kelas = dir1[i]
				print("jenis kelas = " + jenis_kelas)

				file_name	= os.listdir('data/training/' + direktori + '/' + dir2)[0]	
				print("file name = " + file_name)
				files	= os.listdir('data/training/' + direktori + '/' + dir2)
				for file in files:

					# berkas 		= cwd + '\\data\\training\\' + direktori + '\\' + dir2 + '\\' + file

					print(f"file pelatihan single = {file}")
					Ekspresi_wajah.latih(file, 'training', direktori)

			flash('Ciri data pelatihan berhasil disimpan!')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

	@page.route(f'{base}/pelatihan2', methods=['GET', 'POST'])
	def pelatihan2():
		if request.method == 'POST':
		
			f = request.files['zip_file']
			filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			f.save(filename)

			direktori = strftime("%Y-%m-%d-%H-%M-%S")

			# if not os.path.exists(direktori):
			# 	os.makedirs(direktori)

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/training/' + direktori) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			# pelatihan disini
			dir1 		= os.listdir('data/training/' + direktori)
			cwd 		= os.getcwd()

			for i in range(len(dir1)):
				print(i)

				dir2		= os.listdir('data/training/' + direktori + '/') [i]
				print("dir 2 = " + dir2)

				jenis_kelas = dir1[i]
				print("jenis kelas = " + jenis_kelas)

				file_name	= os.listdir('data/training/' + direktori + '/' + dir2)[0]	
				print("file name = " + file_name)
				files	= os.listdir('data/training/' + direktori + '/' + dir2)
				for file in files:

					berkas 		= cwd + '\\data\\training\\' + direktori + '\\' + dir2 + '\\' + file

					print("berkas = " + berkas)

					# openCV
					berkas_citra = Ekspresi_wajah.Dw.deteksi_single(berkas, direktori, jenis_kelas)

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
			direktori = time + '/' + selected_label

			if not os.path.exists('data/training/' + direktori):
				os.makedirs('data/training/' + direktori)

			# with open(filename, mode = 'r') as file:
			# 	zip_file = zipfile.ZipFile(filename)
			# 	files = [zip_file.extract(fl, 'data/training/' + direktori) for fl in zip_file.namelist()]
			# 	zip_file.close()
			# os.remove(filename)
			Ekspresi_wajah.upload_multiple_files('zip_file[]', 'data/training/' + direktori)

			# pelatihan disini
			dir1 		= os.listdir('data/training/' + direktori)
			cwd 		= os.getcwd()

			for file in dir1:
				berkas = cwd + '\\data\\training\\' + direktori + '\\' + file
				face = Ekspresi_wajah.Dw.deteksi('training', berkas, time, selected_label)
				praproses = Praproses()
				piksel_biner = praproses.biner(face)
				gmi 		= GMI(piksel_biner) 
				gmi.hitungMomenNormalisasi()
				ciri 		= gmi.hitungCiri()
				kelas 		= selected_label

				Ekspresi_wajah.Db.insert_ciri("ciri_ck_setara", kelas, ciri)

			# for i in range(len(dir1)):
			# 	print(i)

			# 	dir2		= os.listdir('data/training/' + direktori + '/') [i]
			# 	print("dir 2 = " + dir2)

			# 	jenis_kelas = dir1[i]
			# 	print("jenis kelas = " + jenis_kelas)

			# 	file_name	= os.listdir('data/training/' + direktori + '/' + dir2)[0]	
			# 	print("file name = " + file_name)
			# 	files	= os.listdir('data/training/' + direktori + '/' + dir2)
			# 	for file in files:

			# 		berkas 		= cwd + '\\data\\training\\' + direktori + '\\' + dir2 + '\\' + file

			# 		print("berkas = " + berkas)

			# 		# openCV
			# 		berkas_citra = Ekspresi_wajah.Dw.deteksi(berkas, direktori, dir2)

			# 		# im 			= Image.open(berkas_citra)
			# 		# im			= im.convert('L')
			# 		# im 			= np.array(im)

			# 		# grayscale 	= Image.fromarray(im)
			# 		# threshold 	= 256 / 2
			# 		# binary 		= grayscale.point(lambda p: p > threshold and 255)
			# 		# binary.save('result/'+ file +'.png')
			# 		# piksel_biner= np.array(binary)

			# 		pra = Praproses()
			# 		piksel_biner = pra.biner(berkas_citra)

			# 		gmi 		= GMI(piksel_biner) 
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
		direktori = ""

		if request.method == "POST":
			f = request.files['foto']
			
			direktori = strftime("%Y-%m-%d-%H-%M-%S")

			filename = 'data\\testing\\' + secure_filename(direktori + '_' + f.filename)
			f.save(filename)

			os.makedirs(f'data/testing/{direktori}')

			cwd = os.getcwd()

			berkas 		= cwd + '\\data\\testing\\' + secure_filename(direktori + '_' + f.filename)
			print(berkas)

			ekspresi, ciri, ciricv = Ekspresi_wajah.Dw.deteksi_multi_face2(berkas, direktori)
		
		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'}, hasil = ekspresi, ciri = ciri, ciricv = ciricv)

	@page.route(f'{base}/coba', methods=['POST'])
	def coba():
		wkwk = request.form['wkwk']
		return 'data yang anda kirim: ' + wkwk


	@page.route(f'{base}/latih-uji', methods=['GET', 'POST'])
	def latih_uji(): 
		file_hasil = []
		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_s 	= []
		file_name_o 	= []
		semua_hasil_s 	= []
		hasil_final_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		waktu 			= []
		akurasi 		= {}

		if request.method == 'POST':
		
			f = request.files['zip_file']
			filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			f.save(filename)

			direktori = strftime("%Y-%m-%d-%H-%M-%S")

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/latih_uji/' + direktori) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			Ekspresi_wajah.latih(files, 'latih_uji', direktori)
			jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi = Ekspresi_wajah.uji()

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = hasil_final_s, semua_hasil_o = hasil_final_o, waktu = waktu, akurasi = akurasi)


	def latih(files, ket, direktori):
		dir1 		= os.listdir('data/'+ ket +'/' + direktori)
		cwd 		= os.getcwd()

		for i in range(len(dir1)):

			dir2			= os.listdir('data/'+ ket +'/' + direktori + '/') [i]
			jenis_kelas	 	= dir1[i]
			file_name		= os.listdir('data/'+ ket +'/' + direktori + '/' + dir2)[0]	
			files			= os.listdir('data/'+ ket +'/' + direktori + '/' + dir2)
			
			for file in files:

				berkas 		= cwd + '\\data\\'+ ket +'\\' + direktori + '\\' + dir2 + '\\' + file
				path 		= Ekspresi_wajah.Dw.resize_image(berkas, file, direktori, dir2)
				berkas_citra= Ekspresi_wajah.Dw.deteksi(ket, path, direktori, dir2)
				piksel_biner= Ekspresi_wajah.pra.biner(berkas_citra)

				gmi 		= GMI(piksel_biner) 
				gmi.hitungMomenNormalisasi()
				ciri 		= gmi.hitungCiri()
				kelas 		= jenis_kelas
				Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciri, 'S')

				ciricv 		= Ekspresi_wajah.OC.gmi_OpenCV(piksel_biner)

				Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciricv, 'O')
		return True


	def uji():
		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_s 	= []
		file_name_o 	= []
		semua_hasil_s 	= []
		hasil_final_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		waktu			= []
		cwd				= os.getcwd()
		dirr 			= cwd + '\\data\\uji\\'

		for i in range(jumlah_data):
			path  		= dirr + str(data_uji[i][1])
			file_name__s, jarak_s, direktori, semua_hasil_s, id_pengujian_update = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], path, data_uji[i][1])
			file_name_s.append(file_name__s)
			waktu.append(semua_hasil_s['waktu'])
			hasil_final_s.append({
				'WS'	: semua_hasil_s['wajah'],
				'B'		: semua_hasil_s['bahagia'],
				'S'		: semua_hasil_s['sedih'],
				'M'		: semua_hasil_s['marah'],
				# 'J'		: semua_hasil_s['jijik'],
				'K'		: semua_hasil_s['kaget'],
				# 'T'		: semua_hasil_s['takut'],
				# 'N'		: semua_hasil_s['natural']
			})
 
			file_name_o, jarak_o, semua_hasil_o= Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], path, data_uji[i][1], direktori, id_pengujian_update)
			hasil_final_o.append({
				'WO'	: semua_hasil_o['wajah'],
				'B'		: semua_hasil_o['bahagia'],
				'S'		: semua_hasil_o['sedih'],
				'M'		: semua_hasil_o['marah'],
				# 'J'		: semua_hasil_o['jijik'],
				'K'		: semua_hasil_o['kaget'],
				# 'T'		: semua_hasil_o['takut'],
				# 'N'		: semua_hasil_o['natural']
			})

		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o,
			'jumlah_data'			: jumlah_data,
			'data_uji'				: data_uji
		}

		jarak = {
			'jarak_all_s'			: jarak_s,
			'jumlah_jarak_all_s'	: len(jarak_s),
			'jarak_all_o'			: jarak_o,
			'jumlah_jarak_all_o'	: len(jarak_o)  
		}

		for i in range(jumlah_data):
			target.append({
				'WT'	: data_uji[i][2],
				'B'		: data_uji[i][3],
				'S'		: data_uji[i][4],
				'M'		: data_uji[i][5],
				# 'J'		: data_uji[i][6],
				'K'		: data_uji[i][7],
				# 'T'		: data_uji[i][8],
				# 'N'		: data_uji[i][9]
			})

		target_akhir = []
		for i in range(jumlah_data):
			t_a = {}
			for key, value in target[i].items():
				if value != 0:
					t_a[key] = value
			target_akhir.append(t_a) 

		hasil_s = []
		for i in range(jumlah_data):
			h_s = {}
			for key, value in hasil_final_s[i].items():
				if value != 0:
					h_s[key] = value
			hasil_s.append(h_s)

		hasil_o = []
		for i in range(jumlah_data):
			h_o = {}
			for key, value in hasil_final_o[i].items():
				if value != 0:
					h_o[key] = value
			hasil_o.append(h_o)

		akurasi_s = []
		for i in range(jumlah_data):
			a_s = {}
			for key,value in  hasil_s[i].items():
				if key == 'WS':
					a_s[key] = (hasil_s[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_s[i].keys() and x != 'WT':
					a_s[x] 	= 0

			for key,value in hasil_s[i].items():
				if key != 'WS':
					a_s[key] = (hasil_s[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_s.append(a_s)


		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				a_o[key] = (hasil_o[i][key]/data_uji[i][2]) * 100 if data_uji[i][2] != 0 else 0
			akurasi_o.append(a_o)

		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				if key == 'WO':
					a_o[key] = (hasil_o[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_o[i].keys() and x != 'WT':
					a_o[x] 	= 0

			for key,value in hasil_o[i].items():
				if key != 'WO':
					a_o[key] = (hasil_o[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_o.append(a_o)

		jW = 0
		aW = 0
		jB = 0
		aB = 0
		jW = 0
		aS = 0
		jS = 0
		aM = 0
		jM = 0
		aJ = 0
		jJ = 0
		aK = 0
		jK = 0
		aT = 0
		jT = 0
		aN = 0
		jN = 0
		for i in range(jumlah_data):
			for key, value in akurasi_s[i].items():
				if key == 'WS':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_s = {
			'WS'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		for i in range(jumlah_data):
			for key, value in akurasi_o[i].items():
				if key == 'WO':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_o = {
			'WO'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		r_all_s = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_s.items():
				if key in akurasi_s[i].keys():
					v = int(value)
					r_all_s.append(key + '=' + str(v))

		r_all_o = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_o.items():
				if key in akurasi_o[i].keys():
					v = int(value)
					r_all_o.append(key + '=' + str(v))

		akurasi = {
			's'			: akurasi_s,
			'o'			: akurasi_o,
			'rata_s'	: set(r_all_s),
			'rata_o'	: set(r_all_o)
		}

		return jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi



	# ####################################
	

	@page.route(f'{base}/lakukan-uji', methods=['GET', 'POST'])
	def lakukan_uji():
		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_s 	= []
		file_name_o 	= []
		semua_hasil_s 	= []
		hasil_final_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		waktu			= []
		cwd				= os.getcwd()
		dirr 			= cwd + '\\data\\uji\\'

		for i in range(jumlah_data):
			path  		= dirr + str(data_uji[i][1])
			file_name__s, jarak_s, direktori, semua_hasil_s, id_pengujian_update = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], path, data_uji[i][1])
			print(f"id file = {data_uji[i][0]}")
			file_name_s.append(file_name__s)
			waktu.append(semua_hasil_s['waktu'])
			hasil_final_s.append({
				'WS'	: semua_hasil_s['wajah'],
				'B'		: semua_hasil_s['bahagia'],
				'S'		: semua_hasil_s['sedih'],
				'M'		: semua_hasil_s['marah'],
				# 'J'		: semua_hasil_s['jijik'],
				'K'		: semua_hasil_s['kaget'],
				# 'T'		: semua_hasil_s['takut'],
				# 'N'		: semua_hasil_s['natural']
			})
 
			file_name_o, jarak_o, semua_hasil_o= Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], path, data_uji[i][1], direktori, id_pengujian_update)
			hasil_final_o.append({
				'WO'	: semua_hasil_o['wajah'],
				'B'		: semua_hasil_o['bahagia'],
				'S'		: semua_hasil_o['sedih'],
				'M'		: semua_hasil_o['marah'],
				# 'J'		: semua_hasil_o['jijik'],
				'K'		: semua_hasil_o['kaget'],
				# 'T'		: semua_hasil_o['takut'],
				# 'N'		: semua_hasil_o['natural']
			})

		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o,
			'jumlah_data'			: jumlah_data,
			'data_uji'				: data_uji
		}

		jarak = {
			'jarak_all_s'			: jarak_s,
			'jumlah_jarak_all_s'	: len(jarak_s),
			'jarak_all_o'			: jarak_o,
			'jumlah_jarak_all_o'	: len(jarak_o)  
		}

		for i in range(jumlah_data):
			target.append({
				'WT'	: data_uji[i][2],
				'B'		: data_uji[i][3],
				'S'		: data_uji[i][4],
				'M'		: data_uji[i][5],
				# 'J'		: data_uji[i][6],
				'K'		: data_uji[i][7],
				# 'T'		: data_uji[i][8],
				# 'N'		: data_uji[i][9]
			})

		target_akhir = []
		for i in range(jumlah_data):
			t_a = {}
			for key, value in target[i].items():
				if value != 0:
					t_a[key] = value
			target_akhir.append(t_a) 

		hasil_s = []
		for i in range(jumlah_data):
			h_s = {}
			for key, value in hasil_final_s[i].items():
				if value != 0:
					h_s[key] = value
			hasil_s.append(h_s)

		hasil_o = []
		for i in range(jumlah_data):
			h_o = {}
			for key, value in hasil_final_o[i].items():
				if value != 0:
					h_o[key] = value
			hasil_o.append(h_o)

		akurasi_s = []
		for i in range(jumlah_data):
			a_s = {}
			for key,value in  hasil_s[i].items():
				if key == 'WS':
					a_s[key] = (hasil_s[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_s[i].keys() and x != 'WT':
					a_s[x] 	= 0

			for key,value in hasil_s[i].items():
				if key != 'WS':
					a_s[key] = (hasil_s[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_s.append(a_s)


		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				a_o[key] = (hasil_o[i][key]/data_uji[i][2]) * 100 if data_uji[i][2] != 0 else 0
			akurasi_o.append(a_o)

		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				if key == 'WO':
					a_o[key] = (hasil_o[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_o[i].keys() and x != 'WT':
					a_o[x] 	= 0

			for key,value in hasil_o[i].items():
				if key != 'WO':
					a_o[key] = (hasil_o[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_o.append(a_o)

		jW = 0
		aW = 0
		jB = 0
		aB = 0
		jW = 0
		aS = 0
		jS = 0
		aM = 0
		jM = 0
		aJ = 0
		jJ = 0
		aK = 0
		jK = 0
		aT = 0
		jT = 0
		aN = 0
		jN = 0
		for i in range(jumlah_data):
			for key, value in akurasi_s[i].items():
				if key == 'WS':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_s = {
			'WS'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		for i in range(jumlah_data):
			for key, value in akurasi_o[i].items():
				if key == 'WO':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_o = {
			'WO'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		r_all_s = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_s.items():
				if key in akurasi_s[i].keys():
					v = int(value)
					r_all_s.append(key + '=' + str(v))

		r_all_o = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_o.items():
				if key in akurasi_o[i].keys():
					v = int(value)
					r_all_o.append(key + '=' + str(v))

		akurasi = {
			's'			: akurasi_s,
			'o'			: akurasi_o,
			'rata_s'	: set(r_all_s),
			'rata_o'	: set(r_all_o)
		}

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = hasil_final_s, semua_hasil_o = hasil_final_o, waktu = waktu, akurasi = akurasi)



	@page.route(f'{base}/hasil_detail/<int:id_file>/<string:waktu>', methods=['GET', 'POST'])
	def hasil_detail(id_file, waktu):

		data_pengujian 	= Ekspresi_wajah.Db.select_data_pengujian(id_file, waktu)
		jumlah_wajah 	= len(data_pengujian)
		ciri_all_s 		= []
		ciri_all_o 		= []

		for i in range(jumlah_wajah):
			print(f"_____ {data_pengujian[0][2]}")
			ciri_s = Ekspresi_wajah.Db.select_ciri_pengujian(data_pengujian[i][2], 'S')
			ciri_all_s.append(ciri_s)

			ciri_o = Ekspresi_wajah.Db.select_ciri_pengujian(data_pengujian[i][3], 'O')
			ciri_all_o.append(ciri_o) 

		return render_template('layout.html', data = { 'view' : 'detail', 'title' : 'Pengujian dan Pelatihan'}, ciri_s = ciri_all_s, ciri_o = ciri_all_o, data_pengujian = data_pengujian)


	@page.route(f'{base}/uji_data', methods=['GET', 'POST'])
	def uji_data():
		# if request.method == 'POST':
		# jumlah = request.form['jumlah']

		jumlah 		= [3, 2, 1]
		kum_ekspresi= ['Bahagia', 'Sedih']
		data_latih 	= []

		# jumlah * setiap kelas
		for i in range(len(jumlah)):
			a = []
			for j in range(len(kum_ekspresi)):
				print(f"Ekspresi_wajah.Db.select_sejumlah_data_latih('S', {kum_ekspresi[j]}, {jumlah[i]})")
				a.extend(Ekspresi_wajah.Db.select_sejumlah_data_latih('S', kum_ekspresi[j], jumlah[i]))
			print(f"j a = {len(a)}")
			data_latih.append(a) 

		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_s 	= []
		file_name_o 	= []
		semua_hasil_s 	= []
		hasil_final_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		waktu			= []
		cwd				= os.getcwd()
		dirr 			= cwd + '\\data\\uji\\'

		for i in range(jumlah_data):
			path  		= dirr + str(data_uji[i][1])
			file_name__s, jarak_s, direktori, semua_hasil_s, id_pengujian_update = Ekspresi_wajah.Dw.deteksi_multi_face_sendiri(data_uji[i][0], path, data_uji[i][1])
			print(f"id file = {data_uji[i][0]}")
			file_name_s.append(file_name__s)
			waktu.append(semua_hasil_s['waktu'])
			hasil_final_s.append({
				'WS'	: semua_hasil_s['wajah'],
				'B'		: semua_hasil_s['bahagia'],
				'S'		: semua_hasil_s['sedih'],
				'M'		: semua_hasil_s['marah'],
				# 'J'		: semua_hasil_s['jijik'],
				'K'		: semua_hasil_s['kaget'],
				# 'T'		: semua_hasil_s['takut'],
				# 'N'		: semua_hasil_s['natural']
			})
 
			file_name_o, jarak_o, semua_hasil_o= Ekspresi_wajah.Dw.deteksi_multi_face_opencv(data_uji[i][0], path, data_uji[i][1], direktori, id_pengujian_update)
			hasil_final_o.append({
				'WO'	: semua_hasil_o['wajah'],
				'B'		: semua_hasil_o['bahagia'],
				'S'		: semua_hasil_o['sedih'],
				'M'		: semua_hasil_o['marah'],
				# 'J'		: semua_hasil_o['jijik'],
				'K'		: semua_hasil_o['kaget'],
				# 'T'		: semua_hasil_o['takut'],
				# 'N'		: semua_hasil_o['natural']
			})

		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o,
			'jumlah_data'			: jumlah_data,
			'data_uji'				: data_uji
		}

		jarak = {
			'jarak_all_s'			: jarak_s,
			'jumlah_jarak_all_s'	: len(jarak_s),
			'jarak_all_o'			: jarak_o,
			'jumlah_jarak_all_o'	: len(jarak_o)  
		}

		for i in range(jumlah_data):
			target.append({
				'WT'	: data_uji[i][2],
				'B'		: data_uji[i][3],
				'S'		: data_uji[i][4],
				'M'		: data_uji[i][5],
				# 'J'		: data_uji[i][6],
				'K'		: data_uji[i][7],
				# 'T'		: data_uji[i][8],
				# 'N'		: data_uji[i][9]
			})

		target_akhir = []
		for i in range(jumlah_data):
			t_a = {}
			for key, value in target[i].items():
				if value != 0:
					t_a[key] = value
			target_akhir.append(t_a) 

		hasil_s = []
		for i in range(jumlah_data):
			h_s = {}
			for key, value in hasil_final_s[i].items():
				if value != 0:
					h_s[key] = value
			hasil_s.append(h_s)

		hasil_o = []
		for i in range(jumlah_data):
			h_o = {}
			for key, value in hasil_final_o[i].items():
				if value != 0:
					h_o[key] = value
			hasil_o.append(h_o)

		akurasi_s = []
		for i in range(jumlah_data):
			a_s = {}
			for key,value in  hasil_s[i].items():
				if key == 'WS':
					a_s[key] = (hasil_s[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_s[i].keys() and x != 'WT':
					a_s[x] 	= 0

			for key,value in hasil_s[i].items():
				if key != 'WS':
					a_s[key] = (hasil_s[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_s.append(a_s)


		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				a_o[key] = (hasil_o[i][key]/data_uji[i][2]) * 100 if data_uji[i][2] != 0 else 0
			akurasi_o.append(a_o)

		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				if key == 'WO':
					a_o[key] = (hasil_o[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0

			for x, y in target_akhir[i].items():
				if x not in hasil_o[i].keys() and x != 'WT':
					a_o[x] 	= 0

			for key,value in hasil_o[i].items():
				if key != 'WO':
					a_o[key] = (hasil_o[i][key]/target[i][key]) * 100 if target[i][key] != 0 else 0
			akurasi_o.append(a_o)

		jW = 0
		aW = 0
		jB = 0
		aB = 0
		jW = 0
		aS = 0
		jS = 0
		aM = 0
		jM = 0
		aJ = 0
		jJ = 0
		aK = 0
		jK = 0
		aT = 0
		jT = 0
		aN = 0
		jN = 0
		for i in range(jumlah_data):
			for key, value in akurasi_s[i].items():
				if key == 'WS':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_s = {
			'WS'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		for i in range(jumlah_data):
			for key, value in akurasi_o[i].items():
				if key == 'WO':
					jW += 1
					aW += value
				elif key == 'B':
					jB += 1
					aB += value
				elif key == 'S':
					jS += 1
					aS += value
				elif key == 'M':
					jM += 1
					aM += value
				elif key == 'J':
					jJ += 1
					aJ += value
				elif key == 'K':
					jK += 1
					aK += value
				elif key == 'T':
					jT += 1
					aT += value
				elif key == 'N':
					jN += 1
					aN += value

		rata2_akurasi_o = {
			'WO'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			# 'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			# 'T'			: aT/jT if jT != 0 else 0,
			# 'N'			: aN/jN if jN != 0 else 0
		}

		r_all_s = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_s.items():
				if key in akurasi_s[i].keys():
					v = int(value)
					r_all_s.append(key + '=' + str(v))

		r_all_o = []
		for i in range(jumlah_data):
			for key, value in rata2_akurasi_o.items():
				if key in akurasi_o[i].keys():
					v = int(value)
					r_all_o.append(key + '=' + str(v))

		akurasi = {
			's'			: akurasi_s,
			'o'			: akurasi_o,
			'rata_s'	: set(r_all_s),
			'rata_o'	: set(r_all_o)
		}

		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = hasil_final_s, semua_hasil_o = hasil_final_o, waktu = waktu, akurasi = akurasi)
		

		return "hasil"




