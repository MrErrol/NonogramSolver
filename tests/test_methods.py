# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from methods import push_block_Origins

hints1 = [1, 1, 1]
hints2 = [1, 2, 1, 3]
blockOrigins1 = [0, 0, 0]
blockOrigins2 = [0, 0, 0, 0]
blockOrigins3 = [0, 0, 5]
blockOrigins4 = [0, 0, 7, 5]

def test_push_block_Origins():
    assert push_block_Origins(hints1, blockOrigins1) == (True, [0, 2, 4])
    assert push_block_Origins(hints2, blockOrigins2) == (True, [0, 2, 5, 7])
    assert push_block_Origins(hints1, blockOrigins3) == (True, [0, 2, 5])
    assert push_block_Origins(hints2, blockOrigins4) == (True, [0, 2, 7, 5])
    assert push_block_Origins(hints1, blockOrigins1, index=1) == (True, [0, 0, 2])
    assert push_block_Origins(hints1, blockOrigins1, index=2) == (False, [0, 0, 0])
    assert push_block_Origins(hints2, blockOrigins4, index=2) == (True, [0, 0, 7, 9])