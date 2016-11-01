from tqdm import tqdm
import time
from pymongo import MongoClient

def RunModelsAll(models, records, summaryModels=[], verbose = False, db = None, collection = None, dbIdentifier = None):
    """
    Return a set of records (dict) with results of models; optionally store results in MongoDB

    :param list models: list of 'Model'; the models which will be run
    :param list records: list of dict; records to which models will be applied
    :param list summaryModels: list of 'SummaryModel'; the models which will be run after initial models
    :param bool verbose: use tqdm to display progress
    :param MongoClient db: MongoDB connection
    :param str collection: Collection in which to store results
    :param str dbIdentifier: field name of unique identifier to be used when storing results in MongoDB
    """

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
    """
    Return a single record (dict) with results from all models

    :param list models: list of 'Model'; the models which will be run
    :param dict record: record to which models will be applied
    """

    record['results'] = {}

    for model in models:

        data = record['data'][model.name][model.version]

        x = model.execute(data = data, results = record['results'])

        record['results'] = x

    return record

def RunSummaryModels(summaryModels, record):
    """
    Return single record (dict) with result from all SummaryModel

    :param list summaryModels: list of 'SummaryModel'; the models which will be run after initial models
    :param dict record: record to which models will be applied
    """

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
    """
    Definition of a model; used as a wrapper for python functions for operational ease
    """

<<<<<<< HEAD
    def __init__(self, name, fields, version, fcn, status='draft'):
=======
    def __init__(self, name, fields, version, fcn):
        """
        Initializes model object

        :param str name: name of model
        :param dict fields: field names with expected type; will be used for validation of input; will be used for unit testing models in future versions
        :param str version: version identifier if experimenting with multiple iterations of the same model
        :param fcn fcn: function to execute
        """
>>>>>>> feature/initialDocs

        self.name = name
        self.fields = fields
        self.version = version
        self.fcn = fcn
        self.status = status

    def execute(self, data, results):
        """
        Validates input data against expected fields, passes to function, and appends output to results keyed by model name/version

        :param dict data: input data
        :param dict results: result set to which output is appended
        """

        for field in self.fields.keys():
            if field not in data.keys():
                raise Exception("Expected 'data' input '" + field + "' not found")

        results[self.name] = {}
        results[self.name][self.version] = self.fcn(data=data, results=results)
        results[self.name][self.version]['_status'] = self.status

        return results

class SummaryModel(Model):
    """
    Extension of Model; also validates input 'results' parameter to 'execute' to ensure results from previous models can be used
    """

<<<<<<< HEAD
    def __init__(self, name, models, version, fcn, fields={}, status='draft'):
=======
    def __init__(self, name, models, version, fcn, fields={}):
        """
        Initializes SummaryModel object

        :param str name: name of model
        :param list models: list of model names and versions; used to validate input
        :param str version: version identifier if experimenting with multiple iterations of the same model
        :param fcn fcn: function to execute
        :param dict fields: field names with expected type; will be used for validation of input; will be used for unit testing models in future versions
        """
>>>>>>> feature/initialDocs

        self.name=name
        self.models=models
        self.version=version
        self.fcn=fcn
        self.fields=fields
        self.status = status

class SummaryModelListException(Exception):
    """
    Raised when input 'results' set does not match input 'models' list
    """

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)
