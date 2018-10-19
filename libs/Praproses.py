from PIL import Image
import numpy as np

class Praproses:

	def biner(self, img):
		im 			= Image.open(img)
		im			= im.convert('L')
		im 			= np.array(im)

		grayscale 	= Image.fromarray(im)
		threshold 	= 256 / 2
		img_biner 	= grayscale.point(lambda p: p > threshold and 255)
		img_biner 	= np.array(img_biner)
		return img_biner