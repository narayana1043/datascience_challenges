import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# utils
def cal_entropy(data, target_col):
    grouped_counts = data.groupby([target_col]).size()
    total_count = grouped_counts.values.sum()
    p = np.array([count/total_count for count in grouped_counts.values])
    entropy = np.dot(p, np.log(1/p))
    return entropy


class Node:
    data = None
    left = None
    majority_target = None
    is_leaf = False
    right = None
    parent = None
    entropy = None


class DecisionTree:

    def __init__(self, target_col=None, n_splits=5):
        self.target_col = target_col
        self.n_splits = n_splits

    def find_cut(self, data):
        data_dict = dict()
        for col in data.columns:
            data_dict[col] = dict()
            if col.lower() != self.target_col:
                values = data[col].values
                max_val = np.max(values)
                min_val = np.min(values)
                split_width = (max_val - min_val)/self.n_splits
                for i in range(self.n_splits+1):
                    split_val = min_val + (i * split_width)
                    left_data = data[data[col] <= split_val]
                    right_data = data[data[col] > split_val]
                    data_dict[col][split_val] = ((left_data.shape[0] * cal_entropy(left_data, self.target_col)) +
                                                 (right_data.shape[0] * cal_entropy(right_data, self.target_col)))\
                                                /data.shape[0]
        min_entropy = 2
        min_col = None
        min_split_val = None
        for col in data_dict.keys():
            for split_val in data_dict[col]:
                if data_dict[col][split_val] == 0.0:
                    return None
                elif data_dict[col][split_val] < min_entropy:
                    min_col, min_split_val, min_entropy = col, split_val, data_dict[col][split_val]

        return data[data[min_col] <= min_split_val], data[data[min_col] > min_split_val], min_entropy

    def fit(self, train, target_col=None, n_splits=None):
        if target_col:
            self.target_col = target_col
        if n_splits:
            self.n_splits = n_splits
        if not(self.target_col and self.n_splits):
            print('set target_col and n_splits')
            sys.exit()

        root = Node()
        root.data = train
        cut_returned = self.find_cut(train)
        root.left, root.right, root.entropy = cut_returned
        if cut_returned:
            root.left, root.right = Node(), Node()
            root.left.parent, root.right.parent = root, root
            root.left.data, root.right.data = cut_returned[:2]
        else:
            root.is_leaf = True

        nodes = []
        nodes.append(root.left)
        nodes.append(root.right)
        while nodes != []:
            curr_node = nodes.pop()
            curr_node.entropy = cal_entropy(curr_node.data, self.target_col)
            cut_returned = self.find_cut(curr_node.data)
            if cut_returned and cut_returned[2] < curr_node.entropy:
                curr_node.left, curr_node.right = Node(), Node()
                curr_node.left.parent, curr_node.right.parent = curr_node, curr_node
                curr_node.left.data, curr_node.right.data, = cut_returned[:2]
                nodes.append(curr_node.left)
                nodes.append(curr_node.right)
            else:
                curr_node.is_leaf = True
                curr_node.majority_target = curr_node.data[self.target_col].unique()[0]

    def predict(self):
        pass


red_wine_df = pd.read_csv('./data/winequality-red.csv', sep=';')
white_wine_df = pd.read_csv('./data/winequality-white.csv', sep=';')
wine_df = pd.concat([red_wine_df, white_wine_df])
train, test = train_test_split(wine_df, test_size=0.33, random_state=42)
clf = DecisionTree()
clf.fit(train, 'quality')

# X_train, Y_train = train.drop(['quality']), train['quality']
# X_test, Y_test = test.drop(['quality']), test['quality']