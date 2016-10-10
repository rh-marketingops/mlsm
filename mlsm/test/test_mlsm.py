###############################################################################
## imports
###############################################################################

import mongomock
import time
from nose.tools import *
from mock import patch

import mlsm

from . import test_fcn
from . import test_data

###############################################################################
## setup test db
###############################################################################

db = mongomock.MongoClient().db

###############################################################################
## setup basic config
###############################################################################

version = '0.0.0'

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
    assert results['test']['results']['c'] == 3

def test_modelRunResultModelVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2}, results={})
    assert results['test']['_version'] == '0.0.0'

@raises(Exception)
def test_modelExecRejectBadDataFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2, 'badfield': 5}, results={})

@raises(Exception)
def test_modelExecRejectMissingDataFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1}, results={})

###############################################################################
## Summary model class
###############################################################################

def test_SummaryModelName():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.name=='testSummary'

def test_SummaryModelModels():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.models==[testmodel]

def test_SummaryModelVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.version==version

def test_SummaryModelFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.fcn==test_fcn.basic_sum_fcn

def test_SummaryModelFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_sum_fcn)
    assert testsummodel.fields==test_fcn.basic_fcn_good_fieldset

def test_SummaryModelBasicAdd():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn)
    results1 = testmodel.execute(data={'a': 1, 'b': 2}, results={})
    results2 = testsummodel.execute(data={'a': 1, 'b': 2}, results=results1)
    assert results2['testSummary']['results']['d'] == 8

@raises(Exception)
def test_SummaryModelNoModelResults():
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel], fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn)
    results2 = testsummodel.execute(data={'a': 1, 'b': 2}, results={})

###############################################################################
## Run model against all records
###############################################################################

def test_modelRunAllRecords():
    testData = test_data.modelRunAllRecords
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunModel(model = testmodel, records = testData)
    for row in testResults:
        assert 'test' in row['results']

###############################################################################
## Run all models against all records
###############################################################################

def test_modelRunAllModelsAllRecords():
    testData = test_data.modelRunAllModelsAllRecords
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testResults = mlsm.RunAllModels(models = [testmodel1, testmodel2, testmodel3], records = testData)
    for row in testResults:
        assert 'test1' in row['results'] and 'test2' in row['results'] and 'test3' in row['results']

###############################################################################
## Run all models and run a summary function which references other models
###############################################################################

def test_RunAllRunSummary():
    testData = test_data.modelRunSummary
    testmodel1 = mlsm.Model(name='test1', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel2 = mlsm.Model(name='test2', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testmodel3 = mlsm.Model(name='test3', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    testsummodel = mlsm.SummaryModel(name='testSummary', models = [testmodel1, testmodel2, testmodel3], fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_sum_fcn_multiple)
    testResults = mlsm.RunAllModels(models = [testmodel1, testmodel2, testmodel3], summaryModels=[testsummodel], records = testData)
    for row in testResults:
        assert 'testSummary' in row['results']
