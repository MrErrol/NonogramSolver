# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call, Mock
import lib.nonogram as nonogram


def test_ModeData_initialisation_empty():
    mode_data = nonogram.ModeData()
    assert mode_data.fig == None
    assert mode_data.image == None
    assert mode_data.wait == None
    assert mode_data.verbosity == -1


def test_ModeData_initialisation_wait():
    mode_data = nonogram.ModeData(wait=5)
    assert mode_data.fig == None
    assert mode_data.image == None
    assert mode_data.wait == 5
    assert mode_data.verbosity == -1


def test_ModeData_initialisation_full():
    mode_data = nonogram.ModeData(wait=5, verbosity=2)
    assert mode_data.fig == None
    assert mode_data.image == None
    assert mode_data.wait == 5
    assert mode_data.verbosity == 2


def test_ModeData_copy():
    mode_data = nonogram.ModeData(wait=5, verbosity=2)
    mode_data_copy = mode_data.copy()
    assert mode_data_copy.image == None
    assert mode_data_copy.fig == None
    assert mode_data_copy.wait == None
    assert mode_data_copy.verbosity == 2


@patch('lib.nonogram.plot')
def test_ModeData_plot_simple(mocked_plot):
    mode_data = nonogram.ModeData()
    mocked_plot.return_value = ('fig', 'im')
    mode_data.plot('data')
    assert mode_data.fig == 'fig'
    assert mode_data.image == 'im'
    assert mocked_plot.mock_calls == [call('data', interactive=False)]


@patch('lib.nonogram.plot')
def test_ModeData_plot_interactive(mocked_plot):
    mode_data = nonogram.ModeData()
    mocked_plot.return_value = ('fig', 'im')
    mode_data.plot('data', True)
    assert mode_data.fig == 'fig'
    assert mode_data.image == 'im'
    assert mocked_plot.mock_calls == [call('data', interactive=True)]


@patch('lib.nonogram.update_plot')
def test_ModeData_update_plot(mocked_uplot):
    mode_data = nonogram.ModeData(wait=4.2)
    mode_data.fig = 'fig'
    mode_data.image = 'im'
    mode_data.update_plot('data')
    assert mocked_uplot.mock_calls == [call('data', 'fig', 'im', 4.2)]


@patch('lib.nonogram.end_iplot')
def test_ModeData_end_iplot(mocked_eiplot):
    mode_data = nonogram.ModeData(wait=4.2)
    mode_data.fig = 'fig'
    mode_data.image = 'im'
    mode_data.update_plot = Mock()
    mode_data.end_iplot('data')
    assert mode_data.update_plot.mock_calls == [call('data')]
    assert mocked_eiplot.mock_calls == [call()]


def test_ModeData_is_interactive_plot_active():
    mode_data = nonogram.ModeData()
    assert mode_data.is_interactive_plot_active() == False
    # To fake existence of a figure
    mode_data.fig = True
    assert mode_data.is_interactive_plot_active() == True


def test_ModeData_get_verbosity():
    mode_data = nonogram.ModeData(verbosity=2)
    assert mode_data.get_verbosity() == 2


def test_ModeData_set_verbosity():
    mode_data = nonogram.ModeData(verbosity=2)
    mode_data.set_verbosity(3)
    assert mode_data.verbosity == 3
