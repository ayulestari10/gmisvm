from flask import Flask, Blueprint, abort
import MySQLdb
import numpy as np

class Database:

	def __init__(self, hostname, username, password, database):
		self.db = MySQLdb.connect(hostname, username, password, database)
		self.cur = self.db.cursor()

	def select_kelas(self, table):
		try:

			query = "SELECT * FROM " + table
			self.cur.execute(query)

			data = self.cur.fetchall()

			x = np.array(data)
			kelas = x[:, 1]

			return kelas
		except:
			print("error")
			return None

	def select_ciri(self, table):
		try:
			query = "SELECT * FROM " + table
			self.cur.execute(query)

			data = self.cur.fetchall()
			x = np.array(data)
			ciri = x[:, 2:]
			kum_ciri = ciri.astype(np.float64)

			return kum_ciri
		except:
			print("error")
			return None

	def insert_ciri(self, table, kelas, ciri):

		try:
			self.cur.execute("INSERT INTO "+ table +"(kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6]))

			self.db.commit()
		except:
			self.db.rollback()

	def insert_ciri_test(self, table, kelas, ciri, jarak):
		try:
			self.cur.execute("INSERT INTO "+ table +"(kelas, ciri1, ciri2, ciri3, ciri4, ciri5, ciri6, ciri7, jarak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" % ("'" + kelas + "'", ciri[0], ciri[1], ciri[2], ciri[3], ciri[4], ciri[5], ciri[6], jarak))

			self.db.commit()
		except:
			self.db.rollback()

	def insert_jarak(self, data, id_tes):
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
			self.cur.execute("SELECT * FROM ciri_test ORDER BY id_ciri DESC LIMIT 1")
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
