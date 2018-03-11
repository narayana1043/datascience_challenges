import pandas as pd
import numpy as np

# utils


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-1.0 * x))


def d1_sigmoid(x):
    sigmoid_x = sigmoid(x)
    return sigmoid_x(1 - sigmoid_x)


class LogisticRegression:

    def __init__(self, eeta=0.1, max_iter=200):
        self.eeta = eeta
        self.max_iter = max_iter
        self.w = None

    def fit(self, X_train, Y_train):
        self.w = np.random.rand(X_train.shape[1])
        self.w = np.dot(np.dot(np.linalg.inv(np.dot(X_train.T, X_train)), X_train.T), Y_train)
        predictions = sigmoid(np.dot(X_train, self.w))
        I = np.identity(predictions.shape[0])
        for i in range(self.max_iter):
            P = np.diag(predictions)
            predictions = sigmoid(np.array(np.dot(X_train, self.w), dtype=np.float32))
            gradient = np.dot(X_train.T, Y_train - predictions)
            hessian_inv = -np.linalg.inv(np.dot(np.dot(X_train.T, np.dot(P, (I - P))), X_train))
            self.w -= self.eeta * np.dot(hessian_inv, gradient)
            predictions = self.predict(X_train)
            err = np.linalg.norm(predictions - Y_train)
            print(err)

    def predict(self, X_test):
        return sigmoid(np.dot(X_test, self.w))

redwine_df = pd.read_csv('./data/winequality-red.csv', sep=';')
whitewine_df = pd.read_csv('./data/winequality-white.csv', sep=';')
wine_df = pd.concat([redwine_df, whitewine_df])
wine_df = redwine_df
wine_df['quality'] = wine_df['quality'] > 5
wine_df['quality1'] = pd.Series(wine_df['quality']).map(lambda x: 1 if x==True else 0)
wine_df = wine_df[[col for col in wine_df.columns if col != 'quality']]
print(wine_df.head())

clf = LogisticRegression()
X_train = wine_df[[col for col in wine_df.columns if col != 'quality1']]
Y_train = wine_df['quality1']
clf.fit(X_train, Y_train)
