
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import lib.nonogram as nonogram

def test_MetaData_initialisation():
    nonogram.MetaData(2, 3)
    assert True
