from flask import Flask, Blueprint, abort
import MySQLdb
import numpy as np

class Database:

	def __init__(self, hostname, username, password, database):
		self.db = MySQLdb.connect(hostname, username, password, database)
		self.cur = self.db.cursor()

	def select_kelas(self, table, ket):
		try:

			query = "SELECT * FROM " + table + ' WHERE ket = "' + ket + '"'
			self.cur.execute(query)

			data = self.cur.fetchall()

			x = np.array(data)
			kelas = x[:, 2]

			return kelas
		except:
			print("error")
			return None

	def select_ciri(self, table, ket):
		try:
			query = 'SELECT * FROM ' + table + ' WHERE ket = "' + ket + '"'
			self.cur.execute(query)

			data = self.cur.fetchall()
			x = np.array(data)
			ciri = x[:, 3:]
			kum_ciri = ciri.astype(np.float64)

			return kum_ciri
		except:
			print("error")
			return None

	def insert_ciri(self, table, ciri, ket):

		try:
			self.cur.execute("INSERT INTO "+ table +"(ket, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + ket + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			self.db.commit()
		except:
			self.db.rollback()

	def insert_ciri_pelatihan(self, table, kelas, ciri, ket):

		try:
			self.cur.execute("INSERT INTO "+ table +"(ket, kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + ket + "'", "'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			self.db.commit()
		except:
			self.db.rollback()

	def insert_pengujian(self, data):

		try:
			self.cur.execute("INSERT INTO pengujian(id_file, id_ciri_pengujian_s, waktu, hasil_sendiri, direktori) VALUES (%s, %s, %s, %s, %s)" % ("'" + data['id_file'] + "'", "'" + data['id_ciri_pengujian_s'] + "'", "'" + data['waktu'] + "'", "'" + data['hasil_sendiri'] + "'", "'" + data['direktori'] + "'"))

			self.db.commit()
		except:
			print("error pengujian")
			self.db.rollback()

	def update_pengujian(self, data):

		try:
			self.cur.execute("UPDATE pengujian SET id_ciri_pengujian_o = '" + data['id_ciri_pengujian_o'] + "', hasil_opencv = '" + data['hasil_opencv'] + "' WHERE id_pengujian = '" + str(data['id_pengujian']) + "'")

			self.db.commit()
		except:
			print("error update pengujian")
			self.db.rollback()

	def insert_jarak_ciri(self, id_ciri_pengujian, kelas, data):
		try:
			self.cur.execute("INSERT INTO jarak(id_ciri_pengujian, kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" % (id_ciri_pengujian, "'" + kelas + "'", data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

			self.db.commit()
		except:
			print("Error Insert Jarak Ciri")
			self.db.rollback()

	def select_hasil(self, col, id_file, waktu):
		try:
			self.cur.execute("SELECT "+ col +" FROM pengujian WHERE id_file = '" + str(id_file) + "' AND waktu = '" + waktu + "'")
			data = self.cur.fetchall()
			return data
		except:
			print("Error select hasil")
			return None


	def insert_hasil(self, data):

		try:
			self.cur.execute("INSERT INTO hasil(id_file, ket, jumlah_wajah_terdeteksi, klasifikasi_bahagia, klasifikasi_sedih, klasifikasi_marah, klasifikasi_jijik, klasifikasi_kaget, klasifikasi_takut, klasifikasi_natural) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (data['id_file'], "'" + data['ket'] + "'", data['wajah'], data['bahagia'], data['sedih'], data['marah'], data['jijik'], data['kaget'], data['takut'], data['natural'] ))

			self.db.commit()
		except:
			print("error insert hasil")
			self.db.rollback()


	def select_data_uji(self):
		try:
			self.cur.execute("SELECT * FROM file_uji")
			data = self.cur.fetchall()
			return data
		except:
			print("Error select file uji")
			return None

	def select_data_uji_jumlah(self, jumlah):
		try:
			self.cur.execute("SELECT * FROM file_uji ORDER BY id_file ASC LIMIT " + str(jumlah))
			data = self.cur.fetchall()
			return data
		except:
			print("Error select file uji jumlah")
			return None

	def select_data_pengujian(self, id_file, waktu):
		try:
			self.cur.execute("SELECT * FROM pengujian WHERE id_file = '" + str(id_file) + "' AND waktu = '" + waktu + "'")
			data = self.cur.fetchall()
			print(f"Data cantik = {data}")
			return data
		except:
			print("Error select pengujian")
			return None

	def select_join_hasil(self, ket):
		try:
			self.cur.execute("SELECT * FROM hasil inner join file_uji on hasil.id_file = file_uji.id_file WHERE hasil.ket = '" + ket + "'")
			data = self.cur.fetchall()
			return data
		except:
			print("Error select hasil uji")
			return None
	
	def select_target(self, id_file):
		try:
			self.cur.execute("SELECT * FROM file_uji WHERE id_file = '" + str(id_file) + "'")
			data = self.cur.fetchall()
			return data
		except:
			print("Error select target")
			return None

	def select_ciri_pengujian(self, id_ciri_pengujian, ket):
		try:
			self.cur.execute("SELECT * FROM ciri_pengujian WHERE id_ciri_pengujian = '" + str(id_ciri_pengujian) + "' AND ket = '" + ket + "'")

			data = self.cur.fetchall()
			data = np.array(data)

			return data[:, 2:]
		except:
			print("error select ciri pengujian")
			return None

	def select_pengujian_first_row(self):
		try:
			self.cur.execute("SELECT * FROM pengujian ORDER BY id_pengujian DESC LIMIT 1")
			data = self.cur.fetchall()
			return data
		except:
			print("Error first row pengujian")
			return None

	def select_sejumlah_data_latih(self, ket, kelas, jumlah):
		try:
			self.cur.execute("SELECT * FROM ciri_pelatihan WHERE ket='" + ket + "' AND kelas='" + kelas +  "' ORDER BY id_ciri_pelatihan ASC LIMIT " + str(jumlah))
			data = self.cur.fetchall()
			data = np.array(data)
			return data[:, 3:]
		except:
			print("Error select sejumlah data uji")
			return None




	# ####



	def insert_ciri_pengujian(self, table, kelas, ciri):
		try:
			self.cur.execute("INSERT INTO "+ table +"(kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			self.db.commit()
		except:
			self.db.rollback()

	def insert_jarak2(self, data, id_tes):
		try:
			self.cur.execute("INSERT INTO jarak(id_tes, jarak_marah, jarak_jijik, jarak_takut, jarak_bahagia, jarak_sedih, jarak_kaget, jarak_natural) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % (id_tes, data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

			self.db.commit()
		except:
			print("Error Insert Jarak")
			self.db.rollback()

	def insert_jarak_min(self, id_tes, data):
		try:
			self.cur.execute("SELECT LEAST(jarak_marah, jarak_jijik, jarak_takut, jarak_bahagia, jarak_sedih, jarak_kaget, jarak_natural) as jarak_min From jarak where id_tes = " + id_tes)
			jarak_min = self.cur.fetchall()
			
			jarak_min2, = jarak_min
			jarak_min3, = jarak_min2
			jarak_min3  = str(jarak_min3)
			self.cur.execute("UPDATE jarak SET jarak_min = " + jarak_min3 + " WHERE id_tes = " + id_tes)
			self.db.commit()

			return jarak_min3
		except:
			print("Error Jarak Min")
			self.db.rollback()

	def select_jarak(self, id_tes):
		try:
			self.cur.execute("SELECT * FROM jarak WHERE id_tes = " + id_tes)
			data = self.cur.fetchall()
			return data
		except:
			print("Error select jarak")
			return None

	def select_first_row(self):
		try:
			self.cur.execute("SELECT * FROM ciri_pengujian ORDER BY id_ciri_pengujian DESC LIMIT 1")
			data = self.cur.fetchall()
			return data
		except:
			print("Error first row")
			return None


	def select_id(self, ciri, jarak):
		try:
			self.cur.execute("SELECT id_ciri FROM ciri_test WHERE ciri1 = " + ciri[0] + " AND ciri2 = " + ciri[1] + " AND ciri3 = " + ciri[2] + " AND ciri4 = " + ciri[3] + " AND ciri5 = " + ciri[4] + " AND ciri6 = " + ciri[5] + " AND ciri7 = " + ciri[6] + " AND jarak = " + jarak)
		except:
			print("Error ID")
			return None

	def select_avg(self, table, kelas):
		try:
			query = "SELECT AVG(ciri1) AS avg_ciri1, AVG(ciri2) AS avg_ciri2, AVG(ciri3) AS avg_ciri3, AVG(ciri4) AS avg_ciri4, AVG(ciri5) AS avg_ciri5, AVG(ciri6) AS avg_ciri6, AVG(ciri7) AS avg_ciri7 FROM " + table + " WHERE kelas='" + kelas + "'"
			self.cur.execute(query)
			data = self.cur.fetchall()
			return data[0] if len(data) > 0 else None
		except:
			print("Error AVG")
			return None
