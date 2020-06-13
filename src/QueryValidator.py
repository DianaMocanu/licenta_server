


class QueryValidator:


    def checkIntegralQuery(self, query):
        lowerQuery = query.lower()
        existSelect,selectAnswer = self.checkSelectExistance(lowerQuery)
        if not existSelect:
            return existSelect, selectAnswer
        existFrom, fromAnswer = self.checkFromExistance(lowerQuery)
        if not existFrom:
            return existFrom, fromAnswer
        existWhere, whereAnswer = self.checkWhereExistance(lowerQuery)
        if not existWhere:
            return existWhere, whereAnswer
        existCond, condAnswer = self.checkConditionExistance(lowerQuery)
        if not existCond:
            return existCond, condAnswer
        return True, 'success'

    def checkExecuteQuery(self, query):
        lowerQuery = query.lower()
        existSelect, selectAnswer = self.checkSelectExistance(lowerQuery)
        if not existSelect:
            return existSelect, selectAnswer
        existFrom, fromAnswer = self.checkFromExistance(lowerQuery)
        if not existFrom:
            return existFrom, fromAnswer
        return True, 'success'

    def checkFromExistance(self, query):
        try:
            fromIdx = query.index('from')
            return True, fromIdx
        except Exception as err:
            return False, 'The query must contain a FROM Clause'

    def checkWhereExistance(self, query):
        try:
            whereIdx = query.index('where')
            return True, whereIdx
        except Exception as err:
            return False, 'The query should contain a WHERE Clause'

    def checkSelectExistance(self, query):
        try:
            selectIdx = query.index('select')
            return True, selectIdx
        except Exception as err:
            return False, 'The query must contain a SELECT Clause'

    def checkConditionExistance(self, query):
        try:
            whereIdx = query.index('where')
            if(whereIdx+5 == len(query)):
                return False, 'The query should contain a condition'
            return True, whereIdx
        except Exception as err:
            return False, 'The query should contain a WHERE Clause'

    def checkDatabase(self, database):
        if(len(database) > 0):
            return True
        return False