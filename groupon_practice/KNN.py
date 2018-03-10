import numpy as np
import pandas as pd
from collections import Counter


# utils
def max_label(label_counts):
    max_label = ''
    max_count = 0
    for label, count in label_counts.items():
        if max_count < count:
            max_label, max_count = label, count
    return max_label


class KNN:
    def __init__(self, n_neighbours=8):
        self.n_neighbours = n_neighbours

    def predict(self, X_train, X_test, Y):
        Y_predicted = []
        for sample_y in Y.values:
            neighbours_index = np.argsort(np.sqrt(np.sum(np.square(X_train - sample_y), axis=1)))[:self.n_neighbours]
            neighbours_labels = [x[0] for x in X_test.loc[neighbours_index].values]
            neighbour_label_counts = Counter(neighbours_labels)
            Y_predicted.append(max_label(neighbour_label_counts))
        return Y_predicted


data = pd.read_csv('./data/iris.data.csv', names=[0, 1, 2, 3, 4])
# X = data.sample(n=10, axis=0, replace=False)
# Y = data.iloc[[data_ind for data_ind in data.index if data_ind not in X.index]]
X = data
Y = data
X = X.reindex(range(X.shape[0]))
X_train = X[[0,1,2,3]]
X_test = X[[4]]
Y_train = Y[[0,1,2,3]]
Y_test = Y[[4]]
# print(X)
clf = KNN()
Y_predicted = clf.predict(X_train, X_test, Y_train)
print([y[0] for y in Y_test.values], '\n', Y_predicted)