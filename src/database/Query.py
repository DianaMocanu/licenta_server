import mysql.connector
from mysql import connector
from mysql.connector import Error
import numpy as np
import re
from itertools import combinations
from itertools import combinations_with_replacement


class Query:

    def __init__(self, database, query):
        self.user = "root"
        self.password = 'Dulciurile25'
        self.database = database
        self.tags = []
        self.query = query
        self.connect()

    def connect(self):
        # try:
        self.connection = connector.connect(host='localhost',
                                            database=self.database,
                                            user=self.user,
                                            password=self.password,
                                            auth_plugin='mysql_native_password'
                                            )

        self.cursor = self.connection.cursor()

    # except Error as e:
    #     print("Error while connecting to MySQL", e)

    def executeQuery(self):
        # try:
        self.cursor.execute(self.query)
        self.field_names = [i[0] for i in self.cursor.description]
        result = self.cursor.fetchall()
        return result

    # except Error as msg:
    #     print(
    #     "Command skipped: ", msg)

    def negateQuery(self, query):

        lower_query = query.lower()
        idx = lower_query.index("where")
        if "group" in lower_query:
            end_ind = lower_query.index("group")
            negate_command = query[:idx + 5] + " not(" + query[idx + 5: end_ind] + ")" + query[end_ind:]
        else:
            if "order" in lower_query:
                end_ind = lower_query.index("order")
                negate_command = query[:idx + 5] + " not(" + query[idx + 5: end_ind - 1] + ")" + query[end_ind - 1:]
            else:
                negate_command = query[:idx + 5] + " not(" + query[idx + 5:] + ")"

        self.cursor.execute(negate_command)
        res = self.cursor.fetchall()
        return res

    def negateQueryRandom(self, number, i, total_size):
        selectPart, wherePart = self.deconstructQuery()
        # print(self.constructQueryGreedy(wherePart, number, selectPart))
        n = i / 100 * (total_size - number)
        n = number
        randPart = "ORDER BY RAND() LIMIT " + str(int(round(n)))
        newQuery = selectPart + " not( " + wherePart + " )" + randPart
        result = self.getTuples(newQuery)
        return result


    def negateQueryCombinationsN(self, number):
        selectPart, wherePart = self.deconstructQuery()
        conditions = re.split("and | or", wherePart)
        return self.condCombN(conditions, selectPart, number)


    def getTuples(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def condCombN(self, conditions, selectPart, length):
        n = len(conditions)
        minDif = np.Inf
        resultedTuples = []
        for i in range(1, np.power(2,n)):
            negatedCondition = []
            b = '{0:b}'.format(i)
            binaryNumber = b.zfill(n)
            binary = [int(x) for x in list(binaryNumber)]
            for i in range(0, n):
                digit = binary[i]
                if  digit:
                    negatedCondition.append(" not( " + conditions[i] +")")
                else:
                    negatedCondition.append(conditions[i])

            newCond = self.constructCondition(negatedCondition)
            newQuery = selectPart + " " + newCond
            tuples = self.getTuples(newQuery)
            difference = abs(length - len(tuples))
            if difference < minDif and len(tuples) > 0:
                minDif = difference
                resultedTuples = tuples

        return resultedTuples


    # def splitWhereClause(self, whereClause):
    #     # print(whereClause.split("and"))
    #     conditions = re.split("and | or", whereClause)
    #     comb = []
    #
    #     #get combinations of all conditions
    #     for i in list(range(len(conditions))):
    #         comb.append(combinations(conditions, i + 1))
    #     comb = [i for row in comb for i in row]
    #
    #     possibleNegations = []
    #
    #     for i in range(0, len(comb)):
    #         combination = comb[i]
    #         if len(combination) == 1:
    #             possibleNegations.append(["not( " + combination[0] + ")"])
    #         else:
    #
    #             for j in range(0, len(combination)):
    #                 possibleNegations.append(
    #                     ["not( " + combination[j] + ")", combination[0:j], combination[j + 1:len(combination)]])
    #
    #
    #     return possibleNegations

    def constructCondition(self, conditions):
        finalCond = "and ".join(conditions)
        return finalCond

    # def constructQueryGreedy(self, whereClause, number, selectPart):
    #     minDif = np.Inf
    #     finalQuery= ""
    #     possibleNegations = self.splitWhereClause(whereClause)
    #     for condition in possibleNegations:
    #         if len(condition) == 1:
    #             newQuery = selectPart + " " + condition[0]
    #             results = len(self.getTuples(newQuery))
    #             absDiff = results - number
    #             if minDif > absDiff:
    #                 minDif = absDiff
    #                 finalQuery= newQuery
    #         else:
    #             cond = self.constructCondition(condition)
    #             print(cond)
    #             newQuery = selectPart + "where " + cond
    #             results = len(self.getTuples(newQuery))
    #             absDiff = number - results
    #             if minDif > absDiff:
    #                 minDif = absDiff
    #                 finalQuery = cond
    #
    #     return finalQuery



    def deconstructQuery(self):
        lower_query = self.query.lower()
        idx = lower_query.index("where")
        selectPart = self.query[:idx + 5]
        wherePart = self.query[idx + 5:]
        return selectPart, wherePart

    def negateQuery2(self):
        lower_query = self.query.lower()
        idx = lower_query.index("where")

        wherePart = self.query[idx + 5:].split("and")
        newCond = " not(" + wherePart[0] + ")"
        for x in range(1, len(wherePart)):
            newCond += "and " + wherePart[x]
        print(newCond)
        negate_command = self.query[:idx + 5] + newCond

        self.cursor.execute(negate_command)
        res = self.cursor.fetchall()

        return res
