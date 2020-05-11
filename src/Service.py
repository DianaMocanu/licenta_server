from src.database.Connect import Connect
import numpy as np
from src.learning.LearningService import LearningService


class Service:

    def getQueryAlternativeConditions(self, query, database):
        self.conenctService = Connect(database, query)
        X = self.conenctService.constructData()
        tags =np.array(self.conenctService.tags)
        rest = np.array(self.conenctService.getNextNegated(query))
        target_names = [0,1]
        feature_names = self.conenctService.field_names
        self.learningService = LearningService(X, tags, feature_names, target_names,rest)
        results = self.learningService.generateConditionsQuery()
        return(results)

