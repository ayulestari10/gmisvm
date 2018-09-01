from flask import Flask, Blueprint, abort
from PIL import Image
import numpy as np

class Praproses:

	page = Blueprint('Praproses_page', __name__, template_folder = 'templates')
	base = '/praproses'

	def biner(self, img):
		im 			= Image.open(img)
		im			= im.convert('L')
		im 			= np.array(im)

		grayscale 	= Image.fromarray(im)
		threshold 	= 256 / 2
		binary 		= grayscale.point(lambda p: p > threshold and 255)
		# binary.save('result/'+ file +'.png')
		return np.array(binary)
	

	def grayscale():
		return 'grayscale'