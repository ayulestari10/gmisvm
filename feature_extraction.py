from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

img = np.array([
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9]
])

data = np.array([img.flatten()])
print(data)

img = np.array([
	[2, 4, 6],
	[8, 4, 1],
	[3, 8, 4]
])
print(img.flatten())
data = np.append(data, [img])
print(data)

sc = StandardScaler()
img_std = sc.fit(data)

pca = PCA(2)
proj = pca.fit_transform(img_std)
print(proj)