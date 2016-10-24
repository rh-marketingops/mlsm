###############################################################################
## imports
###############################################################################

import time
from nose.tools import *
import mongomock
from mock import patch

import mlsm

from . import test_fcn
from . import test_data

###############################################################################
## setup basic config
###############################################################################

version = '0.0.0'

###############################################################################
## setup mongomock
###############################################################################

db = mongomock.MongoClient().db

coll = 'results'

###############################################################################
## Model class
###############################################################################

# create model check name
def test_createNewModelCheckName():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.name == 'test'

# create model check field listing
def test_createNewModelCheckFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fields == test_fcn.basic_fcn_good_fieldset

# create model check function
def test_createNewModelCheckFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fcn == test_fcn.basic_fcn_good

# create model check version
def test_createNewModelCheckVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.version == version

# create model check basic fcn True
def test_createNewModelCheckBasicFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fcn(data={}, results={})

# basic addition model
def test_createNewModelCheckAddFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.fcn(data={'a': 1, 'b': 2}, results={})
    assert results['c'] == 3

def test_createNewModelRun():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2}, results={})
    assert results['test'][version]['c'] == 3

def test_modelRunResultModelVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2}, results={})
    assert version in results['test']

@raises(Exception)
def test_modelExecRejectMissingDataFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1}, results={})

###############################################################################
## Summary model class
###############################################################################

def test_SummaryModelName():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.name=='testSummary'

def test_SummaryModelModels():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.models[0]['name']=='test' and testsummodel.models[0]['version']==version

def test_SummaryModelVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.version==version

def test_SummaryModelFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.fcn==test_fcn.basic_sum_fcn

def test_SummaryModelFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.fields==test_fcn.basic_fcn_good_fieldset

def test_SummaryModelBasicAdd():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [{'name': 'test', 'version': version}], fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn)
    results1 = testmodel.execute(data={'a': 1, 'b': 2}, results={})
    results2 = testsummodel.execute(data={'a': 1, 'b': 2}, results=results1)
    assert results2['testSummary'][version]['d'] == 8

###############################################################################
## Run all models against one record
###############################################################################

def test_modelRunAllModelsOneRecord():
    testData = test_data.modelRunAllModelsOneRecord
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModels(models = [testmodel1, testmodel2, testmodel3], record = testData)
    assert 'test1' in testResults['results'] and 'test2' in testResults['results'] and 'test3' in testResults['results']

def test_modelRunAllModelsOneRecordResults():
    testData = test_data.modelRunAllModelsOneRecord
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModels(models = [testmodel1, testmodel2, testmodel3], record = testData)
    assert 'c' in testResults['results']['test1']['0.0.0'] and 'c' in testResults['results']['test2']['0.0.0'] and 'c' in testResults['results']['test3']['0.0.0']

###############################################################################
## Run all models against all records
###############################################################################

def test_modelRunAllModelsAllRecords():
    testData = test_data.modelRunAllModelsAllRecords
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], records = testData)
    for row in testResults:
        assert 'test1' in row['results'] and 'test2' in row['results'] and 'test3' in row['results']

def test_modelRunAllModelsAllRecordsLen():
    testData = test_data.modelRunAllModelsAllRecords
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], records = testData)
    assert len(testResults) == 3

def test_modelRunAllModelsAllRecordsVerbose():
    testData = test_data.modelRunAllModelsAllRecords
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], records = testData, verbose = True)
    assert len(testResults) == 3

###############################################################################
## Run all models and run a summary function which references other models
###############################################################################

def test_RunAllRunSummary():
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': version}, {'name': 'test2', 'version': version}, {'name': 'test3', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData)
    for row in testResults:
        assert 'testSummary' in row['results']

def test_RunAllRunSummaryLen():
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': version}, {'name': 'test2', 'version': version}, {'name': 'test3', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData)
    assert len(testResults) == 3

def test_RunAllRunSummaryStoreResultsMongo():
    db['results'].drop()
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': version}, {'name': 'test2', 'version': version}, {'name': 'test3', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData, db = db, collection = 'results', dbIdentifier='id')
    mongoResults = db['results'].find()
    x = []
    for row in mongoResults:
        testmodel1test = version in row['results']['test1']
        testmodel2test = version in row['results']['test2']
        testmodel3test = version in row['results']['test3']
        testsummodeltest = version in row['results']['testSummary']
        x.append(testmodel3test)
        x.append(testmodel2test)
        x.append(testmodel1test)
        x.append(testsummodeltest)
    assert all(x)

def test_RunAllRunSummaryStoreResultsMongoTimestamp():
    db['results'].drop()
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': version}, {'name': 'test2', 'version': version}, {'name': 'test3', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData, db = db, collection = 'results', dbIdentifier='id')
    mongoResults = db['results'].find_one()
    assert '_timestamp' in mongoResults

def test_RunAllRunSummaryStoreResultsCount():
    db['results'].drop()
    testData = test_data.modelRunSummaryOne
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': version}, {'name': 'test2', 'version': version}, {'name': 'test3', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData, db = db, collection = 'results', dbIdentifier='id')
    testResults = mlsm.RunModelsAll(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData, db = db, collection = 'results', dbIdentifier='id')
    mongoResults = db['results'].find()
    x = []
    for row in mongoResults:
        x.append(row['_current'])
    assert x[0]!=x[1]

@raises(mlsm.SummaryModelListException)
def test_RunSummaryNoResults():
    testData = test_data.modelRunSummary
    summodellist = [{'name': 'test1', 'version': version}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [], summaryModels=[testsummodel], records = testData)

@raises(mlsm.SummaryModelListException)
def test_RunSummaryWrongVersion():
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    summodellist = [{'name': 'test1', 'version': '0.0.1'}]
    testsummodel = mlsm.SummaryModel(name='testSummary', models = summodellist, fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunModelsAll(models = [testmodel1], summaryModels=[testsummodel], records = testData)
