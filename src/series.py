import numpy as np
import pandas as pd
import plotly.express as px

from pingouin import ancova
from scipy.stats import ttest_ind_from_stats

class ControlledInterventionSeries:
    def __init__(self, series, control_series, intervention_index, covariates=None):
        self.series = series
        self.control_series = control_series

        # TODO: allow different covariates for series and control series?
        self.covariates = covariates

        # TODO: allow for different lengths in series and control_series?
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

    def ttest_ind_from_stats(self, apply_to, equal_var=True, alternative='two-sided'):
        nobs = self.sample_sizes()

        if apply_to == "series":
            series_before, series_after = self.get_split_series()
            mean1 = series_before.mean()
            mean2 = series_after.mean()
            std1 = series_before.std()
            std2 = series_after.std()

        elif apply_to == "control_series":
            series_before, series_after = self.get_split_control_series()
            mean1 = series_before.mean()
            mean2 = series_after.mean()
            std1 = series_before.std()
            std2 = series_after.std()

        elif apply_to == "difference":
            diff_before, diff_after = self.get_split_difference()
            mean1 = diff_before.mean()
            mean2 = diff_after.mean()
            std1 = diff_before.std()
            std2 = diff_after.std()

        else:
            raise ValueError("'apply_to' must be set se either 'series', 'control_series' or 'difference'")

        return ttest_ind_from_stats(
            mean1=mean1,
            mean2=mean2,
            std1=std1,
            std2=std2,
            nobs1=nobs[1],
            nobs2=nobs[2],
            equal_var=equal_var,
            alternative=alternative
        )

    def ancova(self, effsize='np2'):

        intervention = self.series.copy()
        intervention.iloc[:self.intervention_index] = 0
        intervention.iloc[self.intervention_index:] = 1
        data = pd.DataFrame({
            "series": self.series,
            "control_series": self.control_series,
            "intervention": intervention,
        })

        cov_names = []
        if self.covariates is not None:
            for i, covariate in enumerate(self.covariates):
                data[f"covariate_{i}"] = covariate
                cov_names += [f"covariate_{i}"]

        return ancova(
            data=data,
            dv="series",
            covar=["control_series"] + cov_names,
            between="intervention"
        )

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
        diff_before, diff_after = self.get_split_difference()
        mean_diff_before = diff_before.mean()
        mean_diff_after = diff_after.mean()
        pval_diff = self.ttest_ind_from_stats(apply_to="difference").pvalue

        series_before, series_after = self.get_split_series()
        mean_series_before = series_before.mean()
        mean_series_after = series_after.mean()
        pval_series = self.ttest_ind_from_stats(apply_to="series").pvalue

        control_series_before, control_series_after = self.get_split_control_series()
        mean_control_series_before = control_series_before.mean()
        mean_control_series_after = control_series_after.mean()
        pval_control_series = self.ttest_ind_from_stats(apply_to="control_series").pvalue

        print(f"""
___________________
Data Statistics

The means of series before and after intervention are
\tBefore: {mean_series_before}, After: {mean_series_after}

The means of control-series before and after intervention are
\tBefore: {mean_control_series_before}, After: {mean_control_series_after}

The mean difference of the series and control-series before and after is
\tBefore: {mean_diff_before}, After: {mean_diff_after}.
___________________
Results from ttest:

The p-values for significance of differences in means before and after intervention are
\tSeries: {pval_series}, Control Series: {pval_control_series}, Difference: {pval_diff}.

___________________
Rsults from ANCOVA:

{str(self.ancova())}
        """)
