from flask import render_template

class Render_template:

	def tampilan_latih_uji(self):
		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'})	

	def tampilan_pengujian1(self, jarak, files, target, hasil_final_s, hasil_final_o, waktu, akurasi, jumlah_data_teruji, direktori):
		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = hasil_final_s, semua_hasil_o = hasil_final_o, waktu = waktu, akurasi = akurasi, jumlah_data_teruji = jumlah_data_teruji, direktori = direktori)

	def tampilan_pengujian2(self, semua_hasil):
		return render_template('layout.html', data = { 'view' : 'pengujian', 'title' : 'Pengujian dan Pelatihan'}, semua_hasil = semua_hasil)

	def tampilan_detail(self, ciri_all_s, ciri_all_o, data_pengujian, data_jarak_s, data_jarak_o, hasil_s, hasil_o):
		return render_template('layout.html', data = { 'view' : 'detail', 'title' : 'Pengujian dan Pelatihan'}, ciri_s = ciri_all_s, ciri_o = ciri_all_o, data_pengujian = data_pengujian, data_jarak_s = data_jarak_s, data_jarak_o = data_jarak_o, hasil_s = hasil_s, hasil_o = hasil_o)

