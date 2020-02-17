#!/usr/bin/env python
'''
this is very simple examples for how to use pytest fixture
If an object should be generated whenever called by test_funcX, just refer to the examples below
'''
import pytest
from decorator import *

@pytest.fixture(scope='function')
def genObj():
    print("------ generating object ---------")
    res = MyTest()
    yield res
    print("------- deleting object ----------")
    del res
    
def test_fun1(genObj):
    obs=genObj; obs.inc()
    pred = 1
    assert pred == obs.getNum()

def test_fun2(genObj):
    '''
    this function will be passed when the scope is function of fixture, however failed when the scope is module.
    because scope='function' means that the fixture is called whenever the test_xxx is called. 
    By contrast, scope='module' means that the fixture is called only once by this module file
    '''
    obs=genObj; obs.inc()
    pred = 1
    assert pred == obs.getNum()
