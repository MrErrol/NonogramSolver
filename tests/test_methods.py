# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from methods import push_block_Origins, deduce_new_block_origins, deduce_new_block_endings

hints1 = [1, 1, 1]
hints2 = [1, 2, 1, 3]
blockOrigins1 = [0, 0, 0]
blockOrigins2 = [0, 0, 0, 0]
blockOrigins3 = [0, 0, 5]
blockOrigins4 = [0, 0, 7, 5]
blockOrigins5 = [0, 2, 4]

def test_push_block_Origins():
    assert push_block_Origins(hints1, blockOrigins1) == (True, [0, 2, 4])
    assert push_block_Origins(hints2, blockOrigins2) == (True, [0, 2, 5, 7])
    assert push_block_Origins(hints1, blockOrigins3) == (True, [0, 2, 5])
    assert push_block_Origins(hints2, blockOrigins4) == (True, [0, 2, 7, 5])
    assert push_block_Origins(hints1, blockOrigins1, index=1) == (True, [0, 0, 2])
    assert push_block_Origins(hints1, blockOrigins1, index=2) == (False, [0, 0, 0])
    assert push_block_Origins(hints2, blockOrigins4, index=2) == (True, [0, 0, 7, 9])

line1 = [0]*5 + [-1]
line2 = [0, 1, 0, 0, 0, 0, -1]
line3 = [-1, 0, 0, 0, 0, 0, -1]
line4 = [-1, 0, 1, 0, -1, 0, 0, 1, -1]
line5 = [0, 0, 0, 0, 0, 0, 1, 0, -1]
line6 = [0, 0, 0, 0, 0, 0, 0, -1, -1]
line7 = [0, 1, 0, 0, -1, 0, 1, 0, -1]
line8 = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1]
line9 = [-1, 0, 0, 1, 0, 0, 1, 0, 1, -1]
line10 = [-1, 0, 0, 1, 0, 0, 1, 0, 1, 0, -1]
    
# function behaviour depends on the function push_block_Origins (see tests above)
def test_deduce_new_block_origins():
    assert deduce_new_block_origins(line1, hints1, blockOrigins1) == (False, [0, 0, 0]), "for not initialized blockOrigins gives no gain"
    assert deduce_new_block_origins(line1, hints1, blockOrigins5) == (False, [0, 2, 4])
    assert deduce_new_block_origins(line2, hints1, blockOrigins1) == (True,  [1, 3, 5])
    assert deduce_new_block_origins(line3, hints1, blockOrigins1) == (True,  [1, 3, 5])
    assert deduce_new_block_origins(line4, hints1, blockOrigins1) == (True,  [2, 5, 7])
    assert deduce_new_block_origins(line8, hints2, blockOrigins2) == (True,  [1, 3, 6, 8])
    assert deduce_new_block_origins(line9, hints1, blockOrigins1) == (True,  [3, 6, 8])
    assert deduce_new_block_origins(line10, hints1, blockOrigins1) == (True,  [3, 6, 8])

blockEndings1 = [4, 4, 4]
blockEndings2 = [0, 2, 4]
blockEndings3 = [7, 7, 7]
blockEndings4 = [11, 11, 11, 11]
    
# function behaviour depends on the function deduce_new_block_origins (see tests above)
# It is just extended wrapper for the function above
def test_deduce_new_block_endings():
    assert deduce_new_block_endings(line1, hints1, blockEndings1) == (False, [4, 4, 4]), "for not initialized blockOrigins gives no gain"
    assert deduce_new_block_endings(line1, hints1, blockEndings2) == (False, [0, 2, 4])
    assert deduce_new_block_endings(line5, hints1, blockEndings3) == (True,  [2, 4, 6])
    assert deduce_new_block_endings(line6, hints1, blockEndings3) == (True,  [2, 4, 6])
    assert deduce_new_block_endings(line7, hints1, blockEndings3) == (True,  [1, 3, 6])
    assert deduce_new_block_endings(line8, hints2, blockEndings4) == (True,  [1, 4, 6, 10])