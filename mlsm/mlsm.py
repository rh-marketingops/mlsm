

class Model(object):

    def __init__(self, name, fields, version, fcn):

        self.name = name
        self.fields = fields
        self.version = version
        self.fcn = fcn

    def execute(self, data, results):

        for field in self.fields.keys():
            if field not in data.keys():
                raise Exception("Expected 'data' input '" + field + "' not found")
        for field in data.keys():
            if field not in self.fields.keys():
                raise Exception("'data' input '" + field + "' unexpected")

        results[self.name] = self.fcn(data=data, results=results)

        return results
