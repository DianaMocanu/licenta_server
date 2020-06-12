# import mysql.connector
from mysql import connector
# from mysql.connector import Error
import numpy as np
import re
# import pymysql
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
        self.connection = connector.connect(host='localhost',
                                            database=self.database,
                                            user=self.user,
                                            password=self.password,
                                            )

        self.cursor = self.connection.cursor()

    def executeQuery(self):

        self.cursor.execute(self.query)
        self.field_names = [i[0] for i in self.cursor.description]
        result = self.cursor.fetchall()
        return result

    def constructQueryWithoutId(self):
        lower_query = self.query.lower()
        idx = lower_query.index("from")
        whereIdx = lower_query.index('where')
        table = self.query[idx + 4: whereIdx]
        columns = ("show columns from " + table)
        self.cursor.execute(columns)
        result = []
        for (columns) in self.cursor:
            if columns[0] != 'id':
                result.append(columns[0])

        columnsString = ' ,'.join(result)
        query = 'select ' + columnsString + " from " + table + ' ' + self.query[whereIdx: ]
        return Query(self.database, query)


    def executeQueryOnlyId(self):
        lower_query = self.query.lower()
        idx = lower_query.index("from")
        fromPart = self.query[idx:]
        query = 'select id ' + fromPart
        self.cursor.execute(query)
        result = []
        for (databases) in self.cursor:
            result.append(databases[0])
        return result


    def negateQueryRandom(self, number, i, total_size):
        selectPart, wherePart = self.deconstructQuery()
        n = i / 100 * (total_size - number)
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


    def constructCondition(self, conditions):
        finalCond = " and ".join(conditions)
        return finalCond


    def deconstructQuery(self):
        lower_query = self.query.lower()
        idx = lower_query.index("where")
        selectPart = self.query[:idx + 5]
        wherePart = self.query[idx + 5:]
        return selectPart, wherePart
