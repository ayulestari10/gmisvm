from sklearn.svm import SVC, LinearSVC
from sklearn.preprocessing import LabelEncoder

class Klasifikasi:

	def __init__(self, ciri, kelas):
		self.encoder = LabelEncoder()
		self.encoder.fit(kelas)
		self.clf = LinearSVC()
		self.clf.fit(ciri, self.encoder.transform(kelas))

	def classify(self, ciri):
		result = self.clf.predict(ciri)
		ekspresi = str(self.encoder.inverse_transform(result[0]))
		return ekspresi

