# controlled_timeseries_intervention

A simple package for a basic analysis of controlled time-series intervention:

Given a **series**, a **control-series** and and **intervention time** it
automatically performs an analysis on the effect of the intervention. For that it
performs a ttest of the series pre- against post-intervention data, ttest of the
control-series pre- against post-intervention data and a ttest of the difference
of the series and control-series pre- and post-intervention data. Additionally,
an ANCOVA (analysis of covariance) is performed utilizing the control-series as
a covariate in order to increase power to detect significant results on the series.

An example on synthetically created data:

```
>>> import numpy as np
>>> import pandas as pd

>>> from scipy.stats import norm

>>> from src.series import ControlledInterventionSeries

>>> control_series = pd.Series(norm(loc=10, scale=.5).rvs(n))
>>> series = norm(loc=11, scale=.5).rvs(n)

>>> series = pd.Series((series) + np.concatenate([np.zeros(split), np.ones(n - split) * .3]))

>>> experiment = ControlledInterventionSeries(
>>>     series, control_series, split
>>> ).report()
___________________
Data Statistics

The means of series before and after intervention are
	Before: 10.929243549827472, After: 11.218828045926207

The means of control-series before and after intervention are
	Before: 10.005319046381818, After: 9.91104884687324

The mean difference of the series and control-series before and after is
	Before: 0.9239245034456536, After: 1.307779199052971.

The mean ratio of the series and control-series before and after is
	Before: 1.0945466284944954, After: 1.134990023826841.
___________________
Results from ttest:

The p-values for significance of differences in means before and after intervention are
	Series: 0.008147006816551472, Control Series: 0.35205089829866143, Difference: 0.009119634821134176, Ratio: 0.00877675059754353.

___________________
Rsults from ANCOVA:

           Source         SS  DF         F     p-unc       np2
0    intervention   2.134285   1  7.362142  0.007883  0.070544
1  control_series   0.042617   1  0.147005  0.702253  0.001513
2        Residual  28.120298  97       NaN       NaN       NaN
```

For some more insightful examples have a look at [this notebook](examples.ipynb).
