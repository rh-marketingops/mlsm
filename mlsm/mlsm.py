
def RunAllModels(models, records, summaryModels=[]):

    for model in models:

        records = RunModel(model, records)

    for model in summaryModels:

        records = RunModel(model, records)

    return records

def RunModel(model, records):

    for row in records:

        model.execute(data = row['data'], results = row['results'])

    return records

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

        results[self.name] = {}
        results[self.name]['results'] = self.fcn(data=data, results=results)
        results[self.name]['_version'] = self.version

        return results

class SummaryModel(Model):

    def __init__(self, name, models, version, fcn, fields={}):

        self.name=name
        self.models=models
        self.version=version
        self.fcn=fcn
        self.fields=fields
