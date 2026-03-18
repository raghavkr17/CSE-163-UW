# Education Data Analysis

1. While writing test cases, one of your coworkers noticed that some calls to `mean_min_degrees` produce `NaN` values and wanted your opinion on whether or not this is a bug with the function. Here is the code she used:

```python
mean_min_degrees(data, category="Pacific Islander")
```

**Using what you know about the data, explain why a `NaN` value appears in the result of your coworker's code cell.**

NaN shows up when using `mean_min_degrees(data, category="Pacific Islander")` because some years don’t have data for Pacific Islanders. It’s not a bug—just missing data in the dataset.

2. Between the scatter plot and the bar plot for the high school completion visualization, **which visualization do you prefer, and why?** Be sure to include at least one reference to the reading to support your answer.

I like the bar plot better than the scatter plot for high school completion. It’s easier to compare F, M, and A percentages for one year. Scatter plots are better for relationships, but here we just need a clear comparison.

3. **Describe a possible bias present in this dataset and why it might have occurred.** You may refer to the original data source, or look up any outside information to support your answer. If you are using additional sources, make sure to list them as part of your answer. We do not require formal citations, but your sources should be specific so that a staff member can find them! (i.e., don't say something broad like "Wikipedia")

One bias in this dataset is underrepresentation of certain racial groups in early years. Surveys back then didn’t always capture minority populations, which can make the numbers look higher or lower than reality.
