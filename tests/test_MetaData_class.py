
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call
import lib.nonogram as nonogram


@patch('lib.nonogram.ProgressTracker')
def test_MetaData_initialisation(mocked_progress_tracker):
    meta_data = nonogram.MetaData(2, 3)
    assert meta_data.n_rows == 2
    assert meta_data.n_cols == 3
    assert mocked_progress_tracker.mock_calls == [call(2,3)]
    assert meta_data.transposed == False


@patch('lib.nonogram.ProgressTracker')
def test_MetaData_copy(mocked_progress_tracker):
    meta_data = nonogram.MetaData(2, 3)
    mocked_progress_tracker.reset_mock()
    meta_data_copy = meta_data.copy()
    assert meta_data_copy.n_rows is meta_data_copy.n_rows
    assert meta_data_copy.n_cols is meta_data_copy.n_cols
    assert meta_data_copy.transposed == meta_data_copy.transposed
    assert mocked_progress_tracker.mock_calls == [call(2, 3), call().copy()]


@patch('lib.nonogram.ProgressTracker')
def test_MetaData_transpose(mocked_progress_tracker):
    meta_data = nonogram.MetaData(2, 3)
    mocked_progress_tracker.reset_mock()
    meta_data.transpose()
    assert meta_data.n_rows == 3
    assert meta_data.n_cols == 2
    assert mocked_progress_tracker.mock_calls == [call().transpose()]
    assert meta_data.transposed == True


def test_MetaData_is_transposed():
    meta_data = nonogram.MetaData(2, 3)
    assert meta_data.is_transposed() == False
    meta_data.transpose()
    assert meta_data.is_transposed() == True


def test_MetaData_get_number_of_rows():
    meta_data = nonogram.MetaData(2, 3)
    assert meta_data.get_number_of_rows() == 2


def test_MetaData_get_number_of_cols():
    meta_data = nonogram.MetaData(2, 3)
    assert meta_data.get_number_of_cols() == 3
