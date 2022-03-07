import pandas as pd
import numpy as np

from numpy.testing import assert_array_equal
from pytest import approx

import sys

sys.path.append("../")

from src.series import ControlledInterventionSeries


def test_means():
    series = ControlledInterventionSeries(
        series=pd.Series([1, 2, 1, 2, 1, 2]),
        control_series=pd.Series([3, 4, 3, 4, 3, 4]),
        intervention_index=3
    )

    means = series.means()

    assert means["series"] == approx(np.array([1.5, 4 / 3, 5 / 3]))
    assert means["control_series"] == approx(np.array([3.5, 10 / 3, 11 / 3]))

def test_sample_size():
    series = ControlledInterventionSeries(
        series=pd.Series([1, 2, 1, 2, 1, 2]),
        control_series=pd.Series([3, 4, 3, 4, 3, 4]),
        intervention_index=4
    )

    size = series.sample_sizes()

    assert_array_equal(size, np.array([6, 4, 2]))

def test_get_split_differnce():
    series = ControlledInterventionSeries(
        series=pd.Series([1, 2, 1, 2, 1, 2]),
        control_series=pd.Series([3, 4, 3, 4, 3, 7]),
        intervention_index=4
    )

    diff = series.get_split_difference()

    assert_array_equal(diff[0], np.array([-2, -2, -2, -2]))
    assert_array_equal(diff[1], np.array([-2, -5]))
