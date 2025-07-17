# Bai-Perron-Test-in-Python
I found there is no clear/step-by-step example of how to do Bai Perron test in Python. (There is packages in R and Stata)

This repository provides an exmaple of using Bai-Perron method([Bai and Perron(2003)](https://onlinelibrary.wiley.com/doi/10.1002/jae.659)) on PCE data in Python. The [related data](https://journaldata.zbw.eu/dataset/computation-and-analysis-of-multiple-structural-change-models) of the paper can also be accessed as reference.

The benefit of structural point test is that we can train different model in different periods, which will give a better model than the regression over the whole interval.

## Chow Test

* For the structural breakpoint analysis, I start from simple one -- Chow Test. This script "chow_test_pcepi.py" performs a Chow test to detect structural breaks in the PCEPI time series. 

### Algorithm:
1. Select a breakpoint time index
>Eg:Pick breakpoint as 10 from time index (t=1,2,3,4...)
3. Fit a linear regression model to the data before and after the breakpoint
>Eg:one data is with time index 1,2,...10, another data is with time index 11,12,13...len(data)
4. Calculate the F-statistic
>(See the formula as below)
6. Repeat for all possible breakpoints
>There is restriction on smallest segement. For exmaple, the minimum number of data in one segment is 10)
7. Select the breakpoint with the highest F-statistic
8. Plot the results (Different breakpoint ~ Related F-statistic)

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

