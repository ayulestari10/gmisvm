from flask import Flask, Blueprint, abort

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] 		= 'localhost'
app.config['MYSQL_DATABASE_USER'] 		= 'root'
app.config['MYSQL_DATABASE_PASSWORD'] 	= ''
app.config['MYSQL_DATABASE_DB'] 			= 'gmisvm'
mysql.init_app(app)

class Database:

	page = Blueprint('Database_page', __name__, template_folder = 'templates')
	base = 'database'

	def select_kelas(table):
		cur = mysql.get_db().cursor()
		cur.execute("SELECT * FROM ciri_ck_modif")

		data = cur.fetchall()

		x = np.array(data)
		kelas = x[:, 1]

		return kelas

	def select_ciri(table):
		cur = mysql.get_db().cursor()
		cur.execute("SELECT * FROM ciri_ck_modif")

		data = cur.fetchall()
		print(f"SELECTED: {data}")
		x = np.array(data)
		print(x[:,1])
		ciri = x[:, 2:]
		kum_ciri = ciri.astype(np.float64)

		return kum_ciri
