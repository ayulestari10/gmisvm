from flask import Flask, Blueprint, abort

class Klasifikasi:

	page = Blueprint('Klasifikasi_page', __name__, template_folder = 'templates')
	base = '/klasifikasi'


	def Multi_SVM():
		return 'multi svm'
