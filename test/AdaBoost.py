from sklearn.tree import DecisionTreeClassifier
import numpy as np

class AdaBoost:

	def fit(self, X_train, Y_train):
		self.n_train = len(X_train)
		self.w = np.ones(self.n_train) / self.n_train