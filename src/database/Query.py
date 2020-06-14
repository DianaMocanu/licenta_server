import time

from mysql import connector
import numpy as np
import re

from sklearn.externals._arff import xrange

from src.QueryValidator import QueryValidator


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
        lowerQuery = self.query.lower()
        idx = lowerQuery.index("from")
        whereIdx = lowerQuery.index('where')
        table = self.query[idx + 4: whereIdx]
        columns = f'show columns from {table}'
        self.cursor.execute(columns)
        result = [columns[0] for (columns) in self.cursor if columns[0] != 'id']
        columnsString = ' ,'.join(result)
        query = f'select {columnsString} from {table} {self.query[whereIdx:]}'
        return Query(self.database, query)


    def executeQueryOnlyId(self):
        lowerQuery  = self.query.lower()
        idx = lowerQuery .index("from")
        fromPart = self.query[idx:]
        query = f'select id {fromPart}'
        self.cursor.execute(query)
        result = []
        for (databases) in self.cursor:
            result.append(databases[0])
        return result


    def negateQueryRandom(self, number, i, total_size):
        selectPart, wherePart = self.deconstructQuery()
        n = i / 100 * (total_size - number)
        randPart = f'ORDER BY RAND() LIMIT  {str(int(round(n)))}'
        newQuery = f'{selectPart} not( {wherePart} ) {randPart}'
        result = self.getTuples(newQuery)
        return result


    def negateQueryCombinationsN(self, number):
        selectPart, wherePart = self.deconstructQuery()
        # ands =  [i.start() for i in re.finditer('', wherePart)]
        # ors = [i.start() for i in re.finditer('or', wherePart)]
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
            # negatedCondition = []
            b = '{0:b}'.format(i)
            binaryNumber = b.zfill(n)
            binary = [int(x) for x in list(binaryNumber)]
            negatedCondition = [f' not( {conditions[i]} )' if binary[i] else conditions[i] for i in xrange(0,n)]
            # for i in range(0, n):
            #     digit = binary[i]
            #     if  digit:
            #         negatedCondition.append(f' not( {conditions[i]} )')
            #     else:
            #         negatedCondition.append(conditions[i])

            newCond = ' and'.join(negatedCondition)
            newQuery = f'{selectPart} {newCond}'
            tuples = self.getTuples(newQuery)
            tuplesLength = len(tuples)
            difference = abs(length - tuplesLength)
            if tuplesLength and difference < minDif:
                minDif = difference
                resultedTuples = tuples

        return resultedTuples


    def constructCondition(self, conditions):
        finalCond = " and ".join(conditions)
        return finalCond


    def deconstructQuery(self):
        lowerQuery  = self.query.lower()
        idx = lowerQuery .index("where")
        selectPart = self.query[:idx + 5]
        wherePart = self.query[idx + 5:]
        return selectPart, wherePart
