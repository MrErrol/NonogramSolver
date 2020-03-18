# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from unittest.mock import patch, Mock, call
import lib.nonogram as nonogram
from lib.solver import solver

nono  = nonogram.Nonogram("nonograms/small_1.dat")
nono1 = nonogram.Nonogram("nonograms/small_1.dat")
nono2 = nonogram.Nonogram("nonograms/small_1.dat")
nono3 = nonogram.Nonogram("nonograms/small_1.dat")
nono4 = nonogram.Nonogram("nonograms/small_1.dat")
nono5 = nonogram.Nonogram("nonograms/small_1.dat")
nono6 = nonogram.Nonogram("nonograms/small_1.dat")
nono7 = nonogram.Nonogram("nonograms/small_1.dat")
nono_pre = nonogram.Nonogram("tests/data/nono_test_3.dat", presolved=True)


@patch('builtins.print')
@patch('builtins.quit')
def test_Nonogram_read_nonogram_from_file(mocked_quit, mocked_print):
    nonogram.Nonogram("tests/data/nono_test_3_inconsistent.dat")
    assert mocked_print.mock_calls == [
        call('Input nonogram is not self consistent.'),
        call('The sum of filled cells in rows is different than in columns.'),
        ]
    assert mocked_quit.mock_calls == [call()]


def test_transpose_rows():
    rows = [[1, 2, 3, -1], [4, 5, 6, -1], [7, 8, 9, -1]]
    assert nonogram.transpose_rows(rows) == [[1, 4, 7, -1], [2, 5, 8, -1], [3, 6, 9, -1]]


def test_Nonogram_initialisation():
    assert nono.nRows == 3
    assert nono.nCols == 3
    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.rowHints == [[2], [2], [1, 1]]
    assert nono.colHints == [[1, 1], [2], [2]]
    assert nono.rowBlockOrigins == [[0], [0], [0, 0]]
    assert nono.colBlockOrigins == [[0, 0], [0], [0]]
    assert nono.rowBlockEndings == [[2], [2], [2, 2]]
    assert nono.colBlockEndings == [[2, 2], [2], [2]]
    assert nono.undetermind == 9
    assert nono.rowsChanged == {0, 1, 2}
    assert nono.colsChanged == {0, 1, 2}
    assert nono.transposed == False    


def test_Nonogram_initialisation_presolved():
    assert nono_pre.rows == [[ 1,  1, -1, -1],
                             [-1,  1,  0, -1],
                             [ 0, -1,  1, -1],
                             ]
    assert nono_pre.cols == [[ 1, -1,  0, -1],
                             [ 1,  1, -1, -1],
                             [-1,  0,  1, -1],
                             ]


def test_Nonogram_transpose():
    nono.transpose()
    assert nono.nRows == 3
    assert nono.nCols == 3
    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.rowHints == [[1, 1], [2], [2]]
    assert nono.colHints == [[2], [2], [1, 1]]
    assert nono.rowBlockOrigins == [[0, 0], [0], [0]]
    assert nono.colBlockOrigins == [[0], [0], [0, 0]]
    assert nono.rowBlockEndings == [[2, 2], [2], [2]]
    assert nono.colBlockEndings == [[2], [2], [2, 2]]
    assert nono.undetermind == 9
    assert nono.rowsChanged == {0, 1, 2}
    assert nono.colsChanged == {0, 1, 2}
    assert nono.transposed == True
    nono.transpose()


def test_Nonogram_fill_cell():
    nono.rowsChanged = set()
    nono.colsChanged = set()
    nono.fill_cell(1, 2,  1)
    nono.fill_cell(0, 1, -1)
    assert nono.rows == [[0, -1, 0, -1], [0, 0, 1, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [-1, 0, 0, -1], [0, 1, 0, -1]]
    assert nono.rowsChanged == {0, 1}
    assert nono.colsChanged == {1, 2}
    assert nono.undetermind == 7
    with pytest.raises(Exception):
        nono.fill_cell(1, 2, -1)


def test_Nonogram_self_consistency_check():
    assert nono1.self_consistency_check() == True
    nono1.rowHints[0][0] += 1
    assert nono1.self_consistency_check() == False


def test_Nonogram_get_picture_data():
    solver(nono2)
    assert nono2.get_picture_data() == [[1, 1, -1], [-1, 1, 1], [1, -1, 1]]
    nono2.transpose()
    assert nono2.get_picture_data() == [[1, 1, -1], [-1, 1, 1], [1, -1, 1]]


@patch('lib.nonogram.plot')
def test_Nonogram_plot(mocked_plot):
    mocked_plot.return_value = ('fig', 'im')
    nono3.get_picture_data = Mock(return_value='data')

    nono3.plot()

    assert mocked_plot.mock_calls == [call('data', interactive=False)]
    assert nono3.get_picture_data.mock_calls == [call()]
    assert nono3.im == 'im'
    assert nono3.fig == 'fig'


@patch('lib.nonogram.update_plot')
def test_Nonogram_update_plot(mocked_plot):
    nono4.get_picture_data = Mock(return_value='data')

    nono4.update_plot()

    assert mocked_plot.mock_calls == [
        call('data', None, None, 0.0)
    ]


@patch('lib.nonogram.end_iplot')
def test_Nonogram_end_iplot(mocked_eiplot):
    nono5.update_plot = Mock()

    nono5.end_iplot()

    assert nono5.update_plot.mock_calls == [call()]
    assert mocked_eiplot.mock_calls == [call()]


@patch('builtins.print')
def test_Nonogram_show_basic_hint(mocked_print):
    nono6.transposed = False
    nono6.show_basic_hint(0, 1)
    assert mocked_print.mock_calls == [call('Analyze row 0.')]
    mocked_print.reset_mock()

    nono6.transposed = True
    nono6.show_basic_hint(0, 1)
    assert mocked_print.mock_calls == [call('Analyze column 0.')]
    mocked_print.reset_mock()

    nono6.transposed = False
    nono6.hinter = 'advanced'
    nono6.show_basic_hint(0, 1)
    assert mocked_print.mock_calls == [
        call("Assume the cell at row=0 and col=1 to be filled " +\
         "and try to deduce consequences.")
    ]
    mocked_print.reset_mock()

    nono6.transposed = True
    nono6.hinter = 'advanced'
    nono6.show_basic_hint(0, 1)
    assert mocked_print.mock_calls == [
        call("Assume the cell at row=1 and col=0 to be filled " +\
             "and try to deduce consequences.")
    ]


@patch('builtins.quit')
@patch('builtins.print')
def test_Nonogram_show_hint(mocked_print, mocked_quit):
    nono7.show_basic_hint = Mock()
    nono7.hinter = 'assumption_making'
    nono7.verbose = 1

    nono7.show_hint(0, 1, -1)

    assert nono7.show_basic_hint.mock_calls == [call(1, 2)]
    assert mocked_print.mock_calls == [
        call("Cell at row=1 and col=2 may be deduced to be empty."),
        call('You will need to analyze more than just single row or column.'),
    ]
    assert mocked_quit.mock_calls == [call()]

    nono7.show_basic_hint.reset_mock()
    mocked_print.reset_mock()
    mocked_quit.reset_mock()

    nono7.hinter = 'simple'
    nono7.verbose = 1

    nono7.show_hint(0, 1, -1)

    assert nono7.show_basic_hint.mock_calls == [call(1, 2)]
    assert mocked_print.mock_calls == [
        call("Cell at row=1 and col=2 may be deduced to be empty."),
    ]
    assert mocked_quit.mock_calls == [call()]
