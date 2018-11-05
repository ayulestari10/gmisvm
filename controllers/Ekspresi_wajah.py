from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for, session
from PIL import Image
from jinja2 import TemplateNotFound
import numpy as np
import zipfile
from time import gmtime, strftime
import time
import os
from werkzeug.utils import secure_filename
import cv2
import matplotlib.pyplot as plt
import pickle
import csv

from sklearn.model_selection import GridSearchCV, KFold
from sklearn.multiclass import OneVsRestClassifier
from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neural_network import MLPClassifier
from sklearn import datasets


from libs.Deteksi_wajah import Deteksi_wajah
from libs.GMI import GMI
from models.Database import Database
from libs.Klasifikasi import Klasifikasi
from libs.Praproses import Praproses
from libs.OpenCV import OpenCV
from libs.Render_template import Render_template
from collections import Counter

class Ekspresi_wajah:

	page 		= Blueprint('Ekspresi_wajah_page', __name__, template_folder = 'templates')
	base 		= '/ekspresi-wajah'
	Db 			= Database('localhost', 'root', '', 'gmisvm')
	Dw 			= Deteksi_wajah()
	pra 		= Praproses()
	OC 			= OpenCV()
	RT 			= Render_template()
	rectColor 	= {
		'bahagia'	: (102, 255, 255),	# kuning
		'sedih'		: (255, 191, 0),	# biru
		'jijik'		: (50, 205, 50),	# hijau
		'takut'		: (128, 0, 128),	# ungu
		'natural'	: (255, 248, 248),	# putih  
		'marah'		: (60, 20, 220),  	# merah
		'kaget' 	: (30, 105, 210)	# coklat
	}


	@page.route(f'{base}/latih-uji', methods=['GET', 'POST'])
	def latih_uji():
		return Ekspresi_wajah.RT.tampilan_latih_uji() 


	@page.route(f'{base}/pelatihan', methods=['GET', 'POST'])
	def pelatihan(): 

		if request.method == 'POST':

			try:
				f = request.files['zip_file']
			except:
				flash('Tidak ada data yang diunggah!', category='error_pelatihan')
				return Ekspresi_wajah.RT.tampilan_latih_uji() 
			
			zip_filename = f.filename[-3:]

			if zip_filename != 'zip':
				flash('Data yang diunggah harus dalam bentuk zip!', category='error_pelatihan')
				return Ekspresi_wajah.RT.tampilan_latih_uji() 

			filename = 'data/' + secure_filename(strftime("%Y-%m-%d-%H-%M-%S") + '_' + f.filename)
			f.save(filename)

			direktori = strftime("%Y-%m-%d-%H-%M-%S")

			with open(filename, mode = 'r') as file:
				zip_file = zipfile.ZipFile(filename)
				files = [zip_file.extract(fl, 'data/pelatihan/' + direktori) for fl in zip_file.namelist()]
				zip_file.close()
			os.remove(filename)

			dir1 		= os.listdir('data/pelatihan/' + direktori)
			cwd 		= os.getcwd()

			for i in range(len(dir1)):
				dir2			= os.listdir('data/pelatihan/' + direktori + '/') [i]
				jenis_kelas	 	= dir1[i]
				file_name		= os.listdir('data/pelatihan/' + direktori + '/' + dir2)[0]	
				files			= os.listdir('data/pelatihan/' + direktori + '/' + dir2)
				
				for file in files:
					berkas 		= cwd + '\\data\\pelatihan\\' + direktori + '\\' + dir2 + '\\' + file
					path 		= Ekspresi_wajah.Dw.resize_image(berkas, file, direktori, dir2)
					
					# Deteksi Wajah
					berkas_citra= Ekspresi_wajah.Dw.deteksi('pelatihan', path, direktori, dir2)

					# Praproses Wajah
					piksel_biner= Ekspresi_wajah.pra.biner(berkas_citra)

					# Ekstraksi Ciri
					gmi 		= GMI(piksel_biner) 
					gmi.hitungMomenNormalisasi()
					ciri 		= gmi.hitungCiri()
					kelas 		= jenis_kelas
					Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciri, 'S')

					ciricv 		= Ekspresi_wajah.OC.gmi_OpenCV(piksel_biner)
					Ekspresi_wajah.Db.insert_ciri_pelatihan('ciri_pelatihan', kelas, ciricv, 'O')


			flash('Data berhasil dilatih!', category='pelatihan')

		return Ekspresi_wajah.RT.tampilan_latih_uji() 


	@page.route(f'{base}/pengujian1', methods=['GET', 'POST'])
	def pengujian1():
		session['waktu_sekarang'] 	= 0
		session['waktu_uji'] 		= 0
		session['jumlah_data_uji'] 	= 0
		session['penanda_menit'] 	= [0]

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
		jumlah_data_teruji = []
		cwd				= os.getcwd()
		dirr 			= cwd + '\\data\\uji\\'
		waktu_mulai_uji = ''
		waktu_akhir_uji = ''
		semua_id_pengujian_s = []
		semua_id_pengujian_o = []

		for i in range(jumlah_data):
			path  		= dirr + str(data_uji[i][1])
			id_file 	= data_uji[i][0]
			nama_file	= data_uji[i][1]

			file_name__s, direktori, semua_hasil_s, id_pengujian_update, id_ciri_s = Ekspresi_wajah.uji_ciri_sendiri(id_file, path, nama_file)
			
			if i == 0:
				waktu_mulai_uji = semua_hasil_s['waktu']

			if i == (jumlah_data-1):
				waktu_akhir_uji = semua_hasil_s['waktu']

			semua_id_pengujian_s.append(id_ciri_s)

			file_name_s.append(file_name__s)
			waktu.append(semua_hasil_s['waktu'])
			hasil_final_s.append({
				'WS'	: semua_hasil_s['wajah'],
				'B'		: semua_hasil_s['bahagia'],
				'S'		: semua_hasil_s['sedih'],
				'M'		: semua_hasil_s['marah'],
				'J'		: semua_hasil_s['jijik'],
				'K'		: semua_hasil_s['kaget'],
				'T'		: semua_hasil_s['takut'],
				'N'		: semua_hasil_s['natural']
			})
 
			file_name_o, semua_hasil_o, jumlah_data_teruji_o, id_ciri_o = Ekspresi_wajah.uji_ciri_opencv(id_file, path, nama_file, direktori, id_pengujian_update, semua_hasil_s['waktu'])
			
			semua_id_pengujian_o.append(id_ciri_o)
			jumlah_data_teruji.append(jumlah_data_teruji_o)
			hasil_final_o.append({
				'WO'	: semua_hasil_o['wajah'],
				'B'		: semua_hasil_o['bahagia'],
				'S'		: semua_hasil_o['sedih'],
				'M'		: semua_hasil_o['marah'],
				'J'		: semua_hasil_o['jijik'],
				'K'		: semua_hasil_o['kaget'],
				'T'		: semua_hasil_o['takut'],
				'N'		: semua_hasil_o['natural']
			})

			# cek jika pengujian lebih dari 5 menit maka berhenti
			# if session['waktu_sekarang'] >= (60 * 5):
			# 	print("================================================Waktu pengujian telah mencapai 5 menit, proses dihentikan!")
			# 	flash('Waktu pengujian telah mencapai 5 menit, proses dihentikan!')
			# 	jumlah_data = i
			# 	break;

		print(f"waktu_mulai_uji = {waktu_mulai_uji}")
		print(f"waktu_akhir_uji = {waktu_akhir_uji}")

		files = {
			'jumlah_file_name_s'	: len(file_name_s),
			'file_s'				: file_name_s,
			'jumlah_file_name_o'	: len(file_name_o),
			'file_o'				: file_name_o,
			'jumlah_data'			: jumlah_data,
			'data_uji'				: data_uji
		}

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

		target_akhir = []
		for i in range(jumlah_data):
			t_a = {}
			for key, value in target[i].items():
				if value != 0:
					t_a[key] = value
			target_akhir.append(t_a) 


		# cek jika nilai hasil s tidak sama dengan 0 dan nilai ada pada target
		hasil_s = []
		for i in range(jumlah_data):
			h_s = {}
			for key, value in hasil_final_s[i].items():
				if value != 0 and key in target_akhir[i].keys():
					h_s[key] = value
				if key == 'WS':
					h_s['WS'] = value
			hasil_s.append(h_s)


		hasil_o = []
		for i in range(jumlah_data):
			h_o = {}
			for key, value in hasil_final_o[i].items():
				if value != 0 and key in target_akhir[i].keys():
					h_o[key] = value
				if key == 'WO':
					h_o['WO'] = value
			hasil_o.append(h_o)

		akurasi_s = []
		for i in range(jumlah_data):
			a_s = {}
			for key,value in  hasil_s[i].items():
				if key == 'WS':
					a_s[key] = 100 if hasil_s[i][key] > target_akhir[i]['WT'] else ((hasil_s[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0)
				if key != 'WS':
					a_s[key] = 100 if hasil_s[i][key] > target_akhir[i][key] else ((hasil_s[i][key]/target_akhir[i][key]) * 100 if target_akhir[i][key] != 0 else 0)

			# jika hasil_s tidak ada pada target maka akurasi key nya 0
			for k in target_akhir[i].keys():
				if any(k in d for d in hasil_s[i].keys()) == False and k != 'WT':
					a_s[k] = 0

			akurasi_s.append(a_s)

		akurasi_o = []
		for i in range(jumlah_data):
			a_o = {}
			for key,value in  hasil_o[i].items():
				if key == 'WO':
					a_o[key] = 100 if hasil_o[i][key] > target_akhir[i]['WT'] else ((hasil_o[i][key]/target_akhir[i]['WT']) * 100 if target_akhir[i]['WT'] != 0 else 0)
				if key != 'WO':
					a_o[key] = 100 if hasil_o[i][key] > target_akhir[i][key] else ((hasil_o[i][key]/target_akhir[i][key]) * 100 if target_akhir[i][key] != 0 else 0)

			# jika hasil_o tidak ada pada target maka akurasi key nya 0
			for k in target_akhir[i].keys():
				if any(k in d for d in hasil_o[i].keys()) == False and k != 'WT':
					a_o[k] = 0
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
			'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			'T'			: aT/jT if jT != 0 else 0,
			'N'			: aN/jN if jN != 0 else 0
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
			'WO'		: aW/jW if jW != 0 else int(0),
			'B'			: aB/jB if jB != 0 else int(0),
			'S'			: aS/jS if jS != 0 else int(0),
			'M'			: aM/jM if jM != 0 else int(0),
			'J'			: aJ/jJ if jJ != 0 else int(0),
			'K'			: aK/jK if jK != 0 else int(0),
			'T'			: aT/jT if jT != 0 else int(0),
			'N'			: aN/jN if jN != 0 else int(0)
		}

		r_all_s = []
		for key, value in rata2_akurasi_s.items():
			if type(value) == float and value == 0.0:
				v = round(value, 2)
				r_all_s.append(key + '=' + str(v))
			if value != 0:
				v = round(value, 2)
				r_all_s.append(key + '=' + str(v))

		r_all_o = []
		for key, value in rata2_akurasi_o.items():
			if type(value) == float and value == 0.0:
				v = round(value, 2)
				r_all_o.append(key + '=' + str(v))
			if value != 0:
				v = round(value, 2)
				r_all_o.append(key + '=' + str(v))


		akurasi = {
			's'			: akurasi_s,
			'o'			: akurasi_o,
			'rata_s'	: r_all_s,
			'rata_o'	: r_all_o
		}
		
		t = []
		s = []

		# Diagram hasil jumlah data teruji
		for i in range(len(jumlah_data_teruji)):
			for key, value in jumlah_data_teruji[i].items():
				print(f"key = {key} tipe = {type(key)} dan value = {value} tipe = {type(value)}")
				if key != 0:
					# sumbu x
					t.append(key)
					# sumbu y
					s.append(value)

		plt.plot(t, s, linestyle='-', marker='o', color='b')
		plt.xlabel('Waktu (Menit)')
		plt.ylabel('Jumlah Data')
		plt.title('Perbandingan Waktu dengan Jumlah Data Uji yang diproses')
		plt.grid(True)
		path = os.getcwd() + '\\static\\data\\grafik\\' + direktori + '.png'
		plt.savefig(path)

		hasil_pengujian_pertama = []
		for i in range(files['jumlah_data']):
			hasil_pengujian = {
				'No'			: i + 1,
				'ID Ciri Kode Sendiri' : semua_id_pengujian_s[i],
				'ID Ciri OpenCV' : semua_id_pengujian_o[i],
				'Nama File'		: files['data_uji'][i][1],
				'Target'		: target_akhir[i],
				'Hasil Kode Sendiri' : hasil_s[i],
				'Hasil OpenCV'	: hasil_o[i],
				'Akurasi Kode Sendiri' : akurasi_s[i],
				'Akurasi OpenCV' : akurasi_o[i]
			}
			hasil_pengujian_pertama.append(hasil_pengujian)

		path_dir = os.getcwd()

		# Simpan data pengujian ke csv
		keys = hasil_pengujian_pertama[0].keys()
		with open(path_dir + '\\hasil\\pengujian_pertama\\Hasil Pengujian '+ waktu_mulai_uji +'.csv', 'w', newline='') as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(hasil_pengujian_pertama)

		with open(path_dir + '\\hasil\\pengujian_pertama\\Hasil Pengujian '+ waktu_mulai_uji +'.csv','a', newline='') as c:
			for item in r_all_s:
			    c.write(item + ',')
			c.write('\n')
			for item in r_all_o:
				c.write(item + ',')
			c.write('\n')

			data_waktu = []
			for teruji in jumlah_data_teruji:
				for key,value in teruji.items():
					key_durasi = key.replace(',', '.')
					data_waktu.append(str(key_durasi + '=' + str(value)))

			for teruji in data_waktu:
				c.write(teruji + ',')

		# Simpan ciri pengujian s ke csv

		data_ciri_s = Ekspresi_wajah.Db.select_hasil_ciri_pengujian_s(waktu_mulai_uji, waktu_akhir_uji)
		with open(path_dir + '\\hasil\\ekstraksi_ciri\\Hasil Ekstraksi Ciri dari Kode Sendiri '+ waktu_mulai_uji +'.csv','w', newline='') as c:
			c.write('No,')
			c.write('ID Ciri Pengujian,')
			c.write('Ciri 1,')
			c.write('Ciri 2,')
			c.write('Ciri 3,')
			c.write('Ciri 4,')
			c.write('Ciri 5,')
			c.write('Ciri 6,')
			c.write('Ciri 7,')
			c.write('Kelas Terklasifikasi')
			c.write('\n')
			i = 0
			for item in data_ciri_s:
			    i += 1
			    c.write(str(i) + ',')
			    for ciri_s in item:
			    	c.write(str(ciri_s) + ',')
			    c.write('\n')

		# Simpan ciri pengujian o ke csv
		data_ciri_o = Ekspresi_wajah.Db.select_hasil_ciri_pengujian_o(waktu_mulai_uji, waktu_akhir_uji)
		with open(path_dir + '\\hasil\\ekstraksi_ciri\\Hasil Ekstraksi Ciri dari OpenCV '+ waktu_mulai_uji +'.csv','w', newline='') as c:
			c.write('No,')
			c.write('ID Ciri Pengujian,')
			c.write('Ciri 1,')
			c.write('Ciri 2,')
			c.write('Ciri 3,')
			c.write('Ciri 4,')
			c.write('Ciri 5,')
			c.write('Ciri 6,')
			c.write('Ciri 7,')
			c.write('Kelas Terklasifikasi')
			c.write('\n')
			i = 0
			for item in data_ciri_o:
			    i += 1
			    c.write(str(i) + ',')
			    for ciri_o in item:
			    	c.write(str(ciri_o) + ',')
			    c.write('\n')

		return Ekspresi_wajah.RT.tampilan_pengujian1(files, target_akhir, hasil_final_s, hasil_final_o, waktu, akurasi, jumlah_data_teruji, direktori)


	def uji_ciri_sendiri(id_file, image, nama_file):

		waktu_mulai 		= time.time()

		id_pengujian_update = []
		file_name_s 		= []
		waktu 				= []
		dir_s 				= []
		hasil_final_s 		= []
		semua_hasil_s		= {}
		id_ciri_s 			= []

		# Resize
		fname 				= os.getcwd() + '\\data\\uji\\resize\\uji\\' + nama_file
		
		if os.path.isfile(fname):
			print("________________Data Sudah dirize")
			path 			= fname
		else:
			path 			= Ekspresi_wajah.Dw.resize_image(image, nama_file, 'uji', 'uji')

		# deteksi wajah
		faces, img 			= Ekspresi_wajah.OC.deteksi(path)

		print(f"Jumlah face file {id_file} = {len(faces)}")

		global path_wajah
		directory 			= strftime("%Y-%m-%d_%H-%M-%S")

		path 				= 'static/data/latih_uji/' + directory
		if os.path.exists(path) is False:
			os.mkdir(path)

		# ciri dan kelas sendiri
		kumpulan_ciri_s 	= Ekspresi_wajah.Db.select_ciri('ciri_pelatihan', 'S')
		kumpulan_kelas_s 	= Ekspresi_wajah.Db.select_kelas('ciri_pelatihan', 'S')

		rata_rata_ciri_s 	= {}
		for kelas_s in kumpulan_kelas_s:
			rata_rata_ciri_s[kelas_s] 	= Ekspresi_wajah.Db.select_avg('ciri_pelatihan', kelas_s)

		waktu_s 			= strftime("%Y-%m-%d_%H-%M-%S")

		for i, f in enumerate(faces):
			x, y, w, h 		= np.array([v for v in f], dtype=np.int64)

			sub_face 		= img[y:y+h, x:x+w]
			path_wajah 		= path + '/' + str(i) + '.png'
			cv2.imwrite(path_wajah, sub_face)

			sub_face 	= Ekspresi_wajah.pra.biner(path_wajah)
			gmi 		= GMI(sub_face) 
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()
			print(f"Ciri wajah ke-{i} pada file {id_file} = {ciri} dan jumlah = {len(ciri)}")
			
			# klasifikasi sendiri
			kl_s 		= Klasifikasi(kumpulan_ciri_s, kumpulan_kelas_s)			
			ekspresi_s 	= kl_s.classify([ciri])

			cv2.rectangle(img, (x,y), (x+w, y+h), Ekspresi_wajah.rectColor[ekspresi_s])
			cv2.rectangle(img, (x, y - 20), (x + w, y), Ekspresi_wajah.rectColor[ekspresi_s], -1)
			cv2.putText(img, ekspresi_s, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 0.8 , (0, 0, 0), 1)

			Ekspresi_wajah.Db.insert_ciri('ciri_pengujian', ciri, 'S')
			data_pengujian_s	= Ekspresi_wajah.Db.select_first_row()
			id_ciri_s.append(data_pengujian_s[0][0])

			# insert pengujian
			data_pengujian 	= {
				'id_file'				: str(id_file),
				'id_ciri_pengujian_s'	: str(data_pengujian_s[0][0]),
				'waktu'					: waktu_s,
				'hasil_sendiri'			: ekspresi_s,
				'direktori'				: directory
			}
			pengujian = Ekspresi_wajah.Db.insert_pengujian(data_pengujian)
			select_pengujian = Ekspresi_wajah.Db.select_pengujian_first_row()
			id_pengujian_update.append(select_pengujian[0][0]) 

			print(f"===== Ekspresi wajah ke-{i} _ {id_file} = {ekspresi_s}")


		# select data hasil pengujian sendiri dan insert hasil sendiri
		hasil_s 	= Ekspresi_wajah.Db.select_hasil('hasil_sendiri', id_file, waktu_s)
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
			'natural'	: hitung_s['natural'],
			'waktu'		: waktu_s
		}
		Ekspresi_wajah.Db.insert_hasil(hasil_all_s)

		dir_file_name 	= 'static/data/latih_uji/' + directory + '_Hasil_Sendiri.png'
		file_name_s		= directory + '_Hasil_Sendiri.png'
		cv2.imwrite(dir_file_name, img)

		waktu_loop 		= time.time()
		waktu_sekarang 	= session['waktu_sekarang'] + (waktu_loop - waktu_mulai)
		session['waktu_sekarang'] 	= waktu_sekarang

		return file_name_s, directory, hasil_all_s, id_pengujian_update, id_ciri_s



	def uji_ciri_opencv(id_file, image, nama_file, directory, id_pengujian_update, waktu_s):

		file_name_o 		= []
		hasil_final_o 		= []
		semua_hasil_o		= {}
		waktu_mulai 		= time.time()
		jumlah_data_teruji	= {}
		id_ciri_o 			= []
		path 				= 'data/resize/uji/' + nama_file

		# deteksi wajah
		faces,img 			= Ekspresi_wajah.OC.deteksi(path)

		global path_wajah

		# ciri dan kelas openCV
		kumpulan_ciri_o 	= Ekspresi_wajah.Db.select_ciri('ciri_pelatihan', 'O')
		kumpulan_kelas_o 	= Ekspresi_wajah.Db.select_kelas('ciri_pelatihan', 'O')

		rata_rata_ciri_o 	= {}
		for kelas_o in kumpulan_kelas_o:
			rata_rata_ciri_o[kelas_o] = Ekspresi_wajah.Db.select_avg('ciri_pelatihan', kelas_o)

		ekspresi_openCV 	= []

		for i, f in enumerate(faces):
			x, y, w, h = np.array([v for v in f], dtype=np.int64)

			sub_face = img[y:y+h, x:x+w]

			path_wajah = 'static/data/latih_uji/' + directory + '/' + str(i) + '_.png'
			cv2.imwrite(path_wajah, sub_face)

			# Praproses wajah
			pra 		= Praproses()
			sub_face 	= pra.biner(path_wajah)

			# Deteksi Wajah
			ciricv		= Ekspresi_wajah.OC.gmi_OpenCV(sub_face)
			
			# Klasifikasi hasil ciri openCV
			kl_o 		= Klasifikasi(kumpulan_ciri_o, kumpulan_kelas_o)
			ekspresi_o 	= kl_o.classify([ciricv])

			cv2.rectangle(img, (x,y), (x+w, y+h), Ekspresi_wajah.rectColor[ekspresi_o])
			cv2.rectangle(img, (x, y - 20), (x + w, y), Ekspresi_wajah.rectColor[ekspresi_o], -1)
			cv2.putText(img, ekspresi_o, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 0.8 , (0, 0, 0), 1)

			Ekspresi_wajah.Db.insert_ciri('ciri_pengujian', ciricv, 'O')
			data_pengujian_o	= Ekspresi_wajah.Db.select_first_row()
			id_ciri_o.append(data_pengujian_o[0][0])

			# insert pengujian
			data_pengujian 	= {
				'id_file'				: str(id_file),
				'id_ciri_pengujian_o'	: str(data_pengujian_o[0][0]),
				'hasil_opencv'			: ekspresi_o,
				'waktu'					: waktu_s,
				'id_pengujian'			: id_pengujian_update[i]
			}
			pengujian = Ekspresi_wajah.Db.update_pengujian(data_pengujian)

			print(f"===== Ekspresi wajah ke-{i} _ {id_file} = {ekspresi_o}")

			
		# select data hasil pengujian openCV dan insert hasil openCV
		hasil_o = Ekspresi_wajah.Db.select_hasil('hasil_opencv', id_file, waktu_s)
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
		Ekspresi_wajah.Db.insert_hasil(hasil_all_o)

		dir_file_name 	= 'static/data/latih_uji/' + directory + '_Hasil_OpenCV.png'
		file_name_o		= directory + '_Hasil_OpenCV.png'
		cv2.imwrite(dir_file_name, img)

		# tempat cek2 waktu 
		session['jumlah_data_uji'] = session['jumlah_data_uji'] + 1 
		print(f"jumlah_data_uji = {session['jumlah_data_uji']}")

		waktu_loop 		= time.time()
		waktu_sekarang 	= session['waktu_sekarang'] + (waktu_loop - waktu_mulai)
		session['waktu_sekarang'] = waktu_sekarang
		print(f"Waktu sekarang di o = {round(session['waktu_sekarang'], 3)}s")

		## setiap 2 menit
		if int(session['waktu_sekarang'] / (60 * 2)) == len(session['penanda_menit']):
			durasi_menit 		= round(round(session['waktu_sekarang'], 3)/60, 3)
			key_durasi 			= str(durasi_menit).replace('.', ',')
			jumlah_data_teruji 	= {
				key_durasi : session['jumlah_data_uji']
			}
			session['penanda_menit'].append(key_durasi)

		
		if id_file == 115:
			durasi_menit 		= round(round(session['waktu_sekarang'], 3)/60, 3)
			key_durasi 			= str(durasi_menit).replace('.', ',')
			jumlah_data_teruji 	= {
				key_durasi : session['jumlah_data_uji']
			}
			session['penanda_menit'].append(key_durasi)

		print(f"Jumlah penanda menit = {session['penanda_menit'] } dan jumlah =  {len(session['penanda_menit'] )}")

		## cek waktu_sekarang apakah lebih dari 5 menit
		# if session['waktu_sekarang'] >= (60 * 5):
		# 	flash('Waktu pengujian telah mencapai 5 menit, proses dihentikan!')
		# 	return file_name_o, hasil_all_o, jumlah_data_teruji


		# waktu_selesai = time.time()
		# durasi = waktu_selesai - waktu_mulai
		# session['waktu_uji'] = durasi if session['waktu_uji'] is None else (session['waktu_uji'] + durasi)

		return file_name_o, hasil_all_o, jumlah_data_teruji, id_ciri_o





	@page.route(f'{base}/hasil_detail/<int:id_file>/<string:waktu>', methods=['GET', 'POST'])
	def hasil_detail(id_file, waktu):

		data_pengujian 	= Ekspresi_wajah.Db.select_data_pengujian(id_file, waktu)
		jumlah_wajah 	= len(data_pengujian)
		ciri_all_s 		= []
		ciri_all_o 		= []
		id_ciri_s 		= []
		id_ciri_o 		= []
		hasil_s 		= []
		hasil_o 		= []

		for i in range(jumlah_wajah):
			ciri_s = Ekspresi_wajah.Db.select_ciri_pengujian(data_pengujian[i][2], 'S')
			ciri_all_s.append(ciri_s)
			ciri_o = Ekspresi_wajah.Db.select_ciri_pengujian(data_pengujian[i][3], 'O')
			ciri_all_o.append(ciri_o) 

			id_ciri_s.append(data_pengujian[i][2])
			id_ciri_o.append(data_pengujian[i][3])

		for i in range(jumlah_wajah):
			hasil_s.append(data_pengujian[i][5])
			hasil_o.append(data_pengujian[i][6])


		return Ekspresi_wajah.RT.tampilan_detail(ciri_all_s, ciri_all_o, data_pengujian, hasil_s, hasil_o)


	@page.route(f'{base}/pengujian2', methods=['GET', 'POST'])
	def pengujian2():
		semua_hasil = {}
		
		if request.method == 'POST':
			kumpulan_ciri_s 	= Ekspresi_wajah.Db.select_ciri('ciri_pelatihan', 'S')
			kumpulan_kelas_s 	= Ekspresi_wajah.Db.select_kelas('ciri_pelatihan', 'S')

			pembagi = [2, 3, 4, 5, 6, 7, 8, 9, 10] 

			## Metode Multi Class SVM
			hasil_metode1 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= svm.LinearSVC()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode1.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode1.append(round(np.mean(hasil_metode1), 2))
			semua_hasil['Multi Class SVM'] = hasil_metode1


			## Metode Decision Tree Classifier
			hasil_metode2 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= tree.DecisionTreeClassifier()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode2.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode2.append(round(np.mean(hasil_metode2), 2))
			semua_hasil['Decision Tree Classifier'] = hasil_metode2


			## Metode Random Forest Classifier
			hasil_metode3 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= RandomForestClassifier()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode3.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode3.append(round(np.mean(hasil_metode3), 2))
			semua_hasil['Random Forest Classifier'] = hasil_metode3


			## Metode Gaussian Naive Bayes
			hasil_metode4 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= GaussianNB()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode4.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode4.append(round(np.mean(hasil_metode4), 2))
			semua_hasil['Gaussian Naive Bayes'] = hasil_metode4


			## Metode Nearest Centroid
			hasil_metode5 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= NearestCentroid()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode5.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode5.append(round(np.mean(hasil_metode5), 2))
			semua_hasil['Nearest Centroid'] = hasil_metode5


			## Metode MLP Classifier
			hasil_metode6 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= MLPClassifier()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode6.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode6.append(round(np.mean(hasil_metode6), 2))
			semua_hasil['MLP Classifier'] = hasil_metode6


			## Metode Stochastic Gradient Descent Classifier
			hasil_metode7 = []
			for i in range(len(pembagi)):
				kf 			= KFold(n_splits = pembagi[i], random_state = 1, shuffle = True)
				k_scores 	= []

				for j, (train_index, test_index) in enumerate(kf.split(kumpulan_ciri_s)):
					clf 	= SGDClassifier()
					clf.fit(kumpulan_ciri_s[train_index], kumpulan_kelas_s[train_index])
					scores 	= round(clf.score(kumpulan_ciri_s[test_index], kumpulan_kelas_s[test_index]) * 100, 2)
					k_scores.append(scores)
					print(f"Score k-{j + 1} : {scores}%")

				hasil_metode7.append( round(np.mean(np.array(k_scores)), 2) )
				print(f"Mean: {round(np.mean(np.array(k_scores)), 2)}%")

			hasil_metode7.append(round(np.mean(hasil_metode7), 2))
			semua_hasil['Stochastic Gradient Descent Classifier'] = hasil_metode7

			
			t = []
			
			print(f"semua_hasil = {semua_hasil} dan tipe= {type(semua_hasil)} dan jumlah = {len(semua_hasil)}")

			for value in semua_hasil.values():
				t.append(value[9])

			print(f"t = {t} dan tipe = {type(t)}")
			t = np.array(t)
			
			plt.plot([1, 2, 3, 4, 5, 6, 7], t, linestyle='-', marker='o', color='b')
			plt.xticks([1, 2, 3, 4, 5, 6, 7], ['MC', 'DC', 'RS', 'GNB', 'NC', 'MLP', 'SGD'])

			plt.xlabel('Metode Klasifikasi')
			plt.ylabel('Rata-Rata Akurasi')
			plt.title('Perbandingan Metode Klasifikasi dan Rata-Rata Akurasi')
			plt.grid(True)
			path = os.getcwd() + '\\static\\data\\grafik\\metode_klasifikasi.png'
			plt.savefig(path)

		return Ekspresi_wajah.RT.tampilan_pengujian2(semua_hasil)


