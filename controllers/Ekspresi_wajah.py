from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for, session
from PIL import Image
from jinja2 import TemplateNotFound
import numpy as np
import zipfile
from time import gmtime, strftime
import os
from werkzeug.utils import secure_filename
import cv2
import time

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
		hasil_waktu_uji = {}
		hasil_waktu_latih = {}

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

			print(f"Tipe file = {type(files)}")

			hasil_waktu_latih = Ekspresi_wajah.latih(, 'latih_uji', direktori)
			jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi, hasil_waktu_uji = Ekspresi_wajah.uji()

		return Ekspresi_wajah.RT.tampilan_latih_uji(jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi, hasil_waktu_uji, hasil_waktu_latih) 


	def latih(files, ket, direktori):
		dir1 		= os.listdir('data/'+ ket +'/' + direktori)
		cwd 		= os.getcwd()

		waktu_mulai 			= time.time()
		session['waktu_mulai'] 	= waktu_mulai
		session['waktu_latih'] 	= waktu_mulai
		session['durasi'] 		= 0
		j_data_latih 			= []
		jumlah_file_latih 		= []
		penanda_menit = [0]


		for i in range(len(dir1)):


			dir2			= os.listdir('data/'+ ket +'/' + direktori + '/') [i]
			jenis_kelas	 	= dir1[i]
			file_name		= os.listdir('data/'+ ket +'/' + direktori + '/' + dir2)[0]	
			files			= os.listdir('data/'+ ket +'/' + direktori + '/' + dir2)
			
			for file in files:
				j_data_latih.append(file)
				berkas 		= cwd + '\\data\\'+ ket +'\\' + direktori + '\\' + dir2 + '\\' + file
				path 		= Ekspresi_wajah.Dw.resize_image(berkas, file, direktori, dir2)
				
				# Deteksi Wajah
				berkas_citra= Ekspresi_wajah.Dw.deteksi(ket, path, direktori, dir2)

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

				session['durasi'] = time.time() - waktu_mulai
				print(f"Durasi = {session['durasi']}")

				## cek apakah durasi mencapai stngah menit maka simpan jumlah data latih
				if int(session['durasi'] / (60 * 1)) == len(penanda_menit):
					durasi_menit = session['durasi']/60
					jumlah_file_latih.append({
						str(round(durasi_menit, 0)) : len(j_data_latih)
					})
					penanda_menit.append(str(round(durasi_menit, 0)))

				## cek apakah durasi lebih dari 30 menit

				if session['durasi'] >= (60 * 30):
					flash('Waktu pelatihan telah mencapai 30 menit, proses dihentikan!')
					break;

			## cek apakah durasi lebih dari 30 menit
			if session['durasi'] >= (60 * 30):
				flash('Waktu pelatihan telah mencapai 30 menit, proses dihentikan!')
				break;

		waktu_selesai 			= time.time()
		session['waktu_latih'] = waktu_selesai - waktu_mulai 

		hasil_waktu_latih = {
			'latih' 	: jumlah_file_latih
		}

		return hasil_waktu_latih


	def uji():
		session['file_teruji'] = []
		session['waktu_sekarang'] = 0
		session['waktu_uji'] = 0

		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_o 	= []
		semua_hasil_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		waktu 			= []
		data_latih 		= []

		file_name_s, jarak_all_s, direktori, semua_hasil_s, hasil_final_s, id_pengujian_update, waktu = Ekspresi_wajah.uji_ciri_sendiri(data_uji, data_latih)
		
		file_name_o, jarak_o, semua_hasil_o, hasil_final_o, jumlah_data_teruji = Ekspresi_wajah.uji_ciri_opencv(data_uji, data_latih, direktori, id_pengujian_update, waktu)

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
			'WO'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			'T'			: aT/jT if jT != 0 else 0,
			'N'			: aN/jN if jN != 0 else 0
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

		print(f"Total waktu pelatihan: {round(session['waktu_latih'], 2)}s")
		print(f"Total waktu pengujian: {round(session['waktu_uji'], 2)}s")
		print(f"Total waktu: {round(session['waktu_latih'] + session['waktu_uji'], 2)}s")

		hasil_waktu_uji = {
			'uji'		: jumlah_data_teruji
		}

		print(f"hasil_waktu_uji = {hasil_waktu_uji} dan jumlah = {len(hasil_waktu_uji)} dan tipe = {type(hasil_waktu_uji)}")
		print(f"hasil_waktu_uji['uji'] = {hasil_waktu_uji['uji']} dan jumlah = {len(hasil_waktu_uji['uji'])} dan tipe = {type(hasil_waktu_uji['uji'])}")

		return jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi, hasil_waktu_uji


	def uji_ciri_sendiri(data_uji, data_latih):
		jarak_all_s 		= []
		id_pengujian_update = []
		file_name_s 		= []
		waktu 				= []
		hasil_final_s 		= []
		dir_s 				= []

		# ciri dan kelas sendiri dari data pelatihan
		if len(data_latih) == 0:
			kumpulan_ciri_s 	= Ekspresi_wajah.Db.select_ciri('ciri_pelatihan', 'S')
			kumpulan_kelas_s 	= Ekspresi_wajah.Db.select_kelas('ciri_pelatihan', 'S')
		else:
			kumpulan_kelas_s, kumpulan_ciri_s  =  Ekspresi_wajah.ambil_data_latih(data_latih)

		print(f"Kumpulan ciri = {type(kumpulan_ciri_s)} dan kumpulan_kelas = {type(kumpulan_kelas_s)}")
		rata_rata_ciri_s 	= {}
		for kelas_s in kumpulan_kelas_s:
			rata_rata_ciri_s[kelas_s] = Ekspresi_wajah.Db.select_avg('ciri_pelatihan', kelas_s)

		cwd				= os.getcwd()
		dirr 			= cwd + '\\data\\uji\\'
		waktu_mulai 	= time.time()

		# lakukan sebanyak data uji
		for j in range(len(data_uji)):
			file_teruji = session['file_teruji']
			file_teruji.append(data_uji[j])
			session['file_teruji'] = file_teruji

			waktu_s 	= strftime("%Y-%m-%d_%H-%M-%S")

			id_file 	= data_uji[j][0]
			nama_file	= data_uji[j][1]

			# Deteksi wajah
			path_img  	= dirr + str(nama_file)
		
			faces, img, direktori, path2	= Ekspresi_wajah.Dw.deteksi_multi_face(path_img, nama_file, 'sendiri')

			dir_s.append(direktori)

			for i, f in enumerate(faces):
				x, y, w, h 		= np.array([v for v in f], dtype=np.int64)

				sub_face 		= img[y:y+h, x:x+w]
				path_wajah 		= path2 + '/' + str(i) + '.png'
				cv2.imwrite(path_wajah, sub_face)

				
				# Praproses Wajah
				sub_face 	= Ekspresi_wajah.pra.biner(path_wajah)
				
				# Ekstraksi Ciri GMI
				gmi 		= GMI(sub_face) 
				gmi.hitungMomenNormalisasi()
				ciri 		= gmi.hitungCiri()
				print(f"Tipe ciri = {type(ciri)}")
				
				# Klasifikasi Ekspresi Wajah
				kl_s 		= Klasifikasi(kumpulan_ciri_s, kumpulan_kelas_s)			
				ekspresi_s 	= kl_s.classify([ciri])

				cv2.rectangle(img, (x,y), (x+w, y+h), Ekspresi_wajah.rectColor[ekspresi_s])
				cv2.rectangle(img, (x, y - 20), (x + w, y), Ekspresi_wajah.rectColor[ekspresi_s], -1)
				cv2.putText(img, ekspresi_s, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 0.8 , (0, 0, 0), 1)

				Ekspresi_wajah.Db.insert_ciri('ciri_pengujian', ciri, 'S')
				data_pengujian_s	= Ekspresi_wajah.Db.select_first_row()
				id_ciri_pengujian_s	= str(data_pengujian_s[0][0])

				# insert pengujian
				data_pengujian 	= {
					'id_file'				: str(id_file),
					'id_ciri_pengujian_s'	: id_ciri_pengujian_s,
					'waktu'					: waktu_s,
					'hasil_sendiri'			: ekspresi_s,
					'direktori'				: direktori
				}
				# print(f"Data pengujian s = {data_pengujian}")
				pengujian = Ekspresi_wajah.Db.insert_pengujian(data_pengujian)
				select_pengujian = Ekspresi_wajah.Db.select_pengujian_first_row()
				id_pengujian_update.append(select_pengujian[0][0])

				# Jarak Setiap Ciri
				if len(data_latih) == 0:
					jarak_bahagia_s = []
					for b in range(7):
						jarak_bahagia_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['bahagia'][b]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'bahagia', jarak_bahagia_s)

					jarak_sedih_s = []
					for s in range(7):
						jarak_sedih_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['sedih'][s]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'sedih', jarak_sedih_s)

					jarak_marah_s = []
					for m in range(7):
						jarak_marah_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['marah'][m]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'marah', jarak_marah_s)

					jarak_jijik_s = []
					for ji in range(7):
						jarak_jijik_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['jijik'][ji]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'jijik', jarak_jijik_s)

					jarak_kaget_s = []
					for k in range(7):
						jarak_kaget_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['kaget'][k]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'kaget', jarak_kaget_s)

					jarak_takut_s = []
					for t in range(7):
						jarak_takut_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['takut'][t]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'takut', jarak_takut_s)

					jarak_natural_s = []
					for n in range(7):
						jarak_natural_s.append(Ekspresi_wajah.hitung_jarak(ciri[i], rata_rata_ciri_s['natural'][n]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_s, 'natural', jarak_natural_s)
						
					jarak_all = {
						'bahagia'	: jarak_bahagia_s,
						'sedih'		: jarak_sedih_s,
						'marah'		: jarak_marah_s, 
						'jijik'		: jarak_jijik_s,
						'kaget'		: jarak_kaget_s,
						'takut'		: jarak_takut_s,
						'natural'	: jarak_natural_s
					}

					jarak_all_s.append(jarak_all)


			# select data hasil pengujian sendiri dan insert hasil sendiri
			hasil_s 	= Ekspresi_wajah.Db.select_hasil('hasil_sendiri', id_file, waktu_s)
			hitung_s 	= Counter(elem[0] for elem in hasil_s)

			semua_hasil_s = {
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
			Ekspresi_wajah.Db.insert_hasil(semua_hasil_s)

			dir_file_name 	= 'static/data/latih_uji/' + direktori + '_Hasil_Sendiri.png'
			file_name_s.append(direktori + '_Hasil_Sendiri.png')
			cv2.imwrite(dir_file_name, img)
			
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

			waktu_loop = time.time()
			print(f"Jumlah file teruji: {len(file_teruji)}")
			waktu_sekarang = session['waktu_sekarang'] + (waktu_loop - waktu_mulai)
			print(f"Waktu sekarang: {round(waktu_sekarang, 2)}s")
			
			if session['waktu_latih'] == 0:
				waktu_pelatihan = 0
			else:
				waktu_pelatihan = session['waktu_latih']
	
			session['waktu_sekarang'] = waktu_sekarang

			## cek waktu_sekarang + waktu pelatihan apakah lebih dari 30 menit

			if session['waktu_sekarang'] + waktu_pelatihan >= 1800:
				flash('Waktu pelatihan telah mencapai 30 menit, proses dihentikan!')
				break;

		waktu_selesai = time.time()
		durasi = waktu_selesai - waktu_mulai
		session['waktu_uji'] = durasi if session['waktu_uji'] is None else (session['waktu_uji'] + durasi)

		return file_name_s, jarak_all_s, dir_s, semua_hasil_s, hasil_final_s, id_pengujian_update, waktu



	def uji_ciri_opencv(data_uji, data_latih, direktori, id_pengujian_update, waktu):
		jarak_all_o 		= []
		file_name_o 		= []
		hasil_final_o 		= []

		# ciri dan kelas sendiri dari data pelatihan
		if len(data_latih) == 0:
			kumpulan_ciri_o 	= Ekspresi_wajah.Db.select_ciri('ciri_pelatihan', 'O')
			kumpulan_kelas_o 	= Ekspresi_wajah.Db.select_kelas('ciri_pelatihan', 'O')
		else:
			kumpulan_kelas_o, kumpulan_ciri_o = Ekspresi_wajah.ambil_data_latih(data_latih)

		rata_rata_ciri_o 	= {}
		for kelas_o in kumpulan_kelas_o:
			rata_rata_ciri_o[kelas_o] = Ekspresi_wajah.Db.select_avg('ciri_pelatihan', kelas_o)

		Ekspresi_wajah.waktu_o 		= strftime("%Y-%m-%d_%H-%M-%S")
		cwd							= os.getcwd()
		dirr 						= cwd + '\\data\\uji\\'

		waktu_mulai 		= time.time()
		jumlah_file_teruji	= []
		j_data_uji 			= []
		jumlah_data_teruji	= []
		penanda_menit 		= [0]

		# lakukan sebanyak data uji
		for j in range(len(data_uji)):
			j_data_uji.append(j)

			id_file 	= data_uji[j][0]
			nama_file	= data_uji[j][1]

			# Deteksi wajah
			path_img  	= dirr + str(nama_file)
		
			faces, img	= Ekspresi_wajah.Dw.deteksi_multi_face(path_img, nama_file, 'opencv')

			for i, f in enumerate(faces):
				x, y, w, h 		= np.array([v for v in f], dtype=np.int64)

				sub_face 		= img[y:y+h, x:x+w]
				path_wajah 		= 'static/data/latih_uji/' + direktori[j] + '/' + str(i) + '_.png'
				cv2.imwrite(path_wajah, sub_face)

				
				# Praproses Wajah
				sub_face 	= Ekspresi_wajah.pra.biner(path_wajah)
				
				# Ekstraksi Ciri GMI
				ciricv		= Ekspresi_wajah.OC.gmi_OpenCV(sub_face)
				
				# Klasifikasi Ekspresi Wajah
				kl_o 		= Klasifikasi(kumpulan_ciri_o, kumpulan_kelas_o)			
				ekspresi_o 	= kl_o.classify([ciricv])

				cv2.rectangle(img, (x,y), (x+w, y+h), Ekspresi_wajah.rectColor[ekspresi_o])
				cv2.rectangle(img, (x, y - 20), (x + w, y), Ekspresi_wajah.rectColor[ekspresi_o], -1)
				cv2.putText(img, ekspresi_o, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 0.8 , (0, 0, 0), 1)

				Ekspresi_wajah.Db.insert_ciri('ciri_pengujian', ciricv, 'O')
				data_pengujian_o	= Ekspresi_wajah.Db.select_first_row()
				id_ciri_pengujian_o	= str(data_pengujian_o[0][0])

				# Update pengujian
				data_pengujian 	= {
					'id_file'				: str(id_file),
					'id_ciri_pengujian_o'	: id_ciri_pengujian_o,
					'hasil_opencv'			: ekspresi_o,
					'waktu'					: waktu[j],
					'id_pengujian'			: id_pengujian_update[0]
				}
				pengujian = Ekspresi_wajah.Db.update_pengujian(data_pengujian)
				# print(f"hasil data_pengujian o = {data_pengujian} dan tipe = {type(data_pengujian)}")

				# hapus id_pengujian_update yang telah terupdate
				del id_pengujian_update[0]

				# Jarak Setiap Ciri
				if len(data_latih) == 0:
					jarak_bahagia_o = []
					for b in range(7):
						jarak_bahagia_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['bahagia'][b]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'bahagia', jarak_bahagia_o)

					jarak_sedih_o = []
					for s in range(7):
						jarak_sedih_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['sedih'][s]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'sedih', jarak_sedih_o)

					jarak_marah_o = []
					for m in range(7):
						jarak_marah_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['marah'][m]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'marah', jarak_marah_o)

					jarak_jijik_o = []
					for ji in range(7):
						jarak_jijik_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['jijik'][ji]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'jijik', jarak_jijik_o)

					jarak_kaget_o = []
					for k in range(7):
						jarak_kaget_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['kaget'][k]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'kaget', jarak_kaget_o)

					jarak_takut_o = []
					for t in range(7):
						jarak_takut_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['takut'][t]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'takut', jarak_takut_o)

					jarak_natural_o = []
					for n in range(7):
						jarak_natural_o.append(Ekspresi_wajah.hitung_jarak(ciricv[i], rata_rata_ciri_o['natural'][n]))
					Ekspresi_wajah.Db.insert_jarak_ciri(id_ciri_pengujian_o, 'natural', jarak_natural_o)
						
					jarak_all = {
						'bahagia'	: jarak_bahagia_o,
						'sedih'		: jarak_sedih_o,
						'marah'		: jarak_marah_o, 
						'jijik'		: jarak_jijik_o,
						'kaget'		: jarak_kaget_o,
						'takut'		: jarak_takut_o,
						'natural'	: jarak_natural_o
					}

					jarak_all_o.append(jarak_all)

			# select data hasil pengujian sendiri dan insert hasil sendiri
			hasil_o 	= Ekspresi_wajah.Db.select_hasil('hasil_opencv', id_file, waktu[j])
			hitung_o 	= Counter(elem[0] for elem in hasil_o)

			semua_hasil_o = {
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
			Ekspresi_wajah.Db.insert_hasil(semua_hasil_o)

			dir_file_name 	= 'static/data/latih_uji/' + direktori[j] + '_Hasil_OpenCV.png'
			file_name_o.append(direktori[j] + '_Hasil_OpenCV.png')
			cv2.imwrite(dir_file_name, img)

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

			waktu_loop 		= time.time()
			waktu_sekarang 	= session['waktu_sekarang'] + (waktu_loop - waktu_mulai)
			
			waktu_pelatihan = session['waktu_latih']
			session['waktu_sekarang'] = waktu_sekarang

			## setiap 1 menit
			if int(session['waktu_sekarang'] / (60 * 1)) == len(penanda_menit):
				durasi_menit = session['durasi']/60
				jumlah_file_teruji.append({
					str(round(durasi_menit, 0)) : len(j_data_uji)
				})
				penanda_menit.append(str(round(durasi_menit, 0)))

			## cek waktu_sekarang + waktu pelatihan apakah lebih dari 30 menit
			if session['waktu_sekarang'] + waktu_pelatihan >= (60 * 30):
				flash('Waktu pelatihan telah mencapai 30 menit, proses dihentikan!')
				break;

		waktu_selesai = time.time()
		durasi = waktu_selesai - waktu_mulai
		session['waktu_uji'] = durasi if session['waktu_uji'] is None else (session['waktu_uji'] + durasi)

		# for i in range(len(jumlah_data_teruji)):
		# 	for key,value in jumlah_data_teruji[i].items():
		# 		print(f"Jumlah file latih pada menit ke-{key} = {value}")

		return file_name_o, jarak_all_o, semua_hasil_o, hasil_final_o, jumlah_data_teruji



	def ambil_data_latih(data_latih):
		data_lat 			= np.array(data_latih)
		ciri 				= data_lat[:, 3:]
		kumpulan_ciri 		= ciri.astype(np.float64)
		kumpulan_kelas 		= data_lat[:, 2]

		return kumpulan_kelas, kumpulan_ciri 


	@page.route(f'{base}/hasil_detail/<int:id_file>/<string:waktu>', methods=['GET', 'POST'])
	def hasil_detail(id_file, waktu):

		data_pengujian 	= Ekspresi_wajah.Db.select_data_pengujian(id_file, waktu)
		jumlah_wajah 	= len(data_pengujian)
		ciri_all_s 		= []
		ciri_all_o 		= []
		id_ciri_s 		= []
		id_ciri_o 		= []
		data_jarak_s 	= []
		data_jarak_o 	= []
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

		print(f"HASIL S = {hasil_s} dan jumlah = {len(hasil_s)} dan tipe = {type(hasil_s)}")

		for i in range(len(id_ciri_s)):
			data_jarak_s.append(Ekspresi_wajah.Db.select_data_jarak(id_ciri_s[i]))
			data_jarak_o.append(Ekspresi_wajah.Db.select_data_jarak(id_ciri_o[i]))

		

		return Ekspresi_wajah.RT.tampilan_detail(ciri_all_s, ciri_all_o, data_pengujian, data_jarak_s, data_jarak_o, hasil_s, hasil_o)


	# ####################################
	

	@page.route(f'{base}/lakukan-uji', methods=['GET', 'POST'])
	def lakukan_uji():

		session['file_teruji'] = []
		session['waktu_sekarang'] = 0
		session['waktu_uji'] = 0
		session['waktu_latih'] 	= 0

		jarak_s 		= {}
		jarak_o 		= {}
		jarak 			= {}
		files 			= {}
		file_name_o 	= []
		semua_hasil_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		# print(f"Jumlah data uji = {jumlah_data}")
		waktu 			= []
		data_latih 		= []
		
		file_name_s, jarak_all_s, direktori, semua_hasil_s, hasil_final_s, id_pengujian_update, waktu = Ekspresi_wajah.uji_ciri_sendiri(data_uji, data_latih)

		# print(f"id_pengujian_update = {id_pengujian_update} dan jumlah = {len(id_pengujian_update)}")
		
		file_name_o, jarak_o, semua_hasil_o, hasil_final_o = Ekspresi_wajah.uji_ciri_opencv(data_uji, data_latih, direktori, id_pengujian_update, waktu)

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
			'WO'		: aW/jW if jW != 0 else 0,
			'B'			: aB/jB if jB != 0 else 0,
			'S'			: aS/jS if jS != 0 else 0,
			'M'			: aM/jM if jM != 0 else 0,
			'J'			: aJ/jJ if jJ != 0 else 0,
			'K'			: aK/jK if jK != 0 else 0,
			'T'			: aT/jT if jT != 0 else 0,
			'N'			: aN/jN if jN != 0 else 0
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

		print(f"Total waktu pelatihan: {round(session['waktu_latih'], 2)}s")
		print(f"Total waktu pengujian: {round(session['waktu_uji'], 2)}s")
		print(f"Total waktu: {round(session['waktu_latih'] + session['waktu_uji'], 2)}s")


		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = hasil_final_s, semua_hasil_o = hasil_final_o, waktu = waktu, akurasi = akurasi)


	@page.route(f'{base}/uji_data', methods=['GET', 'POST'])
	def uji_data():
		# if request.method == 'POST':
		# jumlah = request.form['jumlah']

		jumlah 		= [10, 20, 30, 68]
		print(f"JUMLAH = {jumlah}")
		print(f"JUMLAH[3] = {jumlah[3]}")
		kum_ekspresi= ['Bahagia', 'Sedih', 'Takut', 'Kaget']
		data_latih_s= []
		data_latih_o= []

		semua_hasil_s 	= []
		semua_hasil_o 	= []
		hasil_final_o 	= []
		target 			= []
		waktu 			= []
		data_uji 		= Ekspresi_wajah.Db.select_data_uji()
		jumlah_data 	= len(data_uji)
		print(f"Jumlah data uji = {jumlah_data}")

		#  Target

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


		result_s = []
		result_o = []
		# jumlah * setiap kelas
		for i in range(len(jumlah)):
			a = []
			for j in range(len(kum_ekspresi)):
				a.extend(Ekspresi_wajah.Db.select_sejumlah_data_latih('S', kum_ekspresi[j], jumlah[i]))
			data_latih_s.append(a) 

		for i in range(len(jumlah)):
			a = []
			for j in range(len(kum_ekspresi)):
				a.extend(Ekspresi_wajah.Db.select_sejumlah_data_latih('O', kum_ekspresi[j], jumlah[i]))
			data_latih_o.append(a) 

		data_latih = {
			'S'		: data_latih_s,
			'O'		: data_latih_o
		}

		#  Pengujian
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


		# pengujian ciri sendiri
		for j_s in range(len(data_latih['S'])):
			print(f"Jumlah data_latih ke-{j_s} = {len(data_latih['S'][j_s])}")
			file_name_s, jarak_all_s, direktori, semua_hasil_s, hasil_final_s, id_pengujian_update, waktu = Ekspresi_wajah.uji_ciri_sendiri(data_uji, data_latih['S'][j_s])

			hasil_s = []
			for i in range(jumlah_data):
				h_s = {}
				for key, value in hasil_final_s[i].items():
					if value != 0:
						h_s[key] = value
				hasil_s.append(h_s)

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

			r_all_s = []
			for i in range(jumlah_data):
				for key, value in rata2_akurasi_s.items():
					if key in akurasi_s[i].keys():
						v = int(value)
						r_all_s.append(key + '=' + str(v))
			print(f"_____________________________________________________js = {j_s}")
			result_s.append(r_all_s)

			print(f"Akurasi s ke - {j_s} = {r_all_s}")
			print(f"Result s  = {result_s} dan jumlah = {len(result_s)} dan tipe = {type(result_s)}")
			print(f"Data latih sendiri ke - {j_s} selesai diuji.")


		# Pengujian ciri OpenCV

		for j_o in range(len(data_latih['O'])):
			print(f"Jumlah data_latih ke-{j_o} = {len(data_latih['O'][j_o])}")
			file_name_o, jarak_o, semua_hasil_o, hasil_final_o, jumlah_data_teruji = Ekspresi_wajah.uji_ciri_opencv(data_uji, data_latih['O'][j_o], direktori, id_pengujian_update, waktu)

			hasil_o = []
			for i in range(jumlah_data):
				h_o = {}
				for key, value in hasil_final_o[i].items():
					if value != 0:
						h_o[key] = value
				hasil_o.append(h_o)

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
				'J'			: aJ/jJ if jJ != 0 else 0,
				'K'			: aK/jK if jK != 0 else 0,
				'T'			: aT/jT if jT != 0 else 0,
				'N'			: aN/jN if jN != 0 else 0
			}


			r_all_o = []
			for i in range(jumlah_data):
				for key, value in rata2_akurasi_o.items():
					if key in akurasi_o[i].keys():
						v = int(value)
						r_all_o.append(key + '=' + str(v))
			print(f"_____________________________________________________jo = {j_o}")
			result_o.append(r_all_o)

			print(f"Akurasi s ke - {j_o} = {r_all_o}")
			print(f"Result s  = {result_o} dan jumlah = {len(result_o)} dan tipe = {type(result_o)}")
			print(f"Data latih sendiri ke - {j_o} selesai diuji.")

		akurasi = {
			's'			: akurasi_s,
			'o'			: akurasi_o,
			'rata_s'	: result_s,
			'rata_o'	: result_o,
			'jumlah_data_uji' : jumlah_data,
			'jumlah_ekspresi' : len(kum_ekspresi)
		}

		print(f"Jumlah rata2 akurasi = {len(akurasi['rata_s'])}")
		print(f"akurasi akhir s = {akurasi['rata_s']}  dan tipe = {type(akurasi['rata_s'])}")
		print(f"akurasi akhir o = {akurasi['rata_o']}  dan tipe = {type(akurasi['rata_o'])}")

		return render_template('layout.html', data = { 'view' : 'latih_uji2', 'title' : 'Pengujian dan Pelatihan'}, target = target, akurasi = akurasi, files = data_latih)


	# @page.route(f'{base}/uji_dengan_waktu/<latih>/<uji>', methods=['GET', 'POST'])
	# def uji_dengan_waktu(latih, uji):
	# 	print(f"Latih = {latih} dan tipe = {type(latih)} dan jumlah = {len(latih)}")
	# 	print(f"uji = {uji} dan tipe = {type(uji)} dan jumlah = {len(uji)}")

	# 	if len(latih) <= 0:
	# 		latih = 0
	# 	elif len(uji) <= 0:
	# 		uji = 0 

	# 	return render_template('layout.html', data = { 'view' : 'uji_dengan_waktu', 'title' : 'Hasil Pengujian dan Pelatihan'}, latih = latih, uji = uji)

	def hitung_jarak(data1, data2):
		data = abs(data1-data2)
		return data


