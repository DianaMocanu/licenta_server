import mysql.connector
from mysql import connector
from mysql.connector import Error
import numpy as np

from src.database.Query import Query


class Connect:

        def __init__(self):
            self.tags = []



        def createLearningSets(self, query):
            self.tags = []
            result = np.array(query.executeQuery())
            self.field_names = query.field_names
            res = self.addTagToArray(np.array(result), 0)
            negQ = np.array(query.negateQuery2())
            negate = self.addTagToArray(negQ, 1)
            return np.concatenate((np.array(result), negQ))

        def addTagToArray(self, elems , tag):
            newArray = []
            for elem in elems :
                elem = np.append(elem, tag)
                self.tags.append(tag)
                newArray.append(elem)
            # arr = np.array(newArray)
            return np.array(newArray)

        def getNextNegated(self, query, database):
            lower_query = query.lower()
            idx = lower_query.index("where")
            wherePart = query[idx + 5:].split("and")
            newCond = wherePart[0] + " and not("
            for x in range(1, len(wherePart)):
                newCond +=  wherePart[x]
            negate_command = query[:idx + 5] + newCond + ")"
            newQuery = Query(database, negate_command)
            res = newQuery.executeQuery()
            return res

