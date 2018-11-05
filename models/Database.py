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
			self.db.commit()

			data = self.cur.fetchall()

			x = np.array(data)
			kumpulan_kelas = x[:, 2]

			return kumpulan_kelas
		except:
			print("error")
			return None

	def select_ciri(self, table, ket):
		try:
			query = 'SELECT * FROM ' + table + ' WHERE ket = "' + ket + '"'
			self.cur.execute(query)
			self.db.commit()
			data = self.cur.fetchall()
			x = np.array(data)
			ciri = x[:, 3:]
			kumpulan_ciri = ciri.astype(np.float64)

			return kumpulan_ciri
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

	def select_hasil(self, col, id_file, waktu):
		try:
			self.cur.execute("SELECT "+ col +" FROM pengujian WHERE id_file = '" + str(id_file) + "' AND waktu = '" + waktu + "'")
			data_hasil = self.cur.fetchall()
			return data_hasil
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
			self.db.commit()
			data = self.cur.fetchall()
			return data
		except:
			print("Error select file uji")
			return None

	def select_data_pengujian(self, id_file, waktu):
		try:
			self.cur.execute("SELECT * FROM pengujian WHERE id_file = '" + str(id_file) + "' AND waktu = '" + waktu + "'")
			self.db.commit()
			data = self.cur.fetchall()
			return data
		except:
			print("Error select pengujian")
			return None

	def select_ciri_pengujian(self, id_ciri_pengujian, ket):
		try:
			self.cur.execute("SELECT * FROM ciri_pengujian WHERE id_ciri_pengujian = '" + str(id_ciri_pengujian) + "' AND ket = '" + ket + "'")
			self.db.commit()
			data = self.cur.fetchall()
			data = np.array(data)

			return data[:, 2:]
		except:
			print("error select ciri pengujian")
			return None

	def select_pengujian_first_row(self):
		try:
			self.cur.execute("SELECT * FROM pengujian ORDER BY id_pengujian DESC LIMIT 1")
			self.db.commit()
			data_pengujian = self.cur.fetchall()
			return data_pengujian
		except:
			print("Error first row pengujian")
			return None

	def select_first_row(self):
		try:
			self.cur.execute("SELECT * FROM ciri_pengujian ORDER BY id_ciri_pengujian DESC LIMIT 1")
			self.db.commit()
			data = self.cur.fetchall()
			return data
		except:
			print("Error first row")
			return None

	def select_avg(self, table, kelas):
		try:
			query = "SELECT AVG(ciri1) AS avg_ciri1, AVG(ciri2) AS avg_ciri2, AVG(ciri3) AS avg_ciri3, AVG(ciri4) AS avg_ciri4, AVG(ciri5) AS avg_ciri5, AVG(ciri6) AS avg_ciri6, AVG(ciri7) AS avg_ciri7 FROM " + table + " WHERE kelas='" + kelas + "'"
			self.cur.execute(query)
			self.db.commit()
			data_rata_rata = self.cur.fetchall()
			return data_rata_rata[0] if len(data_rata_rata) > 0 else None
		except:
			print("Error AVG")
			return None

	def select_hasil_ciri_pengujian_s(self, waktu_mulai, waktu_akhir):
		try:
			query = "SELECT ciri_pengujian.id_ciri_pengujian as id_ciri_pengujian, ciri_pengujian.ciri1, ciri_pengujian.ciri2, ciri_pengujian.ciri3, ciri_pengujian.ciri4, ciri_pengujian.ciri5, ciri_pengujian.ciri6, ciri_pengujian.ciri7, pengujian.hasil_sendiri as kelas FROM ciri_pengujian inner join pengujian on pengujian.id_ciri_pengujian_s = ciri_pengujian.id_ciri_pengujian where pengujian.waktu BETWEEN '"+ waktu_mulai +"' AND '"+ waktu_akhir +"';"
			self.cur.execute(query)
			self.db.commit()
			data = self.cur.fetchall()
			return data
		except:
			print("Error select hasil ciri pengujian s")
			return None

	def select_hasil_ciri_pengujian_o(self, waktu_mulai, waktu_akhir):
		try:
			query = "SELECT  ciri_pengujian.id_ciri_pengujian as id_ciri_pengujian, ciri_pengujian.ciri1, ciri_pengujian.ciri2, ciri_pengujian.ciri3, ciri_pengujian.ciri4, ciri_pengujian.ciri5, ciri_pengujian.ciri6, ciri_pengujian.ciri7, pengujian.hasil_opencv as kelas FROM ciri_pengujian inner join pengujian on pengujian.id_ciri_pengujian_o = ciri_pengujian.id_ciri_pengujian where pengujian.waktu BETWEEN '"+ waktu_mulai +"' AND '"+ waktu_akhir +"';"
			self.cur.execute(query)
			self.db.commit()
			data = self.cur.fetchall()
			return data
		except:
			print("Error select hasil ciri pengujian o")
			return None
