# Bai-Perron-Test-in-Python
I found there is no clear/step-by-step example of how to do Bai Perron test in Python. (There is packages in R and Stata)

This repository provides an exmaple of using Bai-Perron method([Bai and Perron(2003)](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)) on PCE data in Python. The [related data](https://journaldata.zbw.eu/dataset/computation-and-analysis-of-multiple-structural-change-models) of the paper can also be accessed as reference.

The benefit of structural point test is that we can train different model in different periods, which will give a better model than the regression over the whole interval.

## Chow Test

* For the structural breakpoint analysis, I start from simple one -- Chow Test. This script "[chow_test_pcepi.py](https://github.com/veray97/Bai-Perron-Test-in-Python/blob/main/chow_test_pcepi.py)" performs a Chow test to detect structural breaks in the PCEPI time series. I also do Chow test using the best breakpoint found in python. The [F statistic calculated](https://github.com/veray97/Bai-Perron-Test-in-Python/blob/main/Chow%20Test%20result%20in%20R.png) is the same as the [result get from python](https://github.com/veray97/Bai-Perron-Test-in-Python/blob/main/chow_test_results_in_python.png).

### Algorithm:
1. Select a breakpoint time index
3. Fit a linear regression model to the data before and after the breakpoint
4. Calculate the F-statistic
>(See the formula as below)
6. Repeat for all possible breakpoints
>There is restriction on smallest segement. For exmaple, the minimum number of data in one segment is 10)
7. Select the breakpoint with the highest F-statistic
8. Plot the results (Different breakpoint ~ Related F-statistic)
9. Assess structural change by comparing the maximum F-statistic to a predefined benchmark to determine whether a breakpoint is warranted.

&nbsp;

<p align="center">
  <img width="655" height="409" alt="image" src="https://github.com/user-attachments/assets/ac3ae25b-0296-4315-9c85-5b4d9b0772f3" />
</p>

<p align="center">
<a href="https://www.geeksforgeeks.org/r-language/how-to-perform-a-chow-test-in-r/" target="_blank">Formulas in Chow Test</a>
</p>


### Features of Chow Test: 
1. Only one breakpoint is allowed; 
2. Linear regression is used to fit the data before and after the breakpoint.


## CUSUM test

* Rather than finding how many breakpoints in time serie data, CUSUM test is a statistical tool for detecting subtle but meaningful changes in data over time. And it can be combined with other algorithm, for example [Binary Segmentation](https://arxiv.org/html/2410.08654v1), [Optimal Partitioning](https://arxiv.org/pdf/math/0309285), or [Wild Binary Segmentation (WBS)](https://arxiv.org/abs/1411.0858) to find more breakpoints.

### Algorithm:



### Feature of CUSUM test:
1. Sensitive to Small Mean Shifts: By accumulating tiny deviations, CUSUM can detect small changes in the process mean more quickly than Shewhart charts.
2. Provides Information on Direction and Magnitude of Change: The slope of the CUSUM plot can indicate the trend and approximate magnitude of the mean shift.
3. Suitable for Sequential Analysis: It processes one new data point at a time and updates the cumulative sum, making it ideal for real-time monitoring.









