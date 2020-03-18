import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call
from lib.solver import solver
from lib.nonogram import Nonogram


# small nonogram that nonetheless require even assumption making
nono1 = Nonogram('tests/data/nono_test_1.dat')
# smallest nonogram with non-unique solution
nono2 = Nonogram('tests/data/nono_test_nonunique.dat')


@patch('builtins.print')
def test_solver(mocked_print):
    cycle = solver(nono1)

    assert type(cycle) is int
    assert nono1.get_true_rows() == [
        [ 1,  1, -1, -1, -1,  1,  1,  -1],
        [ 1,  1, -1, -1, -1,  1,  1,  -1],
        [-1, -1,  1, -1, -1, -1, -1,  -1],
        [-1, -1,  1,  1,  1, -1, -1,  -1],
    ]

    solver(nono2)

    assert mocked_print.mock_calls == [
        call('Failed to solve Nonogram.'),
        call('Cycle : 0')
    ]

