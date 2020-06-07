import numpy as np

from src.database.Query import Query


class DataController:

        def __init__(self):
            self.tags = []


        def createLearningSets(self, query, negation):
            self.tags = []
            query.negateQueryRandom(13, 15, 254)
            positive_result = np.array(query.executeQuery())
            positive_length = len(positive_result)
            self.field_names = query.field_names
            if negation == 1:
                negative_result = query.negateQueryRandom(positive_length, 15, 254)
            else:
                negative_result = query.negateQueryCombinationsN(positive_length)

            negative_length = len(negative_result)
            print("Negate size: " + str(negative_length) + " Positive size: "  + str(positive_length))
            self.addToTag(positive_length, 0)
            self.addToTag(negative_length, 1)
            return np.concatenate((np.array(positive_result), np.array(negative_result))), positive_result


        def addToTag(self, size, tag):
            tagsToAdd = [tag] * size
            self.tags += tagsToAdd

        def addTagToArray(self, elems , tag):
            newArray = []
            for elem in elems :
                elem = np.append(elem, tag)
                self.tags.append(tag)
                newArray.append(elem)
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

