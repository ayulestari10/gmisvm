import numpy as np
import matplotlib.pyplot as plt
import MySQLdb
from sklearn import svm, tree, datasets
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.multiclass import OneVsRestClassifier

db = MySQLdb.connect("localhost", "root", "", "gmisvm")
cursor = db.cursor()
cursor.execute("SELECT * FROM ciri")
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
		"penghinaan": 4,
		"sedih": 5,
		"takut": 6
	}
	return [dct[str(label)] for label in labels]

# parameters = {'kernel': ('linear', 'rbf', 'sigmoid', 'poly'), 'C': [0.1, 1, 10, 100, 1000, 1000, 10000, 100000, 1000000, 2000000], 'gamma': [0.1, 0.001, 0.0001, 0.00001, 1, 10, 100], 'degree': [3, 4, 5, 6, 7]}
# svc = svm.SVC()
# clf = GridSearchCV(svc, parameters)
# clf.fit(features, labels)
# params = clf.best_params_
# print(clf.best_params_)
# svc = svm.SVC(gamma=params["gamma"], C=params["C"], kernel=params["kernel"], degree=params["degree"], random_state=1)
# svc.fit(features, labels)
# print(f"Score svm: {round(svc.score(features, labels) * 100, 2)}%")
from sklearn.neighbors.nearest_centroid import NearestCentroid


kf = KFold(n_splits=2, random_state=1, shuffle=True)
for i, (train_index, test_index) in enumerate(kf.split(features)):
	# t = tree.DecisionTreeClassifier()
	# t.fit(X[train_index], y[train_index])
	# print(f"Score k-{i + 1} tree: {round(t.score(X[test_index], y[test_index]) * 100, 2)}%")
	# parameters = {'kernel': ('linear', 'rbf', 'sigmoid', 'poly'), 'C': [0.1, 1, 10, 100, 1000, 1000, 10000, 100000, 1000000, 2000000], 'gamma': [0.1, 0.001, 0.0001, 0.00001, 1, 10, 100], 'degree': [3, 4, 5, 6, 7]}
	clf = NearestCentroid()
	# print(f"ini param = {parameters}")
	# clf = GridSearchCV(clf, parameters)
	# clf.fit(features[train_index], labels[train_index])
	# params = clf.best_params_
	# print(clf.best_params_)
	# clf = svm.SVC(gamma=params["gamma"], C=params["C"], kernel=params["kernel"], degree=params["degree"], random_state=1)
	clf.fit(features[train_index], labels[train_index])
	print(f"Score k-{i + 1} svm: {round(clf.score(features[test_index], labels[test_index]) * 100, 2)}%")

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