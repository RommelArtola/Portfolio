'''Credits to follow-along video by AssemblyAI and Misra Turp.
https://www.youtube.com/watch?v=NxEHSAfFlK8&ab_channel=AssemblyAI'''

''' TERMS:
Information Gain: 
    IG = E(parent) - [weighted average] * E(children)

    Where...
        E is Entropy (or lack of order). Root node in a decision tree has a 
            higher level of entropy in comparison to the leaf (final) node.

Entropy:
    E = -1 * sum(   p(X) * np.log2(p(X))    )

p(X):
    p(X) = number of X / number of values

Stopping Criteria (when to not split nodes anymore):
    A pre-defined maximum depth, or...
    A minimum number of samples in a node, or...
    A minimum impurity decrease (minimum entropy change required for a split)
'''

import pandas as pd
import numpy as np
from collections import Counter



class Node():
    def __init__(self, 
                 feature=None, 
                 threshold=None, 
                 left=None, 
                 right=None, 
                 *, #Used to value is not a positional argument. 
                 value=None):
        self.feature    = feature
        self.threshold  = threshold
        self.left       = left
        self.right      = right
        self.value      = value

    
    def is_leaf_node(self):
        '''Returns true if it is a leaf node'''
        return self.value is not None

class DecisionTree():



    def __init__(self, 
                 min_samples_split=2,
                 max_depth=100, 
                 n_features=None):

        self.min_samples_split  = min_samples_split
        self.max_depth          = max_depth
        self.n_features         = n_features
        self.root               = None

    

    def fit(self, X, y):
        """Fit the decision tree model according to X and Y."""
        #X.shape[1] grabs the number of columns (or features)
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1], self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        #Check stopping criteria
        if (depth >= self.max_depth or n_labels==1 or n_samples < self.min_samples_split):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        #find the best split
        feat_indices = np.random.choice(n_feats, self.n_features, replace=False)
        best_feature, best_threshold = self._best_split(X, y, feat_indices)

        #create child nodes
        left_indices, right_indices = self._split(X[:, best_feature], best_threshold)
        left = self._grow_tree(X[left_indices, :], y[left_indices], depth+1)
        right = self._grow_tree(X[right_indices, :], y[right_indices], depth+1)
        return Node(best_feature, best_threshold, left, right)
    
    def _most_common_label(self, y):
        #List the n most common elements and their counts from the most common to the least. If n is None, then list all element counts.
        counter = Counter(y)
        #Grabs the most common value in listed tuple elements form. Then the first tuple, and the first value of said tuple in said list.
        value = counter.most_common(n=1)[0][0]

        return value


    def _best_split(self, X, y, feat_indices):
        best_gain = -1
        split_index, split_threshold = None, None

        for feat_index in feat_indices:
            X_column = X[:, feat_index]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                #calculate information gain
                info_gain = self._information_gain(y, X_column, threshold)

                if info_gain > best_gain:
                    best_gain = info_gain
                    split_index = feat_index
                    split_threshold = threshold

            return split_index, split_threshold
  

    def _information_gain(self, y, X_column, threshold):
        #parent entropy
        parent_entropy = self._entropy(y)

        #create children
        left_indices, right_indices = self._split(X_column, threshold)
        if len(left_indices) == 0 or len(right_indices) == 0:
            return 0
        
        #calcualte the weighted entropy of children
        n = len(y)
        left_n, right_n = len(left_indices), len(right_indices)
        entropy_left, entropy_right = (self._entropy(y[left_indices]), 
                                       self._entropy(y[right_indices])
                                       )
        child_entropy = (left_n/n) * (entropy_left) + (right_n/n) * entropy_right

        #calculate the final info gain
        information_gain = parent_entropy - child_entropy
        return information_gain

    

    def _split(self, X_column, split_threshold):
        left_index = np.argwhere(X_column <= split_threshold).flatten()
        right_index = np.argwhere(X_column > split_threshold).flatten()
        return left_index, right_index
    
    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y) #number of occurences / number of values
        entropy_val = -1 * np.sum([p * np.log2(p) for p in ps if p>0])
        return entropy_val


    def predict(self, X):
        ret = np.array([self._traverse_tree(x, self.root) for x in X])
        return ret

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value
        
        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        
        return self._traverse_tree(x, node.right)