import pandas as pd
from copy import Error
import time
import kagglehub
import os
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statistics
import numpy as np
from scipy.stats import norm
import time 

def confidencInterval(df, sample_size, confidenc_level):
    
    # Convert to numpy array (FAST + CONSISTENT)
    data = np.array(df)

    mean_data = np.mean(data)

    # sample standard deviation (ddof=1 = sample std, not population)
    standard_deviation = np.std(data, ddof=1)

    # Standard Error
    standard_error = standard_deviation / np.sqrt(sample_size)

    alpha = 1 - confidenc_level
    z_value = norm.ppf(1 - alpha / 2)

    margin_of_error = z_value * standard_error

    lower_bound = mean_data - margin_of_error
    upper_bound = mean_data + margin_of_error

    return {
        "Standard Error": standard_error,
        "Margin of Error": margin_of_error,
        "Z value": z_value,
        "Lower bound": lower_bound,
        "Upper bound": upper_bound
    }
def getSumAggregation(df,column_Name):
    random_sample = df[column_Name]
    
    #starting timer
    start_time = time.perf_counter()
    
    random_sample_results = random_sample.sum()
    end_time = time.perf_counter()
    
    
    executionTime= end_time - start_time
    data= {
        "result": random_sample_results,
        "execution time":  executionTime,
       
    }
    return data 

def getAvgAggregation(df,column_Name):
    random_sample = df[column_Name]
    
    #starting timer
    start_time = time.perf_counter()
    
    random_sample_results = random_sample.mean()
    end_time = time.perf_counter()
    
    
    executionTime= end_time - start_time
    data= {
        "result": random_sample_results,
        "execution time":  executionTime,
       
    }
    return data

def getMedianAggregation(df,column_Name):
    random_sample = df[column_Name]
    
    #starting timer
    start_time = time.perf_counter()
    
    random_sample_results = random_sample.median()
    end_time = time.perf_counter()
    
    
    executionTime= end_time - start_time
    data= {
        "result": random_sample_results,
        "execution time":  executionTime,
       
    }
    return data
def absoluteError(aproximateResults,exactResults):
    return abs( aproximateResults - exactResults)
    


def relativeError( absoluteError, exactResult):
    relativeError =absoluteError/ abs(exactResult)
    return relativeError


def percentageError(relativeError):
    percentageError = relativeError *100
    return percentageError



def getSumAggregation(pd,column_name,max_iterations):
    global column_series
    confidencLevel= np.random.uniform(1, 98.0)
    columnList = []
    column =  pd[column_name]
    n = len(column)
    def f(x):
            indx = int(round(x))
            
            indx = max(0,min(indx, n -1))
            return column.iloc[indx]
    learner = adaptive.Learner1D(f, bounds=(-1, 1))
    start_time = time.perf_counter()
    for _ in range(max_iterations):
       " """"add learner here to take the single data point
        from column where you call the aggregation 
        you want to perform"""""
       

       x_next = learner.ask()
       y_next = f(x_next)
        
       columnList.append(y_next)
       
       learner.tell([(x_next,y_next)])
       column_series = pd.Series(column)
       sumAgg =column_series.sum()
       
    end_time =  time.perf_counter()
    exectution_time  = end_time - start_time
    sample_size = column_series.count()
    confidence_interval =confidencInterval(stratatifiedSample[val_col],sample_size,confidencLevel)
    absolute_Error = absoluteError(aproximateSampleResults, get_aggregation_result["result"])
    relative_Error = relativeError(absolute_Error, get_aggregation_result["result"])
    precentage_Error = percentageError(relative_Error)
    
       
       