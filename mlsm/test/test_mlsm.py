###############################################################################
## imports
###############################################################################

import mongomock
import time
from nose.tools import *
from mock import patch

import mlsm

###############################################################################
## setup test db
###############################################################################

db = mongomock.MongoClient().db

###############################################################################
## Test Definitions
###############################################################################

# create model check name
def test_createNewModelCheckName():
    fieldset = {
        'field1': int,
        'field2': str,
        'field3': float
    }
    testmodel = mlsm.Model(name='test', fields=fieldset)
    assert testmodel.name == 'test'

# create model check field listing
def test_createNewModelCheckFields():
    fieldset = {
        'field1': int,
        'field2': str,
        'field3': float
    }
    testmodel = mlsm.Model(name='test', fields=fieldset)
    assert testmodel.fields == fieldset
