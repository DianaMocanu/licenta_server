import mysql.connector
from mysql import connector
from mysql.connector import Error
import numpy as np

class Connect:

        def __init__(self, database, query):
            self.user = "root"
            self.password = 'Dulciurile25'
            self.database = database
            self.tags = []
            self.connect()
            self.query = query

        def connect(self):
            try:
                self.connection = connector.connect(host='localhost',
                                               database=self.database,
                                               user=self.user,
                                               password=self.password,
                                               auth_plugin='mysql_native_password'
                )

                self.cursor = self.connection.cursor()
            except Error as e:
                print("Error while connecting to MySQL", e)

        def readQuery(self):
                try:
                    self.cursor.execute(self.query)
                    self.field_names = [i[0] for i in self.cursor.description]
                    result = self.cursor.fetchall()
                    res = self.addTagToArray(np.array(result), 0)
                    negQ = np.array(self.negateQuery2(self.query))
                    negate= self.addTagToArray(negQ, 1)
                    return np.concatenate((np.array(result), negQ))

                except Error as msg:
                    print(
                    "Command skipped: ", msg)

        def addTagToArray(self, elems , tag):
            newArray = []
            for elem in elems :
                elem = np.append(elem, tag)
                self.tags.append(tag)
                newArray.append(elem)
            # arr = np.array(newArray)
            return np.array(newArray)

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
            self.negateQuery2(query)
            return res

        def negateQuery2(self, query):
            lower_query = query.lower()
            idx = lower_query.index("where")
            wherePart = query[idx + 5:].split("and")
            newCond = " not(" + wherePart[0] + ")"
            for x in range(1, len(wherePart)):
                newCond += "and " +  wherePart[x]
            print(newCond)
            negate_command = query[:idx + 5] + newCond

            self.cursor.execute(negate_command)
            res = self.cursor.fetchall()

            return res

        def getNextNegated(self, query):
            lower_query = query.lower()
            idx = lower_query.index("where")
            wherePart = query[idx + 5:].split("and")
            newCond = wherePart[0] + " and not("
            for x in range(1, len(wherePart)):
                newCond +=  wherePart[x]
            negate_command = query[:idx + 5] + newCond + ")"

            self.cursor.execute(negate_command)
            res = self.cursor.fetchall()

            return res

        def constructData(self):
            result = self.readQuery()
            return result
