# libs
import numpy as np
import pandas as pd

# utils

def eclud_dist(A, b):
    return np.sqrt(np.sum(np.square(A - b), axis=1))


def manhat_dist(A, b):
    return np.sum(np.abs(A - b), axis=1)


def max_dist(A, b):
    return np.max(np.abs(A - b), axis=1)



class KMeans:

    def __init__(self, n_means=3, distance_metric='ecludiean', max_iter=1000):
        self.n_means = n_means
        self.max_iter = max_iter
        self.centers = None
        if distance_metric.lower() == 'manhattan':
            self.distance = manhat_dist
        elif distance_metric.lower() == 'maximum':
            self.distance = max_dist
        else:
            self.distance = eclud_dist

    def fit(self, X):
        center_indices = np.random.choice(X.shape[0], self.n_means, replace=False)
        self.centers = X.loc[center_indices].values
        # print(self.centers)

        for iteration in range(self.max_iter):
            dist = []
            for center in self.centers:
                dist.append(self.distance(X, center))
            category = np.argmin(dist, axis=0)

            for center_id in range(self.n_means):
                self.centers[center_id] = X.loc[np.isin(category, [center_id])].mean(axis=0)
            # print(self.centers)

    def predict(self, Y):
        dist = []
        for center in self.centers:
            dist.append(self.distance(Y, center))
        return np.argmin(dist, axis=0)


# read data
data = pd.read_csv('./data/iris.data.csv', names=[0,1,2,3,4])

# print(data.head())

# clf = KMeans()
# clf.fit(data[[0,1,2,3]])
# print(clf.predict(data[[0,1,2,3]]))


# sample test

sample_x = pd.DataFrame([[1, 2],
              [1.5, 1.8],
              [5, 8],
              [8, 8],
              [1, 1.06],
              [9, 11],
              [1, 3],
              [8, 9],
              [0, 3],
              [5, 4],
              [6, 4], ], columns=[0,1])

for dist in ['manhattan', 'maximum', 'ecludiean']:
    clf = KMeans(distance_metric=dist)
    print('\nMetric:\t',dist)
    clf.fit(sample_x)
    print(clf.centers)
    print(clf.predict(sample_x))
# sample_x.plot.scatter(0,1)
# for center in clf.centers:
#     plt.scatter(center[0], center[1], color='r')
# plt.show()