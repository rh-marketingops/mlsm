###############################################################################
## imports
###############################################################################

import mongomock
import time
from nose.tools import *
from mock import patch

import mlsm

from . import test_fcn

###############################################################################
## setup test db
###############################################################################

db = mongomock.MongoClient().db

###############################################################################
## setup basic config
###############################################################################

fieldset = {
    'field1': int,
    'field2': str,
    'field3': float
}

version = '0.0.0'

###############################################################################
## Test Definitions
###############################################################################

# create model check name
def test_createNewModelCheckName():
    testmodel = mlsm.Model(name='test', fields=fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.name == 'test'

# create model check field listing
def test_createNewModelCheckFields():
    testmodel = mlsm.Model(name='test', fields=fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fields == fieldset

# create model check function
def test_createNewModelCheckFcn():
    testmodel = mlsm.Model(name='test', fields=fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fcn == test_fcn.basic_fcn_good

# create model check version
def test_createNewModelCheckVersion():
    testmodel = mlsm.Model(name='test', fields=fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.version == version
