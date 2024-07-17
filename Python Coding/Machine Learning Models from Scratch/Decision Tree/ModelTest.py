from DecisionTree import DecisionTree
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split


data = datasets.load_breast_cancer()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=.2, 
                                                    random_state=1234
                                                    )

clf = DecisionTree(max_depth=100)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

def accuracy(y_test, y_pred):
    ret = np.sum(y_test == y_pred) / len(y_test)
    return ret

acc = accuracy(y_test, predictions)
acc