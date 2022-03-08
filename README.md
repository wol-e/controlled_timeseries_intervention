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
	Before: 10.950434731880854, After: 11.35359950471546

The means of control-series before and after intervention are
	Before: 10.106635598758281, After: 9.96446014035405

The mean difference of the series and control-series before and after is
	Before: 0.8437991331225732, After: 1.389139364361412.
___________________
Results from ttest:

The p-values for significance of differences in means before and after intervention are
	Series: 0.0004300602547174972, Control Series: 0.15828183031723558, Difference: 0.00032872559792903585.

___________________
Rsults from ANCOVA:

           Source         SS  DF          F     p-unc       np2
0    intervention   4.091516   1  13.257660  0.000438  0.120243
1  control_series   0.037146   1   0.120363  0.729393  0.001239
2        Residual  29.935682  97        NaN       NaN       NaN
```

For some more insightful examples have a look at [this notebook](examples.ipynb).
