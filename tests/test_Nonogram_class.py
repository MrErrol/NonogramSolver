# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, Mock, call
import lib.nonogram as nonogram


filename_1 = "nonograms/small_1.dat"


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


def test_Nonogram_initialisation_in_depth():
    nono = nonogram.Nonogram(filename_1)
    assert nono.meta_data.n_rows == 3
    assert nono.meta_data.n_cols == 3
    assert nono.data.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.data.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.data.row_hints == [[2], [2], [1, 1]]
    assert nono.data.col_hints == [[1, 1], [2], [2]]
    assert nono.limits.row_block_origins == [[0], [0], [0, 0]]
    assert nono.limits.col_block_origins == [[0, 0], [0], [0]]
    assert nono.limits.row_block_endings == [[2], [2], [2, 2]]
    assert nono.limits.col_block_endings == [[2, 2], [2], [2]]
    assert nono.meta_data.progress_tracker.undetermind == 9
    assert nono.meta_data.progress_tracker.rows_changed == {0, 1, 2}
    assert nono.meta_data.progress_tracker.cols_changed == {0, 1, 2}
    assert nono.meta_data.transposed == False


def test_Nonogram_transpose():
    nono = nonogram.Nonogram(filename_1)
    nono.data = Mock()
    nono.limits = Mock()
    nono.meta_data = Mock()
    nono.transpose()
    assert nono.data.mock_calls == [call.transpose()]
    assert nono.limits.mock_calls == [call.transpose()]
    assert nono.meta_data.mock_calls == [call.transpose()]


def test_Nonogram_copy():
    nono = nonogram.Nonogram(filename_1)
    nono.data = Mock()
    nono.limits = Mock()
    nono.meta_data = Mock()
    nono.mode_data = Mock()
    nono_copy = nono.copy()
    assert isinstance(nono_copy, nonogram.Nonogram)
    assert nono.data.mock_calls == [call.copy()]
    assert nono.limits.mock_calls == [call.copy()]
    assert nono.meta_data.mock_calls == [call.copy()]
    assert nono.mode_data.mock_calls == [call.copy()]


def test_Nonogram_get_true_rows():
    nono = nonogram.Nonogram(filename_1)
    nono.data = Mock()
    nono.get_true_rows()
    assert nono.data.mock_calls == [call.get_row()]
    nono.transpose()
    nono.data.reset_mock()
    nono.get_true_rows()
    assert nono.data.mock_calls == [call.get_col()]


@patch('lib.nonogram.strip_trailing_empty_cells')
def test_Nonogram_get_picture_data(mocked_strip):
    nono = nonogram.Nonogram(filename_1)
    nono.get_true_rows = Mock()
    nono.get_true_rows.return_value = 'true_rows'
    nono.get_picture_data()
    assert nono.get_true_rows.mock_calls == [call()]
    assert mocked_strip.mock_calls == [call('true_rows')]


def test_Nonogram_plot_simple():
    nono = nonogram.Nonogram(filename_1)
    nono.mode_data.plot = Mock()
    nono.get_picture_data = Mock()
    nono.get_picture_data.return_value = 'pic_data'
    nono.plot()
    assert nono.get_picture_data.mock_calls == [call()]
    assert nono.mode_data.plot.mock_calls == [call('pic_data', interactive=False)]


def test_Nonogram_plot_interactive():
    nono = nonogram.Nonogram(filename_1)
    nono.mode_data.plot = Mock()
    nono.get_picture_data = Mock()
    nono.get_picture_data.return_value = 'pic_data'
    nono.plot(True)
    assert nono.get_picture_data.mock_calls == [call()]
    assert nono.mode_data.plot.mock_calls == [call('pic_data', interactive=True)]


def test_Nonogram_update_plot():
    nono = nonogram.Nonogram(filename_1)
    nono.mode_data.update_plot = Mock()
    nono.get_picture_data = Mock()
    nono.get_picture_data.return_value = 'pic_data'
    nono.update_plot()
    assert nono.get_picture_data.mock_calls == [call()]
    assert nono.mode_data.update_plot.mock_calls == [call('pic_data')]


def test_Nonogram_end_iplot():
    nono = nonogram.Nonogram(filename_1)
    nono.mode_data.end_iplot = Mock()
    nono.get_picture_data = Mock()
    nono.get_picture_data.return_value = 'data'
    nono.end_iplot()
    assert nono.mode_data.end_iplot.mock_calls == [call('data')]


def test_Nonogram_fill_cell():
    nono = nonogram.Nonogram(filename_1)
    nono.data.fill_cell = Mock()
    nono.meta_data = Mock()
    nono.data.fill_cell.return_value = True
    assert nono.fill_cell(1, 2, 1) == True
    assert nono.data.fill_cell.mock_calls == [call(1, 2, 1)]
    assert nono.meta_data.mock_calls == [call.progress_tracker.filled_cell(1, 2)]

    nono.data.fill_cell.reset_mock()
    nono.meta_data.reset_mock()
    nono.data.fill_cell.return_value = False
    assert nono.fill_cell(1, 2, 1) == False
    assert nono.data.fill_cell.mock_calls == [call(1, 2, 1)]
    assert nono.meta_data.mock_calls == []


@patch('builtins.quit')
@patch('lib.nonogram.show_basic_hint')
def test_Nonogram_show_hint_nonverbose(mocked_show_basic_hint, mocked_quit):
    nono = nonogram.Nonogram(filename_1)
    nono.show_hint_simple(2, 3, -1)
    assert mocked_show_basic_hint.mock_calls == [call(3, False)]
    assert mocked_quit.mock_calls == [call()]


@patch('builtins.quit')
@patch('builtins.print')
@patch('lib.nonogram.show_basic_hint')
def test_Nonogram_show_hint_verbose(mocked_show_basic_hint, mocked_print, mocked_quit):
    nono = nonogram.Nonogram(filename_1)
    nono.mode_data.verbosity = 1
    nono.show_hint_simple(2, 3, -1)
    assert mocked_show_basic_hint.mock_calls == [call(3, False)]
    assert mocked_print.mock_calls == [
        call("Cell at row=3 and col=4 may be deduced to be empty."),
    ]
    assert mocked_quit.mock_calls == [call()]
