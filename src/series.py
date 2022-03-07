import numpy as np
import pandas as pd
import plotly.express as px

from scipy.stats import ttest_ind_from_stats

class ControlledInterventionSeries:
    def __init__(self, series, control_series, intervention_index):
        self.series = series
        self.control_series = control_series

        # TODO: allow for different lengths in test and control?
        if not self.series.index.equals(self.control_series.index):
            raise IndexError("Indices of series and control series need to be identical")

        self.intervention_index = intervention_index

    def means(self):
        means = {}
        series_before, series_after = self.get_split_series()
        control_series_before, control_series_after = self.get_split_control_series()

        means["series"] = np.array([self.series.mean(), series_before.mean(), series_after.mean()])
        means["control_series"] = np.array(
            [self.control_series.mean(), control_series_before.mean(), control_series_after.mean()]
        )

        return means

    def stds(self):
        # TODO: add tests?
        stds = {}

        series_before, series_after = self.get_split_series()
        control_series_before, control_series_after = self.get_split_control_series()

        stds["series"] = np.array([self.series.std(), series_before.std(), series_after.std()])

        stds["control_series"] = np.array(
            [self.control_series.std(), control_series_before.std(), control_series_after.std()]
        )

    def difference(self):
        return self.series - self.control_series

    def sample_sizes(self):
        series_before, series_after = self.get_split_series()
        return np.array([len(self.series), len(series_before), len(series_after)])

    def ttest_ind_from_stats(self, equal_var=True, alternative='two-sided'):
        nobs = self.sample_sizes()
        diff_before, diff_after = self.get_split_difference()

        return ttest_ind_from_stats(
            mean1=diff_before.mean(),
            mean2=diff_after.mean(),
            std1=diff_before.std(),
            std2=diff_after.std(),
            nobs1=nobs[1],
            nobs2=nobs[2],
            equal_var=equal_var,
            alternative=alternative
        )

    def ancova(self):
        pass

    def get_split_series(self):
        return self.series[:self.intervention_index], self.series[self.intervention_index:]

    def get_split_control_series(self):
        return self.control_series[:self.intervention_index], self.control_series[self.intervention_index:]

    def get_split_difference(self):
        diff = self.difference()
        return diff[:self.intervention_index], diff[self.intervention_index:]

    def plot(self, title="Intervention Analysis", show=False):
        df = pd.DataFrame({
            "series": self.series,
            "control_series": self.control_series
        })
        fig = px.line(df, y=["series", "control_series"], title=title)
        fig.add_vline(
            x=self.intervention_index,
            line_width=3,
            line_dash="dash",
            line_color="orange",
            annotation_text="intervention",
        )

        if not show:
            return fig

        fig.show()

    def report(self):
        pval = self.ttest_ind_from_stats().pvalue
        diff_before, diff_after = self.get_split_difference()
        mean_diff_before = diff_before.mean()
        mean_diff_after = diff_after.mean()

        print(f"""
The mean difference of the series and control series before and after the intervention is
\tBefore: {mean_diff_before}, After: {mean_diff_after}.

The estiamted cumulative increment through the intervention based on the data from before the intervention is
\t{(diff_after - mean_diff_before).sum()}

The p-value for significance of this results is
\t{self.ttest_ind_from_stats().pvalue}.
        """)
