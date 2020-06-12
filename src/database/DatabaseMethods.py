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
        tables = ("show tables")
        cursor.execute(tables)
        result = []
        for (tables) in cursor:
            result.append(tables[0])
        return result

    def getColumns(self, database, table):
        conn = mysql.connector.connect(user=self.user, password=self.password,
                                       host='localhost', database= database, buffered=True)
        cursor = conn.cursor()
        columns = ("show columns from " + table)
        cursor.execute(columns)
        result = []
        for (columns) in cursor:
            result.append(columns[0])
        return result

    def getMinMaxColumn(self, database, column, table):
        conn = mysql.connector.connect(user=self.user, password=self.password,
                                       host='localhost', database=database, buffered=True)
        cursor = conn.cursor()
        databases = ("select min( " + column + ') as minValue, max( '+ column + ') as maxVal from ' + table)
        cursor.execute(databases)
        return(cursor.fetchone())

