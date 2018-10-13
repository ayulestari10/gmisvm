import cv2

class OpenCV:

	def __init__(self):
		
		self.face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	def deteksi(self, path):

		img 	= cv2.imread(path)
		gray 	= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces 	= self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)

		return faces, img

	def gmi_OpenCV(self, piksel_biner):
		momen 		= cv2.moments(piksel_biner)
		ciricv 		= cv2.HuMoments(momen).flatten()

		return ciricv
