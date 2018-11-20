from PIL import Image
import cv2, numpy as np, random
from libs.GMI import GMI
from libs.OpenCV import OpenCV
import os
from time import gmtime, strftime


class Deteksi_wajah:

	OC  = OpenCV()	

	def resize_image(self, image, file_name, direktori, dir2):
		img1 		= Image.open(image)
		width 		= 384
		height 		= 288
		img2 		= img1.resize((width, height))

		if dir2 == 'uji':
			path = 'data/resize/'+ direktori
		else:
			path = 'data/resize/'+ direktori + '/' + dir2

		if os.path.exists(path) is False:
			os.makedirs(path, exist_ok=True)

		path2 = str(path) + '/' + str(file_name)
		img2.save(path2)
		
		return path2


	def deteksi(self, ket, path, dir1, dir2):

		faces, img 	= Deteksi_wajah.OC.deteksi(path)
		path_wajah 	= os.getcwd() + '\\data\\'+ ket +'\\' + dir1 + '\\' + dir2 + '\\' + '01.png'

		for f in faces:
			x, y, w, h 		= [v for v in f]
			sub_face 		= img[y:y+h, x:x+w]

			cv2.imwrite(path_wajah, sub_face)
		return path_wajah


	############################################################################

	

	# fungsi untuk mengambil piksel sub window
	def get_sliding_window(self, matrix, x, y, size = 24):
		return matrix[x:x+size, y:y+size]

	def rectangle_a(self, sliding_window, x, y, size=(1, 2)): # size (1,4)
		A = 0 if x <= 0 or y <= 0 else sliding_window[x - 1, y - 1]
		B = 0 if x <= 0 else sliding_window[x - 1, (y + size[1]  - 1) // 2]
		C = 0 if y <= 0 else sliding_window[x + size[0] - 1, y - 1]
		D = sliding_window[x + size[0] - 1, (y + size[1] - 1) // 2]

		black = D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		A = 0 if x <= 0 else sliding_window[x - 1, ((y + size[1]) - 1) // 2]
		B = 0 if x <= 0 else sliding_window[x - 1, (y + size[1]) - 1]
		C = sliding_window[x + size[0] - 1, ((y + size[1]) - 1) // 2]
		D = sliding_window[x + size[0] - 1, (y + size[1]) - 1]

		white = D + A - (B + C)
		print(f"putih = {D} + {A} - {B} + {C}")

		hasil = abs(black - white)
		print(f"hasil = {hasil}\n")

		return hasil

	def rectangle_b(self, sliding_window, x, y, size=(2, 1)):
		A = 0 if x <= 0 or y <= 0 else sliding_window[x - 1, y - 1]
		B = 0 if x <= 0 else sliding_window[x - 1, y + size[1]  - 1]
		C = 0 if y <= 0 else sliding_window[(x + size[0] - 1) // 2, y - 1]
		D = sliding_window[(x + size[0] - 1) // 2, y + size[1] - 1]

		black = D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		A = 0 if y <= 0 else sliding_window[(x + size[0] - 1) // 2, y - 1]
		B = sliding_window[(x + size[0] - 1) // 2, y + size[1] - 1]
		C = 0 if y <= 0 else sliding_window[x + size[0] - 1, y - 1]
		D = sliding_window[x + size[0] - 1, (y + size[1]) - 1]

		white = D + A - (B + C)
		print(f"putih = {D} + {A} - {B} + {C}")

		hasil = abs(black - white)
		print(f"hasil = {hasil}\n")

		return hasil

	def rectangle_c(self, sliding_window, x, y, size=(1, 3)):
		chunk_size = size[1] // 3

		ul_x = x - 1
		ul_y = y - 1
		ur_x = x - 1
		ur_y = y + chunk_size - 1
		bl_x = x + size[0] - 1
		bl_y = y - 1
		br_x = x + size[0] - 1
		br_y = y + chunk_size - 1

		A = 0 if x <= 0 or y <= 0 else sliding_window[ul_x, ul_y]
		B = 0 if x <= 0 else sliding_window[ur_x, ur_y]
		C = 0 if y <= 0 else sliding_window[bl_x, bl_y]
		D = sliding_window[br_x, br_y]

		black = D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		A = 0 if x <= 0 else sliding_window[ul_x, ul_y + chunk_size]
		B = 0 if x <= 0 else sliding_window[ur_x, ur_y + chunk_size]
		C = sliding_window[bl_x, bl_y + chunk_size]
		D = sliding_window[br_x, br_y + chunk_size]

		white = D + A - (B + C)
		print(f"putih = {D} + {A} - {B} + {C}")

		A = 0 if x <= 0 else sliding_window[ul_x, ul_y + (chunk_size * 2)]
		B = 0 if x <= 0 else sliding_window[ur_x, ur_y + (chunk_size * 2)]
		C = sliding_window[bl_x, bl_y + (chunk_size * 2)]
		D = sliding_window[br_x, br_y + (chunk_size * 2)]

		black += D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		hasil = abs(black - white)
		print(f"hasil = {hasil}\n")

		return hasil

	def rectangle_d(self, sliding_window, x, y, size=(2, 2)):
		chunk_x = size[0] // 2
		chunk_y = size[1] // 2

		ul_x = x - 1
		ul_y = y - 1
		ur_x = x - 1
		ur_y = y + chunk_y - 1
		bl_x = x + chunk_x - 1
		bl_y = y - 1
		br_x = x + chunk_x - 1
		br_y = y + chunk_y - 1

		A = 0 if x <= 0 or y <= 0 else sliding_window[ul_x, ul_y]
		B = 0 if x <= 0 else sliding_window[ur_x, ur_y]
		C = 0 if y <= 0 else sliding_window[bl_x, bl_y]
		D = sliding_window[br_x, br_y]

		black = D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		A = 0 if x <= 0 else sliding_window[ul_x, ul_y + chunk_y]
		B = 0 if x <= 0 else sliding_window[ur_x, ur_y + chunk_y]
		C = sliding_window[bl_x, bl_y + chunk_y]
		D = sliding_window[br_x, br_y + chunk_y]

		white = D + A - (B + C)
		print(f"putih = {D} + {A} - {B} + {C}")

		A = 0 if y <= 0 else sliding_window[ul_x + chunk_x, ul_y]
		B = sliding_window[ur_x + chunk_x, ur_y]
		C = 0 if y <= 0 else sliding_window[bl_x + chunk_x, bl_y]
		D = sliding_window[br_x + chunk_x, br_y]

		white += D + A - (B + C)
		print(f"putih = {D} + {A} - {B} + {C}")

		A = sliding_window[ul_x + chunk_x, ul_y + chunk_y]
		B = sliding_window[ur_x + chunk_x, ur_y + chunk_y]
		C = sliding_window[bl_x + chunk_x, bl_y + chunk_y]
		D = sliding_window[br_x + chunk_x, br_y + chunk_y]

		black += D + A - (B + C)
		print(f"hitam = {D} + {A} - {B} + {C}")

		hasil = abs(black - white)
		print(f"hasil = {hasil}\n")

		return hasil

	def deteksi_vj(self):
		# Praproses Ke Gray Scale
		# image = "D:\\bahagia.png"
		# im = self.resize_image(image)
		# im 	= Image.open(image)
		# im	= im.convert('L') 
		# im 	= np.array(im)
		# im = np.random.randint(255, size=(24, 24))
		# print(im)
		# sliding_window = self.get_sliding_window(im, 0, 0)
		# integral_image = self.integral_image(sliding_window)
		# im = np.array([
		# 	[2, 6, 13, 18, 26],
		# 	[3, 12, 20, 32, 47],
		# 	[8, 23, 40, 57, 78],
		# 	[16, 40, 67, 90, 118],
		# 	[26, 62, 97, 123, 157]
		# ])


		im = np.array([
			[2, 4, 7, 5, 8],
			[1, 5, 1, 7, 7],
			[5, 6, 9, 5, 6],
			[8, 9, 10, 6, 7],
			[10, 12, 8, 3, 6]
		])

		print("Deteksi Wajah dengan Metode Viola Jones")
		print(f"\nMisalkan, sub window yang telah dipraproses ke citra gray scale untuk deteksi wajah berupa matriks 5 x 5 berikut ini")
		print(f"Matriks =\n{im}")
		print("\n1. Ubah sub window ke dalam citra integral")
		im_integral = self.integral_image(im)
		print(f"matriks =\n{im_integral}")
		print("\n2. Menghitung fitur Haar")
		print("- Hitung fitur Haar tipe pertama")
		
		tipe_1 = []
		tipe_1.append(self.rectangle_a(im_integral, 0, 0, (1,2) )) # minimal untuk ukuran x=1, y=2
		tipe_1.append(self.rectangle_a(im_integral, 0, 1, (1,2) ))
		tipe_1.append(self.rectangle_a(im_integral, 0, 2, (1,2) ))
		tipe_1.append(self.rectangle_a(im_integral, 0, 3, (1,2) ))
		tipe_1.append(self.rectangle_a(im_integral, 1, 0, (1,2) )) 
		tipe_1.append(self.rectangle_a(im_integral, 1, 1, (1,2) ))
		tipe_1.append(self.rectangle_a(im_integral, 1, 2, (1,2) ))
		tipe_1.append(self.rectangle_a(im_integral, 1, 3, (1,2) ))


		print("\n- Hitung fitur Haar tipe kedua")
		
		tipe_2 = []
		tipe_2.append(self.rectangle_b(im_integral, 0, 0, (2,1) )) # minimal untuk ukuran x=2, y=1
		tipe_2.append(self.rectangle_b(im_integral, 0, 1, (2,1) ))
		tipe_2.append(self.rectangle_b(im_integral, 0, 2, (2,1) ))
		tipe_2.append(self.rectangle_b(im_integral, 0, 3, (2,1) ))
		tipe_2.append(self.rectangle_b(im_integral, 2, 0, (2,1) )) 
		tipe_2.append(self.rectangle_b(im_integral, 2, 1, (2,1) ))
		tipe_2.append(self.rectangle_b(im_integral, 2, 2, (2,1) ))
		tipe_2.append(self.rectangle_b(im_integral, 2, 3, (2,1) ))

		print("\n- Hitung fitur Haar tipe ketiga")
		
		tipe_3 = []
		tipe_3.append(self.rectangle_c(im_integral, 0, 0, (1,3) )) # minimal untuk ukuran x=2, y=1
		tipe_3.append(self.rectangle_c(im_integral, 0, 1, (1,3) ))
		tipe_3.append(self.rectangle_c(im_integral, 0, 2, (1,3) ))
		tipe_3.append(self.rectangle_c(im_integral, 1, 0, (1,3) )) 
		tipe_3.append(self.rectangle_c(im_integral, 1, 1, (1,3) ))
		tipe_3.append(self.rectangle_c(im_integral, 1, 2, (1,3) ))
		tipe_3.append(self.rectangle_c(im_integral, 2, 0, (1,3) )) 
		tipe_3.append(self.rectangle_c(im_integral, 2, 1, (1,3) ))

		print("\n- Hitung fitur Haar tipe keempat")
		
		tipe_4 = []
		tipe_4.append(self.rectangle_d(im_integral, 0, 0, (2,2) )) # minimal untuk ukuran x=2, y=1
		tipe_4.append(self.rectangle_d(im_integral, 0, 1, (2,2) ))
		tipe_4.append(self.rectangle_d(im_integral, 0, 2, (2,2) ))
		tipe_4.append(self.rectangle_d(im_integral, 0, 3, (2,2) )) 
		tipe_4.append(self.rectangle_d(im_integral, 1, 0, (2,2) ))
		tipe_4.append(self.rectangle_d(im_integral, 1, 1, (2,2) ))
		tipe_4.append(self.rectangle_d(im_integral, 1, 2, (2,2) )) 
		tipe_4.append(self.rectangle_d(im_integral, 1, 3, (2,2) ))

		print(f"Fitur Haar Tipe 1 = {tipe_1} dan jumlah fitur tipe 1 = {len(tipe_1)}")
		print(f"Fitur Haar Tipe 2 = {tipe_2} dan jumlah fitur tipe 2 = {len(tipe_2)}")
		print(f"Fitur Haar Tipe 3 = {tipe_3} dan jumlah fitur tipe 3 = {len(tipe_3)}")
		print(f"Fitur Haar Tipe 4 = {tipe_4} dan jumlah fitur tipe 4 = {len(tipe_4)}\n")

		return "Deteksi Wajah"



	def integral_image(self, im):
		for x, row in enumerate(im):
			for y, col in enumerate(row):
				if x > 0: im[x][y] += im[x - 1][y]
				if y > 0: im[x][y] += im[x][y - 1]
				if x > 0 and y > 0: im[x][y] -= im[x - 1][y - 1]
		return im