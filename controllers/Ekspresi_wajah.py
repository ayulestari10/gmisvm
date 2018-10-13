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


	@page.route(f'{base}/latih_data', methods=['GET', 'POST'])
	def latih_data():
		if request.method == 'POST':
			jumlah = request.form['jumlah']

			# jumlah * setiap kelas
			data_b = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Bahagia', jumlah)
			data_s = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Sedih', jumlah)
			data_m = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Marah', jumlah)
			data_j = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Jijik', jumlah)
			data_k = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Kaget', jumlah)
			data_t = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Takut', jumlah)
			data_n = Ekspresi_wajah.Db.select_sejumlah_data_latih('S', 'Natural', jumlah)
		

			print(f"data_b = {data_b} dan tipe = {type(data_b)}")
			print(f"jumlah data_b = {len(data_b)}")

			data_latih = []
			data_latih.extend(data_b)
			data_latih.extend(data_s)
			data_latih.extend(data_m)
			data_latih.extend(data_j)
			data_latih.extend(data_k)
			data_latih.extend(data_t)
			data_latih.extend(data_n) 	

			# Cari rata-rata setiap ciri
			jumlah_data = len(data_latih)

			ciri1 = [float(el[0]) for el in data_latih]
			ciri2 = [float(el[1]) for el in data_latih]
			ciri3 = [float(el[2]) for el in data_latih]
			ciri4 = [float(el[3]) for el in data_latih]
			ciri5 = [float(el[4]) for el in data_latih]
			ciri6 = [float(el[5]) for el in data_latih]
			ciri7 = [float(el[6]) for el in data_latih]

			jum_c = ciri1 + ciri2 + ciri3 + ciri4 + ciri5 + ciri6 + ciri7
			jumlah_c = 0
			for i in range(len(jum_c)):
				jumlah_c += jum_c[i]

			print(f"Jumlah semua ciri = {jumlah_c}")

			mean_ciri1 = np.mean(ciri1)
			mean_ciri2 = np.mean(ciri2)
			mean_ciri3 = np.mean(ciri3)
			mean_ciri4 = np.mean(ciri4)
			mean_ciri5 = np.mean(ciri5)
			mean_ciri6 = np.mean(ciri6)
			mean_ciri7 = np.mean(ciri7)

			mean = np.mean(jumlah_c)

			print(f"Mean = {mean} dan tipe = {type(mean)}")

			# cari ciri - ciri rata2 dan dikuadratkan

			ciri_1 = (ciri1 - mean_ciri1) * (ciri1 - mean_ciri1)
			ciri_2 = (ciri2 - mean_ciri2) * (ciri2 - mean_ciri2)
			ciri_3 = (ciri3 - mean_ciri3) * (ciri3 - mean_ciri3)
			ciri_4 = (ciri4 - mean_ciri4) * (ciri4 - mean_ciri4)
			ciri_5 = (ciri5 - mean_ciri5) * (ciri5 - mean_ciri5)
			ciri_6 = (ciri6 - mean_ciri6) * (ciri6 - mean_ciri6)
			ciri_7 = (ciri7 - mean_ciri7) * (ciri7 - mean_ciri7)

			jumlah_kuadrat_ciri = ciri_1 + ciri_2 + ciri_3 + ciri_4 + ciri_5 + ciri_6 + ciri_7
			jumlah_k = 0
			for i in range(len(jumlah_kuadrat_ciri)):
				jumlah_k += jumlah_kuadrat_ciri[i]

			# Simpangan Baku
			Sbaku = np.sqrt(jumlah_k/jumlah_data)
			# Sbaku = Sbaku*100
			print(f"Data rata2 = {ciri_1} dan tipe = {type(ciri_1)}")
			print(f"Data rata2 = {len(ciri_1)}")
			print(f"Jumlah kuadrat ciri = {jumlah_k}")
			print(f"Simpangan Baku = {Sbaku}")

			# SUD 
			sud = 6/6 # 6 SD / 6 unit dari 7 kelas
			skala_unit_deviasi = sud * Sbaku
			print(f"skala_unit_deviasi = {skala_unit_deviasi} dan tipe={type(skala_unit_deviasi)}")

			# Nilai tengah Kelas Ke-4 = rata2 = mean
			k4 = mean
			k3 = mean - (0.5 * skala_unit_deviasi)
			k2 = mean - (0.8 * skala_unit_deviasi)
			k1 = mean - (1 * skala_unit_deviasi)
			k5 = mean + (0.5 * skala_unit_deviasi)
			k6 = mean + (0.8 * skala_unit_deviasi)
			k7 = mean + (1 * skala_unit_deviasi)

			print(f"K1 = {k1}")
			print(f"K3 = {k3}")
			print(f"K2 = {k2}")
			print(f"K4 = {k4}")
			print(f"K5 = {k5}")
			print(f"K6 = {k6}")
			print(f"K7 = {k7}")

			data_uji = Ekspresi_wajah.Db.select_data_uji_jumlah(1)

			print(f"Data uji = {data_uji} dan tipe = {type(data_uji)}")

			ciri, ciricv = Ekspresi_wajah.Dw.deteksi_single_uji(data_uji[0][0], data_uji[0][1])

			mean_ciri 		= np.mean(ciri)
			mean_ciricv 	= np.mean(ciricv)

			print(f"Mean ciri = {mean_ciri} dan tipe = {type(mean_ciri)}")
			print(f"Mean ciricv = {mean_ciricv} dan tipe = {type(mean_ciricv)}")

			# Klasifikasi data uji

			if mean_ciri <= k1:
				print(f"Kelas Bahagia")
			elif k1 < mean_ciri <= k3:
				print(f"Kelas Sedih") 
			elif k3 < mean_ciri <= k2:
				print(f"Kelas Marah")
			elif k2 < mean_ciri <= k4:
				print(f"Kelas Jijik")
			elif k4 < mean_ciri <= k5:
				print(f"Kelas Kaget")
			elif k5 < mean_ciri <= k6:
				print(f"Kelas Takut")
			elif k6 < mean_ciri <= k7:
				print(f"Kelas Natural")
			else:
				print(f"Kelas Tidak Terdeteksi")      
			
		return "hasil"




