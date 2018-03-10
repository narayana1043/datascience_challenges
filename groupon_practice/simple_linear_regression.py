import numpy as np
import pandas as pd


class LinearRegression:

    def __init__(self):
        self.w = None

    def fit(self, X_train, X_test):
        self.w = np.dot(np.dot(np.linalg.inv(np.dot(X_train.T, X_train)),X_train.T),X_test)

    def predict(self, Y_train):
        return np.dot(Y_train, self.w)

    def predict_mean(self, Y_train):
        return np.ones(np.dot(Y_train, self.w).shape) * np.mean(X_test, axis=0).values



data = pd.read_csv('./data/slump_test.data.csv', index_col='No')
X = data.sample(frac=0.7, replace=False)
Y = data.iloc[[i for i in data.index if i not in X.index]]
X_train = X[[col for col in data.columns if col != 'Compressive Strength (28-day)(Mpa)']]
X_test = X[['Compressive Strength (28-day)(Mpa)']]
Y_train = Y[[col for col in data.columns if col != 'Compressive Strength (28-day)(Mpa)']]
Y_test = Y[['Compressive Strength (28-day)(Mpa)']]


# print(X_train.head())
clf = LinearRegression()
clf.fit(X_train, X_test)
rmse = np.sqrt(np.sum(np.square(Y_test.values.reshape(Y_test.shape[0],) -
                                clf.predict(Y_train).reshape(Y_test.shape[0],))))
mean_rmse = np.sqrt(np.sum(np.square(Y_test.values.reshape(Y_test.shape[0],) -
                                     clf.predict_mean(Y_train).reshape(Y_test.shape[0],))))
print(rmse, mean_rmse)
