# libs
import numpy as np
import pandas as pd

# utils

def eclud_dist(X, center, distance='ecluid'):
    if distance.lower() == 'ecluid':
        return np.sqrt(np.sum(np.square(X - center), axis=1))
    else:
        return None


class KMeans:

    def __init__(self, n_means=3, max_iter=100):
        self.n_means = n_means
        self.max_iter = max_iter
        self.centers = None

    def fit(self, X):
        center_indices = np.random.choice(X.shape[0], self.n_means, replace=False)
        self.centers = X.loc[center_indices].values
        # print(self.centers)

        for iteration in range(self.max_iter):
            dist = []
            for center in self.centers:
                dist.append(eclud_dist(X, center))
            category = np.argmin(dist, axis=0)

            for center_id in range(self.n_means):
                self.centers[center_id] = X.loc[np.isin(category, [center_id])].mean(axis=0)
            # print(self.centers)

    def predict(self, Y):
        dist = []
        for center in self.centers:
            dist.append(eclud_dist(Y, center))
        return np.argmin(dist, axis=0)


# read data
data = pd.read_csv('./data/iris.data.csv', names=[0,1,2,3,4])

# print(data.head())

clf = KMeans()
clf.fit(data[[0,1,2,3]])
print(clf.predict(data[[0,1,2,3]]))


# sample test

# sample_x = pd.DataFrame([[1, 2],
#               [1.5, 1.8],
#               [5, 8],
#               [8, 8],
#               [1, 1.06],
#               [9, 11],
#               [1, 3],
#               [8, 9],
#               [0, 3],
#               [5, 4],
#               [6, 4], ], columns=[0,1])
# clf.fit(sample_x)
# print(clf.centers)
# print(clf.predict(sample_x))
# sample_x.plot.scatter(0,1)
# for center in clf.centers:
#     plt.scatter(center[0], center[1], color='r')
# plt.show()