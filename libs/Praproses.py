from flask import Flask, Blueprint, abort

class Praproses:

	page = Blueprint('Praproses_page', __name__, template_folder = 'templates')
	base = '/praproses'

	def biner():
		return 'biner'

	def grayscale():
		return 'grayscale'