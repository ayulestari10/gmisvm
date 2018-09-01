from flask import Flask, Blueprint, abort,  render_template, request, flash, redirect, url_for
from PIL import Image
from jinja2 import TemplateNotFound

class Ekspresi_wajah:

	page = Blueprint('Ekspresi_wajah_page', __name__, template_folder = 'templates')
	base = '/ekspresi-wajah'


	@page.route(f'{base}/')
	def home():
		try:
			return render_template('home.html')
		except TemplateNotFound:
			abort(404)

	@page.route(f'{base}/pelatihan')
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
					berkas_citra = deteksi_wajah("training", berkas, directory, dir2)

					im 			= Image.open(berkas_citra)
					im			= im.convert('L')
					im 			= np.array(im)

					greyscale 	= Image.fromarray(equ)
					greyscale.save('result/equ/' + file + '.png')

					# threshold 	= 256 / 2
					# binary 		= greyscale.point(lambda p: p > threshold and 255)
					# binary.save('result/result_binary9.jpg')
					# pixel_binary= np.array(binary)

					gmi 		= GMI(equ) 
					gmi.hitungMomenNormalisasi()
					ciri 		= gmi.hitungCiri()
					

					# print(f"ini ciri sebelum = {ciri}")

					# ciri = -np.sign(ciri) * np.log10(np.abs(ciri))

					# HU OpenCV
					# ciri 		= cv2.HuMoments(cv2.moments(pixel_binary)).flatten()
					# print(f"ini ciri sesudah = {ciri}")

					nilai_ciri1 = ciri[0]
					nilai_ciri2 = ciri[1]
					nilai_ciri3 = ciri[2]
					nilai_ciri4 = ciri[3]
					nilai_ciri5 = ciri[4]
					nilai_ciri6 = ciri[5]
					nilai_ciri7 = ciri[6]
					kelas 		= jenis_kelas

					cur = mysql.get_db().cursor()
					cur.execute("INSERT INTO ciri_his_equ(kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

					print("INSERT INTO ciri_his_equ(kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

					mysql.get_db().commit()

			flash('Data pelatihan berhasil dilatih')
			return redirect(url_for('.pelatihan'))

		return render_template('layout.html', data = { 'view' : 'pelatihan', 'title' : 'Pelatihan'})

	@page.route(f'{base}/pengujian')
	def pengujian():
		if request.method == "POST":
			f = request.files['foto']
			
			directory = strftime("%Y-%m-%d-%H-%M-%S")

			filename = 'data/testing/' + secure_filename(directory + '_' + f.filename)
			f.save(filename)

			cwd = os.getcwd()

			berkas 		= cwd + "\\data\\testing\\" + secure_filename(directory + '_' + f.filename)
			print("berkas = " + berkas)

			if not os.path.exists(cwd + "\\data\\testing\\" + directory + "\\coba"):
				os.makedirs(cwd + "\\data\\testing\\" + directory + "\\coba")
				print(cwd + "\\data\\testing\\" + directory + "\\coba")

			berkas_citra = deteksi_wajah("testing", berkas, directory, "coba")

			im 			= Image.open(berkas_citra)
			biner		= im.convert('L')
			pixel 		= np.array(biner)
			
			greyscale 	= Image.fromarray(pixel)
			# greyscale.save('result/result_greyscale.jpg')

			threshold 	= 256 / 2
			binary 		= greyscale.point(lambda p: p > threshold and 255)
			# binary.save('result/result_binary.jpg')
			pixel_binary= np.array(binary)

			gmi 		= GMI(pixel_binary)
			gmi.hitungMomenNormalisasi()
			ciri 		= gmi.hitungCiri()
			print(ciri)

			# Klasifikasi dengan svm

			kumpulan_ciri = select_ciri()
			kumpulan_kelas= select_kelasV2()
			lin_clf = LinearSVC()
			lin_clf.fit(kumpulan_ciri, encode_class(kumpulan_kelas))

			# dec = lin_clf.decision_function(kumpulan_ciri)
			# hasil = dec.shape[1]
			# print(f"Ini hasilnya = {hasil}")
			
			# con = confusion_matrix(kumpulan_kelas, ["jijik"])
			# print(f"Confusion Matrix = {con}")
			result = lin_clf.predict([ciri])
			
			print(f"Kelas: {decode_class(kumpulan_kelas, result)}")

		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian'})

