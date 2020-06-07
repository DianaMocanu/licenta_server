from src.database.DataController import DataController
import numpy as np

from src.database.DatabaseMethods import DatabaseMethods
from src.database.Query import Query
from src.learning.LearningController import LearningController


class Controller:
    def __init__(self):
        self.connectService = DataController()
        self.databaseManager = DatabaseMethods()
        self.size_iris = 245


    def getQueryAlternativeConditions(self, query, database, negation):
        queryNew = Query(database, query)
        X, result = self.connectService.createLearningSets(queryNew, negation)
        tags =np.array(self.connectService.tags)
        # rest = np.array(self.connectService.getNextNegated(query, database))
        target_names = [0,1]
        feature_names = self.connectService.field_names
        learningService = LearningController(X, tags, feature_names, target_names, np.array(result))
        results = learningService.generateConditionsQuery()
        return(results, len(result))

    def executeQuery(self, queryToExec, database):
        query = Query(database, queryToExec)
        return query.executeQuery(), query.field_names

    def getTablesDatabase(self, database):
        return self.databaseManager.getTables(database)

    def getColumns(self, database, table):
        return self.databaseManager.getColumns(database, table)



