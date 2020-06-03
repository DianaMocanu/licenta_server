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
                    negate_command = query[:idx + 5] + " not(" + query[idx + 5: end_ind-1] + ")" + query[end_ind-1:]
                else:
                     negate_command = query[:idx + 5] + " not(" + query[idx + 5:] + ")"

            self.cursor.execute(negate_command)
            res = self.cursor.fetchall()
            return res

        def negateQueryRandom(self, number, i, total_size):
            selectPart, wherePart = self.deconstructQuery()
            n = i/100 * (total_size - number)
            n = number
            print(n)
            randPart = "ORDER BY RAND() LIMIT " + str(int(round(n)))
            newQuery = selectPart + " not( " + wherePart + " )" + randPart
            self.cursor.execute(newQuery)
            result = self.cursor.fetchall()
            self.splitWhereClause(wherePart, number, selectPart)
            return result


        def getNumberTuples(self, query):
            self.cursor.execute(query)
            return self.cursor.fetchall()

        def splitWhereClause(self, whereClause, number, selectPart):
            # print(whereClause.split("and"))
            conditions = re.split("and | or", whereClause)
            min = 1000000
            comb = []

            for i in list(range(len(conditions))):
                # Finds every combination (with replacement) for each object in the list
                comb.append(combinations(conditions, i + 1))

            comb = [i for row in comb for i in row]
            for i in range(0, len(comb)):
                combination = comb[i]
                if(len(combination) == 1):
                    print("not( " + combination[0] + ")")
                else:
                    for j in range(0, len(combination)):
                        print("---------------------------------")
                        print(combination)
                        print("not( "  + combination[j] + ")", combination[0:j] + combination[j+1:len(combination)])
            print(comb)

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
                newCond += "and " +  wherePart[x]
            print(newCond)
            negate_command = self.query[:idx + 5] + newCond

            self.cursor.execute(negate_command)
            res = self.cursor.fetchall()

            return res

