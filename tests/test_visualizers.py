# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call
from utils.visualizers import end_iplot, update_plot, call_imshow, plot

@patch('utils.visualizers.plt.ioff')
@patch('utils.visualizers.plt.show')
def test_end_iplot(mocked_show, mocked_ioff):
    end_iplot()

    assert mocked_ioff.mock_calls == [call()]
    assert mocked_show.mock_calls == [call()]
