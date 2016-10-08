

class Model(object):

    def __init__(self, name, fields, version, fcn, resultSet={}):

        self.name = name
        self.fields = fields
        self.version = version
        self.fcn = fcn
        self.resultSet = resultSet

    def execute(self, data, results):

        for field in self.fields.keys():
            if field not in data.keys():
                raise Exception("Expected 'data' input '" + field + "' not found")
        for field in data.keys():
            if field not in self.fields.keys():
                raise Exception("'data' input '" + field + "' unexpected")

        for rset in self.resultSet.keys():
            if rset not in results.keys():
                raise Exception("Expected 'results' input '" + rset + "' not found")

            for field in self.resultSet[rset].keys():
                if field not in results[rset].keys():
                    raise Exception("Expected 'results' input '" + rset + "' '" + field + "' not found")

        results[self.name] = self.fcn(data=data, results=results)

        return results
