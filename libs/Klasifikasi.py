from flask import Flask, Blueprint, abort
from sklearn.svm import SVC, LinearSVC
from sklearn.preprocessing import LabelEncoder

class Klasifikasi:

	page = Blueprint('Klasifikasi_page', __name__, template_folder = 'templates')
	base = '/klasifikasi'

	def __init__(self, ciri, kelas):
		self.encoder = LabelEncoder()
		self.encoder.fit(kelas)
		self.clf = LinearSVC()
		self.clf.fit(ciri, self.encoder.transform(kelas))

	def classify(self, ciri):
		result = self.clf.predict(ciri)
		return str(self.encoder.inverse_transform(result[0]))

