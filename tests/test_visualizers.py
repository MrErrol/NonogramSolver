# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call, Mock
from matplotlib import pyplot as plt
from utils.visualizers import end_iplot, update_plot, call_imshow, plot

@patch('utils.visualizers.plt.ioff')
@patch('utils.visualizers.plt.show')
def test_end_iplot(mocked_show, mocked_ioff):
    end_iplot()

    assert mocked_ioff.mock_calls == [call()]
    assert mocked_show.mock_calls == [call()]


@patch('utils.visualizers.sleep')
def test_update_plot(mocked_sleep):
    im = plt.imshow([[0]])
    im.set_data = Mock()
    fig = plt.figure()
    fig.canvas.draw = Mock()
    fig.canvas.flush_events = Mock()

    update_plot('data', fig, im, 1.2)

    assert im.set_data.mock_calls == [call('data')]
    assert fig.canvas.draw.mock_calls == [call()]
    assert fig.canvas.flush_events.mock_calls == [call()]
    assert mocked_sleep.mock_calls == [call(1.2)]


@patch('utils.visualizers.plt.imshow')
@patch('utils.visualizers.plt.axis')
def test_call_imshow(mocked_axis, mocked_imshow):
    call_imshow([[0],[1]])

    assert mocked_axis.mock_calls == [call('off')]
    assert mocked_imshow.mock_calls == [call(
      [[0],[1]], cmap='binary', origin='upper', vmin=-1, vmax=1,
      extent=(0.5, 1.5, 0.5, 2.5),
    )]
