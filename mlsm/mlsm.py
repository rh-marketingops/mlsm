from tqdm import tqdm

def RunModelsAll(models, records, summaryModels=[], verbose = False):

    returnRecords = []

    if verbose:

        for record in tqdm(records):

            record = RunModels(models, record)

            record = RunSummaryModels(summaryModels, record)

            returnRecords.append(record)

    else:

        for record in records:

            record = RunModels(models, record)

            record = RunSummaryModels(summaryModels, record)

            returnRecords.append(record)

    return returnRecords

def RunModels(models, record):

    record['results'] = {}

    for model in models:

        x = model.execute(data = record['data'], results = record['results'])

        record['results'] = x

    return record

def RunSummaryModels(summaryModels, record):

    for model in summaryModels:

        for dep in model.models:
            if dep['name'] not in record['results']:
                raise SummaryModelListException("Expected model '" + dep['name'] + "' results not found")
            if dep['version'] not in record['results'][dep['name']]:
                raise SummaryModelListException("Expected model version '" + dep['name'] + "' '" + dep['version'] + "' results not found")

        record['results'] = model.execute(data = record['data'], results = record['results'])

    return record

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

        results[self.name] = {}
        results[self.name][self.version] = self.fcn(data=data, results=results)

        return results

class SummaryModel(Model):

    def __init__(self, name, models, version, fcn, fields={}):

        self.name=name
        self.models=models
        self.version=version
        self.fcn=fcn
        self.fields=fields

class SummaryModelListException(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
