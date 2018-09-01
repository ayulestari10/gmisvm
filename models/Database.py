from flask import Flask, Blueprint, abort
import MySQLdb
import numpy as np

class Database:

	def __init__(self, hostname, username, password, database):
		self.db = MySQLdb.connect(hostname, username, password, database)
		self.cur = self.db.cursor()

	def select_kelas(self, table):
		try:
			self.cur.execute("SELECT * FROM ciri_ck")

			data = self.cur.fetchall()

			x = np.array(data)
			kelas = x[:, 1]

			return kelas
		except:
			print("error")
			return None

	def select_ciri(self, table):
		try:
			self.cur.execute("SELECT * FROM ciri_ck")

			data = self.cur.fetchall()
			print(f"SELECTED: {data}")
			x = np.array(data)
			print(x[:,1])
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
