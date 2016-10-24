from tqdm import tqdm
import time
from pymongo import MongoClient

def RunModelsAll(models, records, summaryModels=[], verbose = False, db = None, collection = None, dbIdentifier = None):

    returnRecords = []

    if verbose:
        runRecords = tqdm(records)
    else:
        runRecords = records

    for record in runRecords:

        record = RunModels(models, record)

        record = RunSummaryModels(summaryModels, record)

        returnRecords.append(record)

        if db and collection and dbIdentifier:

            ## update _current on existing results
            upd = db[collection].update_many({dbIdentifier: record[dbIdentifier]}, {'$inc': {'_current': 1}})

            recordInsert = {}

            recordInsert[dbIdentifier] = record[dbIdentifier]

            recordInsert['_current'] = 0

            recordInsert['_timestamp'] = int(time.time())

            recordInsert['results'] = record['results']

            db[collection].insert_one(recordInsert)

    return returnRecords

def RunModels(models, record):

    record['results'] = {}

    for model in models:

        data = record['data'][model.name][model.version]

        x = model.execute(data = data, results = record['results'])

        record['results'] = x

    return record

def RunSummaryModels(summaryModels, record):

    for model in summaryModels:

        data = record['data'][model.name][model.version]

        for dep in model.models:
            if dep['name'] not in record['results']:
                raise SummaryModelListException("Expected model '" + dep['name'] + "' results not found")
            if dep['version'] not in record['results'][dep['name']]:
                raise SummaryModelListException("Expected model version '" + dep['name'] + "' '" + dep['version'] + "' results not found")

        record['results'] = model.execute(data = data, results = record['results'])

    return record

class Model(object):

    def __init__(self, name, fields, version, fcn, status='draft'):

        self.name = name
        self.fields = fields
        self.version = version
        self.fcn = fcn
        self.status = status

    def execute(self, data, results):

        for field in self.fields.keys():
            if field not in data.keys():
                raise Exception("Expected 'data' input '" + field + "' not found")

        results[self.name] = {}
        results[self.name][self.version] = self.fcn(data=data, results=results)
        results[self.name][self.version]['_status'] = self.status

        return results

class SummaryModel(Model):

    def __init__(self, name, models, version, fcn, fields={}, status='draft'):

        self.name=name
        self.models=models
        self.version=version
        self.fcn=fcn
        self.fields=fields
        self.status = status

class SummaryModelListException(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
