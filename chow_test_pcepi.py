#!/usr/bin/env python3
"""
Chow Test for PCEPI Structural Breakpoint Analysis

This script performs a Chow test to detect structural breaks in the PCEPI time series. 

This algorithm is easy to understand and implement:
1. Select a breakpoint
2. Fit a linear regression model to the data before and after the breakpoint
3. Calculate the F-statistic
4. Repeat for all possible breakpoints
5. Select the breakpoint with the highest F-statistic
6. Plot the results

The feature of this test is that: 
1. Only one breakpoint is allowed; 
2. Linear regression is used to fit the data before and after the breakpoint.

"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime


def chow_test(y, x, break_point):
    """
    Perform Chow test for structural break at given break_point
    
    Parameters:
    y: dependent variable (time series)
    x: independent variable (typically time index)
    break_point: index where to test for structural break
    
    Returns:
    F-statistic, p-value, critical value
    """
    n = len(y)
    k = 2  # number of parameters (intercept + slope)
    
    # Split data at break point
    y1, y2 = y[:break_point], y[break_point:]
    x1, x2 = x[:break_point], x[break_point:]
    
    # Fit full model
    X_full = np.column_stack([np.ones(n), x])
    #np.linalg.lstsq is used to fit the linear regression model.
    beta_full = np.linalg.lstsq(X_full, y, rcond=None)[0]
    y_pred_full = X_full @ beta_full
    #ssr_full is the sum of squared residuals of the full model.
    ssr_full = np.sum((y - y_pred_full)**2)
    
    # Fit first subsample
    X1 = np.column_stack([np.ones(len(y1)), x1])
    beta1 = np.linalg.lstsq(X1, y1, rcond=None)[0]
    y_pred1 = X1 @ beta1
    ssr1 = np.sum((y1 - y_pred1)**2)
    
    # Fit second subsample
    X2 = np.column_stack([np.ones(len(y2)), x2])
    beta2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
    y_pred2 = X2 @ beta2
    ssr2 = np.sum((y2 - y_pred2)**2)
    
    # Calculate F-statistic
    #ssr_restricted means the error we get if we assume the slope and intercept are the same before and after the breakpoint.
    #ssr_unrestricted means the error we get if we assume the slope and intercept are different before and after the breakpoint.
    #ssr_restricted should be alwasy larger than ssr_unrestricted.
    ssr_restricted = ssr_full
    ssr_unrestricted = ssr1 + ssr2
    
    #n-2k is the degree of freedom of the unrestricted model.
    #k is the degree of freedom of the restricted model.
    #Then it's easy to understand that if F is larger, then it means the unrestricted model has better fit for the data.
    f_stat = ((ssr_restricted - ssr_unrestricted) / k) / (ssr_unrestricted / (n - 2*k))
    #cdp is the cumulative distribution function of the F-distribution.
    p_value = 1 - stats.f.cdf(f_stat, k, n - 2*k)
    #ppf is the percent point function of the F-distribution.
    critical_value = stats.f.ppf(0.95, k, n - 2*k)
    
    return f_stat, p_value, critical_value, beta_full, beta1, beta2

def find_optimal_breakpoint(y, x, min_obs=10):
    """
    Find the optimal breakpoint by testing all possible break points
    """
    n = len(y)
    best_f_stat = 0
    best_break_point = None
    f_stats = []
    
    # Test breakpoints from min_obs to n-min_obs
    for bp in range(min_obs, n - min_obs):
        try:
            f_stat, p_val, crit_val, _, _, _ = chow_test(y, x, bp)
            f_stats.append((bp, f_stat, p_val))
            if f_stat > best_f_stat:
                best_f_stat = f_stat
                best_break_point = bp
        except:
            continue
    
    return best_break_point, best_f_stat, f_stats

def main():
    # Load PCEPI data
    print("Loading PCEPI data...")
    try:
        df = pd.read_excel('PCEPI.xlsx', sheet_name='Monthly')
        
        # Clean and prepare data
        df_clean = df.dropna()
        
        # Sort data by observation_date to ensure chronological order
        df_clean['observation_date'] = pd.to_datetime(df_clean['observation_date'])
        df_clean = df_clean.sort_values('observation_date')
        
        # Create simple time index starting from 1 after sorting
        df_clean['time_index'] = range(1, len(df_clean) + 1)
        
        # Prepare variables for analysis
        y = df_clean['PCEPI'].values
        x = df_clean['time_index'].values  # Time index 1, 2, 3, 4...
        
        best_bp, best_f, all_f_stats = find_optimal_breakpoint(y, x)
        
        if best_bp is None:
            print("No valid breakpoint found.")
            return
        
        # Perform Chow test at optimal breakpoint
        f_stat, p_value, critical_value, beta_full, beta1, beta2 = chow_test(y, x, best_bp)
        
        # Show breakpoint information
        break_observation = df_clean.iloc[best_bp]['time_index']
        break_date = df_clean.iloc[best_bp]['observation_date']
        print(f"\nOptimal breakpoint found at observation {break_observation}: {break_date.strftime('%Y-%m-%d')}")
        
        print(f"\nChow Test Results:")
        print(f"F-statistic: {f_stat:.4f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Critical value (5%): {critical_value:.4f}")
        print(f"Reject null hypothesis: {f_stat > critical_value}")
        
        #you can also use p_value to compare with significance level, which is 0.05 to determine if the breakpoint is significant.
        if f_stat > critical_value:
            print("\n*** STRUCTURAL BREAK DETECTED ***")
        else:
            print("\nNo significant structural break detected at this point.")
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Time series with breakpoint
        plt.subplot(2, 2, 1)
        dates = df_clean['observation_date'].values
        plt.plot(dates, y, 'b-', linewidth=1, label='PCEPI')
        plt.axvline(dates[best_bp], color='red', linestyle='--', label=f'Break point')
        plt.title('PCEPI Time Series with Structural Break')
        plt.ylabel('PCEPI')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: F-statistics across all potential breakpoints
        plt.subplot(2, 2, 2)
        bp_indices = [item[0] for item in all_f_stats]
        f_values = [item[1] for item in all_f_stats]
        plt.plot(bp_indices, f_values, 'g-', linewidth=1)
        plt.axhline(critical_value, color='red', linestyle='--', label=f'Critical value ({critical_value:.2f})')
        plt.axvline(best_bp, color='red', linestyle=':', label=f'Optimal break')
        plt.title('F-statistics Across Potential Breakpoints')
        plt.xlabel('Potential Breakpoint (Observation)')
        plt.ylabel('F-statistic')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Fitted lines before and after break
        plt.subplot(2, 1, 2)
        dates = df_clean['observation_date'].values
        plt.plot(dates, y, 'b-', linewidth=1, alpha=0.7, label='PCEPI')
            
        # Fitted line before break
        x1_fit = x[:best_bp]
        y1_fit = beta1[0] + beta1[1] * x1_fit
        plt.plot(dates[:best_bp], y1_fit, 'r-', linewidth=2, label='Pre-break trend')
            
        # Fitted line after break
        x2_fit = x[best_bp:]
        y2_fit = beta2[0] + beta2[1] * x2_fit
        plt.plot(dates[best_bp:], y2_fit, 'orange', linewidth=2, label='Post-break trend')
            
        plt.axvline(dates[best_bp], color='red', linestyle='--', alpha=0.7, label='Break point')

        plt.title('PCEPI with Pre- and Post-Break Trends')
        plt.ylabel('PCEPI')
        plt.xlabel('Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('pcepi_chow_test_results.png', dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved as 'pcepi_chow_test_results.png'")
        plt.show()
        
        # Save detailed results
        break_observation = df_clean.iloc[best_bp]['time_index']
        break_date = df_clean.iloc[best_bp]['observation_date']
        
        results_df = pd.DataFrame({
            'Breakpoint_Index': [best_bp],
            'F_Statistic': [f_stat],
            'P_Value': [p_value],
            'Critical_Value': [critical_value],
            'Significant_Break': [f_stat > critical_value],
            'Full_Intercept': [beta_full[0]],
            'Full_Slope': [beta_full[1]],
            'Pre_Break_Intercept': [beta1[0]],
            'Pre_Break_Slope': [beta1[1]],
            'Post_Break_Intercept': [beta2[0]],
            'Post_Break_Slope': [beta2[1]]
        })
        
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        print("Please ensure PCEPI.xlsx exists and contains the expected data format.")

if __name__ == "__main__":
    main() 