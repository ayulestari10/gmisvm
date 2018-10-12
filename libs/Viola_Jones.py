import cv2

class Viola_Jones:

	def __init__(self):
		
		self.face_cascade = cv2.CascadeClassifier('C:\\xampp\\htdocs\\gmisvm\\static\\haarcascade_frontalface_default.xml')

	def deteksi(self, image):

		img 	= cv2.imread(image)
		gray 	= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces 	= self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)

		return faces, img
