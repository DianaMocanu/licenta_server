import mysql.connector


class DatabaseMethods:

    def __init__(self):
        self.user = "root"
        self.password = 'Dulciurile25'

    def getDatabases(self):

        conn = mysql.connector.connect (user=self.user, password=self.password,
                                   host='localhost',buffered=True)
        cursor = conn.cursor()
        databases = ("show databases")
        cursor.execute(databases)
        for (databases) in cursor:
             print(databases[0])

    def getTables(self, database):
        conn = mysql.connector.connect(user=self.user, password=self.password,
                                       host='localhost', database= database, buffered=True)
        cursor = conn.cursor()
        databases = ("show tables")
        cursor.execute(databases)
        result = []
        for (databases) in cursor:
            result.append(databases[0])
        return result

    def getColumns(self, database, table):
        conn = mysql.connector.connect(user=self.user, password=self.password,
                                       host='localhost', database= database, buffered=True)
        cursor = conn.cursor()
        databases = ("show columns from " + table)
        cursor.execute(databases)
        result = []
        for (databases) in cursor:
            result.append(databases[0])
        return result