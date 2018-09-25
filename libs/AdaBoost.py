from sklearn.tree import DecisionTreeClassifier

class AdaBoost:

	def __init__(self, positive_data, negative_data):
		self.positive_data = positive_data
		self.negative_data = negative_data

	def initialize_weight(self):
		self.positive_weights = 1 / (2 * len(self.positive_data))
		self.negative_weights = 1 / (2 * len(self.negative_data))

	