from flask import render_template

class Render_template:

	def tampilan_latih_uji(self, jarak, files, target, semua_hasil_s, semua_hasil_o, waktu, akurasi, hasil_waktu_uji, hasil_waktu_latih):
		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'}, jarak = jarak, files = files, target = target, semua_hasil_s = semua_hasil_s, semua_hasil_o = semua_hasil_o, waktu = waktu, akurasi = akurasi, hasil_waktu_uji = hasil_waktu_uji, hasil_waktu_latih = hasil_waktu_latih)

	def tampilan_latih_uji2(self):
		return render_template('layout.html', data = { 'view' : 'latih_uji', 'title' : 'Pengujian dan Pelatihan'})

	def tampilan_detail(self, ciri_all_s, ciri_all_o, data_pengujian, data_jarak_s, data_jarak_o, hasil_s, hasil_o):
		return render_template('layout.html', data = { 'view' : 'detail', 'title' : 'Pengujian dan Pelatihan'}, ciri_s = ciri_all_s, ciri_o = ciri_all_o, data_pengujian = data_pengujian, data_jarak_s = data_jarak_s, data_jarak_o = data_jarak_o, hasil_s = hasil_s, hasil_o = hasil_o)

