# some utils test are performed in test_nonogram.py
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from utils.read_from_file import find_beggining_of_data, read_lines

file_1 = open('tests/broken_nono_1.dat', 'r')
file_2 = open('tests/broken_nono_2.dat', 'r')
file_3 = open('tests/broken_nono_3.dat', 'r')

def test_find_beggining_of_data():
    with pytest.raises(Exception):
        find_beggining_of_data(file_1)
    file_1.close()
    with pytest.raises(Exception):
        find_beggining_of_data(file_2)
    file_2.close()
    find_beggining_of_data(file_3)
    with pytest.raises(Exception):
        read_lines(file_3)
    file_3.close()
