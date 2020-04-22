# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from unittest.mock import patch, call
import lib.nonogram as nonogram


filename_1 = "tests/data/nono_test_1.dat"
filename_3 = "tests/data/nono_test_3.dat"
