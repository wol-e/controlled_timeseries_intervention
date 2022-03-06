import numpy as np


class ControlledInterventionSeries:
    def __init__(self, series, control_series, intervention_index):
        self.series = series
        self.control_series = control_series
        self.intervention_index = intervention_index

    def means(self):
        means = {}
        series_before = self.series[:self.intervention_index]
        series_after = self.series[self.intervention_index:]
        means["series"] = np.array([self.series.mean(), series_before.mean(), series_after.mean()])

        control_series_before = self.control_series[:self.intervention_index]
        control_series_after = self.control_series[self.intervention_index:]
        means["control_series"] = np.array(
            [self.control_series.mean(), control_series_before.mean(), control_series_after.mean()]
        )

        return means
