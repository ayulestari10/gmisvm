import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
from sklearn import svm, tree, datasets
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.multiclass import OneVsRestClassifier

db = MySQLdb.connect("localhost", "root", "", "gmisvm")
cursor = db.cursor()
cursor.execute("SELECT * FROM ciri_tanpa_biner")
data = list(cursor.fetchall())
data = np.array(list(data))
features = data[:, 2:].astype(np.float64)
labels = data[:, 1]

def encode_class(labels):
	dct = {
		"bahagia": 0,
		"jijik": 1,
		"kaget": 2,
		"marah": 3,
		"natural": 4,
		"sedih": 5,
		"takut": 6
	}
	return [dct[str(label)] for label in labels]


from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neural_network import MLPClassifier
from sklearn import datasets



k_scores = []
kf = KFold(n_splits=5, random_state=1, shuffle=True)

for i, (train_index, test_index) in enumerate(kf.split(features)):

	clf = svm.SVC(gamma=0.1, C=10000, kernel="linear")
	clf.fit(features[train_index], labels[train_index])
	scores = round(clf.score(features[test_index], labels[test_index]) * 100, 2)
	k_scores.append(scores)
	print(f"Score k-{i + 1} : {scores}%")

print(f"Mean: {np.mean(np.array(k_scores))}%")






	# print(f"i = {i}")
	# t = tree.DecisionTreeClassifier()
	# print("Hay1")
	# t.fit(features[train_index], labels[train_index])
	# print("Hay2")d(t.score(features[test_index], labels[test_index]) * 100, 2)}%")
	# print(f"i = {i}")
	# print("Hay0")
	# parameters = {'kernel': ('linear', 'rbf', 'sigmoid', 'poly'), 'C': [0.1, 1, 10, 100, 1000, 1000, 10000, 100000, 1000000, 2000000], 'gamma': [0.1, 0.001, 0.0001, 0.00001, 1, 10, 100], 'degree': [3, 4, 5, 6, 7]}
	# print("Hay0.5")
	# svc = svm.SVC()
	# print("Hay0.8")
	# print(f"ini param = {parameters}")
	# clf = GridSearchCV(svc, parameters)
	# print("Hay1")
	# clf.fit(features[train_index], labels[train_index])
	# print("Hay2")
	# params = clf.best_params_
	# print("Hay3")
	# print(clf.best_params_)
	# svc = svm.SVC(gamma=params["gamma"], C=params["C"], kernel=params["kernel"], degree=params["degree"], random_state=1)
	# print("Hay4")
	# svc.fit(features[train_index], labels[train_index])
	# print("Hay5")
	# print(f"Score k-{i + 1} svm: {round(svc.score(features[test_index], labels[test_index]) * 100, 2)}%")

# t.fit(features, labels)
# print(f"Score tree: {round(t.score(features, labels) * 100, 2)}%")




# colors = {
# 	"bahagia": "red",
# 	"jijik": "green",
# 	"kaget": "blue",
# 	"marah": "yellow",
# 	"penghinaan": "pink",
# 	"sedih": "grey",
# 	"takut": "black"
# }

# encoded_labels = encode_class(labels)
# fig, ax = plt.subplots()
# ciri1 = 4
# ciri2 = 5
# x = features[:, ciri1] * 10 ** 20
# y = features[:, ciri2] * 10 ** 35
# print(x)
# for i, l in enumerate(set(labels)):
# 	print(l, colors[l])
# 	ax.scatter(x[i], y[i], c=colors[l], label=l)

# # ax.xlim(np.min(point), np.max(point))
# # plt.xlim(np.min(x), np.max(x))
# # plt.ylim(np.min(y), np.max(y))
# plt.xlabel(f"Ciri-{ciri1}")
# plt.ylabel(f"Ciri-{ciri2}")
# ax.legend()
# plt.show()

# # ax.scatter(features[:, 2] * 100000, features[:, 3] * 100000, c=encoded_labels, label=labels)
# # plt.show()



# svm
	# clf = svm.SVC(gamma=0.1, C=10000, kernel="linear")
	# clf = svm.SVC()