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
		img_biner 	= grayscale.point(lambda p: p > threshold and 255)
		img_biner 	= np.array(img_biner)
		return img_biner