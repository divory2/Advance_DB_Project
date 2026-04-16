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
def absoluteError(aproximateResults,exactResults):
    return abs( aproximateResults - exactResults)
    


def relativeError( absoluteError, exactResult):
    relativeError =absoluteError/ abs(exactResult)
    return relativeError


def percentageError(relativeError):
    percentageError = relativeError *100
    return percentageError