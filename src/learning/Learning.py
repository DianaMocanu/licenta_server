from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# from sklearn.tree.export import export_text
from sklearn import preprocessing
import numpy as np

from src.database.Connect import Connect

connect = Connect("Electronics")
# query = connect.readTableFile("../maketable.sql")
# tags = np.array(connect.tags)
# X = np.array(query)
# y = np.array(tags)
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(X, y)

import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Parameters
n_classes = 3
plot_colors = "ryb"
plot_step = 0.02


# for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
#                                 [1, 2], [1, 3], [2, 3]]):
#     # We only take the two corresponding features
#     X = iris.data[:, pair]
#     y = iris.target
#
#     # Train
#     clf = DecisionTreeClassifier().fit(X, y)
#
#     # Plot the decision boundary
#     plt.subplot(2, 3, pairidx + 1)
#
#     x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
#                          np.arange(y_min, y_max, plot_step))
#     plt.tight_layout(h_pad=0.5, w_pad=0.5, pad=2.5)
#
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     cs = plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)
#
#     plt.xlabel(iris.feature_names[pair[0]])
#     plt.ylabel(iris.feature_names[pair[1]])
#
#     # Plot the training points
#     for i, color in zip(range(n_classes), plot_colors):
#         idx = np.where(y == i)
#         plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
#                     cmap=plt.cm.RdYlBu, edgecolor='black', s=15)
#
# plt.suptitle("Decision surface of a decision tree using paired features")
# plt.legend(loc='lower right', borderpad=0, handletextpad=0)
# plt.axis("tight")
#
# plt.figure()
# clf = DecisionTreeClassifier().fit(iris.data, iris.target)
# plot_tree(clf, filled=True)
# plt.show()

iris = load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

estimator = DecisionTreeClassifier(max_leaf_nodes=6, random_state=0)
plt.figure()
estimator.fit(X_train, y_train)
plot_tree(estimator, filled=True)
plt.show()



from sklearn.tree import _tree

def tree_to_code(tree, feature_names, target_names):
    tree_ = tree.tree_
    conditions  = []
    # classes = tree.classes_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    target_name = [
        target_names[i] if i!= _tree.TREE_UNDEFINED else "undefined!" for i in tree.classes_
    ]
    # print("def tree({}):".format(", ".join(feature_names).join(target_names)))



    def recurse2(node, depth, condition):

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            newCond = condition + " and {} <= {}".format(name, threshold)
            recurse2(tree_.children_left[node], depth + 1, newCond)
            condition += " and {} > {}".format(name, threshold)
            recurse2(tree_.children_right[node], depth + 1, condition)

        else:
            value = tree_.value[node]
            # condition += " return {}".format(value)
            maxValueIdx = value.argmax(axis = 1)
            node_class = target_name[maxValueIdx[0]]
            if(maxValueIdx[0] == 1):
                condition = condition[len(" and"):]
                conditions.append(condition)
                # print("Class: " + node_class + " Condition: " + condition)

    def calculateCondition():
        recurse2(0,1,"")
        final_condition = ""
        for c in conditions:
            if(len(final_condition) > 0):
                final_condition += " or (" + c + ")"
            else:
                final_condition += "(" + c +")"
        print(final_condition)

    calculateCondition()

tree_to_code(estimator, iris.feature_names, iris.target_names)