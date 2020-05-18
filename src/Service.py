from src.database.Connect import Connect
import numpy as np

from src.database.DatabaseMethods import DatabaseMethods
from src.database.Query import Query
from src.learning.LearningService import LearningService


class Service:
    def __init__(self):
        self.connectService = Connect()
        self.databaseManager = DatabaseMethods()


    def getQueryAlternativeConditions(self, query, database):
        queryNew = Query(database, query)
        X, result = self.connectService.createLearningSets(queryNew)
        tags =np.array(self.connectService.tags)
        # rest = np.array(self.connectService.getNextNegated(query, database))
        target_names = [0,1]
        feature_names = self.connectService.field_names
        learningService = LearningService(X, tags, feature_names, target_names,np.array(result))
        results = learningService.generateConditionsQuery()
        return(results)

    def executeQuery(self, queryToExec, database):
        query = Query(database, queryToExec)
        return query.executeQuery(), query.field_names

    def getTablesDatabase(self, database):
        return self.databaseManager.getTables(database)



