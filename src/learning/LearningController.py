import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.tree import _tree
import numpy as np
from sklearn.impute import SimpleImputer


class LearningController:

    def __init__(self,  X, Y, feature_names, target_names, rest):

        self.data = X
        self.target = Y
        # self.n_classes= 3
        self.plot_colors = "ryb"
        self.plot_step = 0.02
        self.feature_names = feature_names
        self.target_name = target_names
        self.restTuples = rest

    def initialize(self):
        estimator = DecisionTreeClassifier(max_leaf_nodes=20, random_state=0)
        plt.figure()
        # imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        # x_data = imp.fit_transform(self.data)
        estimator.fit(self.data, self.target)
        plot_tree(estimator, filled=True)
        plt.show()
        # print(estimator.predict(self.restTuples))
        # plt.show()
        self.conditions = []
        self.tree = estimator.tree_
        self.feature_name = [
            self.feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in self.tree.feature
        ]

    def recurse2(self, node, depth, condition):

        if self.tree.feature[node] != _tree.TREE_UNDEFINED:
            name = self.feature_name[node]
            threshold = self.tree.threshold[node]
            newCond = condition + " and {} <= {}".format(name, threshold)
            self.recurse2(self.tree.children_left[node], depth + 1, newCond)
            condition += " and {} > {}".format(name, threshold)
            self.recurse2(self.tree.children_right[node], depth + 1, condition)

        else:
            value = self.tree.value[node]
            maxValueIdx = value.argmax(axis=1)
            node_class = self.target_name[maxValueIdx[0]]
            if (maxValueIdx[0] == 0):
                condition = condition[len(" and"):]
                self.conditions.append(condition)

    def calculateCondition(self, conditions):
        final_condition = ""
        for c in conditions:
            if (len(final_condition) > 0):
                final_condition += " or (" + c + ")"
            else:
                final_condition += "(" + c + ")"
        return final_condition

    def generateConditionsQuery(self):
        self.initialize()
        self.recurse2(0,1,"")
        # disjCond = self.calculateCondition(self.conditions)
        # self.conditions.append(disjCond)
        return self.conditions