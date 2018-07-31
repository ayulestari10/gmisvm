from PIL import Image
import numpy as np, cv2
from libs.GMI import GMI

image = cv2.imread("D:/lena.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image[image < 126] = 0
image[image >= 126] = 1
# cv2.imshow("image", image)
moments = cv2.HuMoments(cv2.moments(image)).flatten()
print(moments)


# print(image)
# gmi = GMI(np.array(image))
# gmi.hitungMomenNormalisasi()
# print(gmi.hitungCiri())


# iris = datasets.load_iris()
X = moments
y = iris.target

kf = KFold(n_splits=10, random_state=1, shuffle=True)
for i, (train_index, test_index) in enumerate(kf.split(X)):
	# t = tree.DecisionTreeClassifier()
	# t.fit(X[train_index], y[train_index])
	# print(f"Score k-{i + 1} tree: {round(t.score(X[test_index], y[test_index]) * 100, 2)}%")
	parameters = {'kernel': ('linear', 'rbf', 'sigmoid', 'poly'), 'C': [0.1, 1, 10, 100, 1000, 1000, 10000, 100000, 1000000, 2000000], 'gamma': [0.1, 0.001, 0.0001, 0.00001, 1, 10, 100], 'degree': [3, 4, 5, 6, 7]}
	svc = svm.SVC()
	clf = GridSearchCV(svc, parameters)
	clf.fit(X[train_index], y[train_index])
	params = clf.best_params_
	print(clf.best_params_)
	svc = svm.SVC(gamma=params["gamma"], C=params["C"], kernel=params["kernel"], degree=params["degree"], random_state=1)
	svc.fit(X[train_index], y[train_index])
	print(f"Score k-{i + 1} svm: {round(svc.score(X[test_index], y[test_index]) * 100, 2)}%")