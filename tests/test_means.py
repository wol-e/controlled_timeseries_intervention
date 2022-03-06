import pandas as pd
import numpy as np

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
