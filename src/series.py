import numpy as np


class ControlledInterventionSeries:
    def __init__(self, series, control_series, intervention_index):
        self.series = series
        self.control_series = control_series

        # TODO: allow for different indices in test and control?
        if not self.series.index.equals(self.control_series.index):
            raise IndexError("Indices of series and control series need to be identical")

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

    def stds(self):
        stds = {}
        series_before = self.series[:self.intervention_index]
        series_after = self.series[self.intervention_index:]
        stds["series"] = np.array([self.series.std(), series_before.std(), series_after.std()])

        control_series_before = self.control_series[:self.intervention_index]
        control_series_after = self.control_series[self.intervention_index:]
        stds["control_series"] = np.array(
            [self.control_series.std(), control_series_before.std(), control_series_after.std()]
        )

        return stds

    def sample_sizes(self):
        sample_sizes = {}
        series_before = self.series[:self.intervention_index]
        series_after = self.series[self.intervention_index:]
        stds["series"] = np.array([self.series.std(), series_before.std(), series_after.std()])

        control_series_before = self.control_series[:self.intervention_index]
        control_series_after = self.control_series[self.intervention_index:]
        stds["control_series"] = np.array(
            [self.control_series.std(), control_series_before.std(), control_series_after.std()]
        )

        return stds