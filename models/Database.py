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
			# print(f"SELECTED: {data}")
			x = np.array(data)
			# print(x[:,1])
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

	def select_avg(self, kelas):
		try:
			query = "SELECT AVG(ciri1) AS avg_ciri1, AVG(ciri2) AS avg_ciri2, AVG(ciri3) AS avg_ciri3, AVG(ciri4) AS avg_ciri4, AVG(ciri5) AS avg_ciri5, AVG(ciri6) AS avg_ciri6, AVG(ciri7) AS avg_ciri7 FROM ciri WHERE kelas='" + kelas + "'"
			self.cur.execute(query)
			data = self.cur.fetchall()
			return data[0] if len(data) > 0 else None
		except:
			print("Error")
			return None
