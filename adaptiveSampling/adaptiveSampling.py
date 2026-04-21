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
import adaptive
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
    print(f"*****here is absoult error {aproximateResults} - {exactResults}\n")
    return abs( aproximateResults - exactResults)
    


def relativeError( absoluteError, exactResult):
    relativeError =absoluteError/ abs(exactResult)
    return relativeError


def percentageError(relativeError):
    percentageError = relativeError *100
    return percentageError



def getAproxSumAggregation(df,column_name,max_iterations,get_aggregation_result):
    global column_series
    confidencLevel= np.random.uniform(.88, .99)
    columnList = []
    column =  df[column_name]
    n = len(column)
    def f(x):
            print(f"x is of type{type(x)} ")
            print(x)
            indx = int(round(x))
            
            indx = max(0,min(indx, n -1))
            
            return column.iloc[indx]
    learner = adaptive.Learner1D(f, bounds=(0, n-1))
    start_time = time.perf_counter()
    for _ in range(max_iterations):
       " """"add learner here to take the single data point
        from column where you call the aggregation 
        you want to perform"""""
       

   
       x_next_list = learner.ask(1)[0]
       x_next =x_next_list[0]
       y_next = f(x_next)
        
       columnList.append(y_next)
       print(type(x_next), x_next)
       learner.tell(x_next,y_next)
    column_series = pd.Series(columnList)
    sumAgg =column_series.sum()
    print(f"Here is sum Agg for aproximate agregation: *** \n {sumAgg}")
       
    end_time =  time.perf_counter()
    exectution_time  = end_time - start_time
    sample_size = column_series.count()
    confidence_interval =confidencInterval(column_series,sample_size,confidencLevel)
    absolute_Error = absoluteError(sumAgg, get_aggregation_result["result"])
    relative_Error = relativeError(absolute_Error, get_aggregation_result["result"])
    precentage_Error = percentageError(relative_Error)
    metric_Evaluation= {
    "absolute error": absolute_Error,
    "relative error": relative_Error,
    "precentage error": precentage_Error,
    "z value": confidence_interval["Z value"],
    "margin of error": confidence_interval["Margin of Error"],
    "standard error": confidence_interval["Standard Error"],
    "lower bound": confidence_interval["Lower bound"],
    "upper bound": confidence_interval["Upper bound"],
    "execution time": exectution_time,
    "approx result": sumAgg,
    "sample size":  sample_size
       
        
        
    }
    return metric_Evaluation

def getAproxAvgAggregation(df,column_name,max_iterations,get_aggregation_result):
    global column_series
    confidencLevel= np.random.uniform(.88, .99)
    columnList = []
    column =  df[column_name]
    n = len(column)
    def f(x):
            indx = int(round(x))
            
            indx = max(0,min(indx, n -1))
            return column.iloc[indx]
    learner = adaptive.Learner1D(f, bounds=(0, n-1))
    start_time = time.perf_counter()
    for _ in range(max_iterations):
       " """"add learner here to take the single data point
        from column where you call the aggregation 
        you want to perform"""""
       

       x_next_list = learner.ask(1)[0]
       x_next = x_next_list[0]
       y_next = f(x_next)
        
       columnList.append(y_next)
       
       learner.tell(x_next,y_next)
    column_series = pd.Series(columnList)
    sumAgg =column_series.mean()
       
    end_time =  time.perf_counter()
    exectution_time  = end_time - start_time
    sample_size = column_series.count()
    confidence_interval =confidencInterval(column_series,sample_size,confidencLevel)
    absolute_Error = absoluteError(sumAgg, get_aggregation_result["result"])
    relative_Error = relativeError(absolute_Error, get_aggregation_result["result"])
    precentage_Error = percentageError(relative_Error)
    metric_Evaluation= {
    "absolute error": absolute_Error,
    "relative error": relative_Error,
    "precentage error": precentage_Error,
    "z value": confidence_interval["Z value"],
    "margin of error": confidence_interval["Margin of Error"],
    "standard error": confidence_interval["Standard Error"],
    "lower bound": confidence_interval["Lower bound"],
    "upper bound": confidence_interval["Upper bound"],
    "execution time": exectution_time,
    "approx result": sumAgg,
    "sample size":  sample_size
       
        
        
    }
    return metric_Evaluation

def getAproxMedianAggregation(df,column_name,max_iterations,get_aggregation_result):
    global column_series
    confidencLevel= np.random.uniform(.88, .99)
    columnList = []
    column =  df[column_name]
    n = len(column)
    def f(x):
            indx = int(round(x))
            
            indx = max(0,min(indx, n -1))
            return column.iloc[indx]
    learner = adaptive.Learner1D(f, bounds=(0,n- 1))
    start_time = time.perf_counter()
    for _ in range(max_iterations):
       " """"add learner here to take the single data point
        from column where you call the aggregation 
        you want to perform"""""
       

       
       x_next_list= learner.ask(1)[0]
       x_next = x_next_list[0]
       y_next = f(x_next)
        
       columnList.append(y_next)
       
       learner.tell(x_next,y_next)
    column_series = pd.Series(columnList)
    sumAgg =column_series.median()
    
    end_time =  time.perf_counter()
    exectution_time  = end_time - start_time
    sample_size = column_series.count()
    confidence_interval =confidencInterval(column_series,sample_size,confidencLevel)
    absolute_Error = absoluteError(sumAgg, get_aggregation_result["result"])
    relative_Error = relativeError(absolute_Error, get_aggregation_result["result"])
    precentage_Error = percentageError(relative_Error)
    metric_Evaluation= {
    "absolute error": absolute_Error,
    "relative error": relative_Error,
    "precentage error": precentage_Error,
    "z value": confidence_interval["Z value"],
    "margin of error": confidence_interval["Margin of Error"],
    "standard error": confidence_interval["Standard Error"],
    "lower bound": confidence_interval["Lower bound"],
    "upper bound": confidence_interval["Upper bound"],
    "execution time": exectution_time,
    "approx result": sumAgg,
    "sample size":  sample_size
       
        
        
    }
    return metric_Evaluation

def make_title(agg_label, experiment_number, column_name, plot_type):
    return f"{agg_label.upper()} | Column: {column_name} | Exp {experiment_number} | {plot_type}"


def plotAllMetrics(aggregation_results: dict, experiment_number: int, column_name: str):
    
    # =========================
    # 1. ORGANIZE EXACT VS APPROX
    # =========================
    pairs = {}

    for key, val in aggregation_results.items():
        if val is None:
            continue

        key_lower = key.lower()

        if key_lower.startswith("aproximate") or key_lower.startswith("approx"):
            # Normalize approximate labels to match exact labels
            if key_lower.startswith("aproximate sum"):
                label = "sum"
            elif key_lower.startswith("aproximate avg"):
                label = "avg"
            elif key_lower.startswith("aproximate median"):
                label = "median"
            else:
                label = key_lower.replace("aproximate", "").replace("approx", "").strip()
            side = "approx"
        elif key_lower.startswith("exact"):
            label = key_lower.replace("exact", "").strip()
            side = "exact"
        else:
            continue

        if label not in pairs:
            pairs[label] = {}
        
        pairs[label][side] = val

    # Filter for complete pairs (both exact and approximate results exist)
    complete = {k: v for k, v in pairs.items() if "exact" in v and "approx" in v}

    if not complete:
        print(f"[Experiment {experiment_number}] No valid exact/approx pairs found.")
        return

    # =========================
    # 2. OUTPUT DIRS
    # =========================
    base_dir = os.path.join("plots", f"experiment_{experiment_number}")
    perf_dir = os.path.join(base_dir, "performance")
    acc_dir = os.path.join(base_dir, "accuracy")
    ci_dir = os.path.join(base_dir, "confidence_interval")

    os.makedirs(perf_dir, exist_ok=True)
    os.makedirs(acc_dir, exist_ok=True)
    os.makedirs(ci_dir, exist_ok=True)

    # =========================
    # 3. LOOP AGGREGATIONS
    # =========================
    for agg_label, sides in complete.items():

        exact = sides["exact"]
        approx = sides["approx"]

        # SAFE GETTERS (prevents blank plots / crashes)
        def safe(v, key, default=0):
            return v.get(key, default)

        exact_time = safe(exact, "execution time") * 1000
        approx_time = safe(approx, "execution time") * 1000

        approx_val = safe(approx, "approx result")
        exact_val = safe(exact, "result")
        moe = safe(approx, "margin of error")
        lower = safe(approx, "lower bound")
        upper = safe(approx, "upper bound")
        sample_size = safe(approx, "sample size", 'N/A')
        
        # Calculate speedup and time saved, handle division by zero
        speedup = (exact_time / approx_time) if approx_time > 0 else 0
        time_saved = exact_time - approx_time

        # =========================
        # ⚡ PERFORMANCE PLOT
        # =========================
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(f"{agg_label.upper()} | Column: {column_name} | Exp {experiment_number} | PERFORMANCE")

        gs = gridspec.GridSpec(2, 2)

        ax1 = fig.add_subplot(gs[0, :])
        bars = ax1.bar(["Exact", "Approx"], [exact_time, approx_time], color=['#185FA5', '#0F6E56'])
        ax1.set_title("Execution Time (ms)")
        ax1.set_ylabel("Time (ms)")

        # Add sample size and column name to the performance plot
        ax1.text(
            0.5,
            max(exact_time, approx_time) * 1.08,
            f"Column: {column_name} | Approx Sample Size: {sample_size}",
            ha='center',
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5)
        )

        ax2 = fig.add_subplot(gs[1, 0])
        speedup_color = "#1D9E75" if speedup >= 1 else "#E24B4A"
        ax2.bar([agg_label], [speedup], color=speedup_color)
        ax2.axhline(1, linestyle="--", color="gray")
        ax2.set_title("Speedup Factor")
        ax2.set_ylabel("× faster")
        ax2.text(0, speedup, f"{speedup:.2f}×", ha='center', va='bottom', fontweight='bold')


        ax3 = fig.add_subplot(gs[1, 1])
        save_color = "#1D9E75" if time_saved >= 0 else "#E24B4A"
        ax3.bar([agg_label], [time_saved], color=save_color)
        ax3.axhline(0, color="gray")
        ax3.set_title("Time Saved (ms)")
        ax3.set_ylabel("ms saved (negative = slower)")
        ax3.text(0, time_saved, f"{time_saved:+.2f} ms", ha='center', va='bottom' if time_saved >= 0 else 'top')


        plt.savefig(os.path.join(perf_dir, f"{agg_label}_performance.png"))
        plt.close(fig)

        # =========================
        # 🎯 ACCURACY PLOT
        # =========================
        fig2 = plt.figure(figsize=(16, 10))
        fig2.suptitle(f"{agg_label.upper()} | Column: {column_name} | Exp {experiment_number} | ACCURACY")

        gs2 = gridspec.GridSpec(2, 4)

        ax4 = fig2.add_subplot(gs2[0, 0])
        ax4.bar([agg_label], [safe(approx, "absolute error")], color='#185FA5')
        ax4.set_title("Absolute Error")
        ax4.set_ylabel("Error")

        ax5 = fig2.add_subplot(gs2[0, 1])
        ax5.bar([agg_label], [safe(approx, "relative error")], color='#0F6E56')
        ax5.set_title("Relative Error")
        ax5.set_ylabel("Ratio")

        ax6 = fig2.add_subplot(gs2[0, 2])
        ax6.bar([agg_label], [safe(approx, "precentage error")], color='#FFA500')
        ax6.set_title("Percentage Error")
        ax6.set_ylabel("Percentage")

        # Sample size (FIXED)
        ax7 = fig2.add_subplot(gs2[0, 3])
        ax7.bar([agg_label], [sample_size if sample_size != 'N/A' else 0], color='#8A2BE2')
        ax7.set_title("Sample Size (n)")
        ax7.set_ylabel("Count")
        ax7.text(0, sample_size if sample_size != 'N/A' else 0, f"{column_name}", ha='center', va='bottom', fontsize=9)


        ax8 = fig2.add_subplot(gs2[1, 0])
        ax8.bar(["Lower", "Upper"], [lower, upper], color=['#87CEEB', '#9370DB'])
        ax8.set_title("Confidence Interval Bounds")
        ax8.set_ylabel("Value")

        ax9 = fig2.add_subplot(gs2[1, 1])
        ax9.bar([agg_label], [moe], color='#32CD32')
        ax9.set_title("Margin of Error")
        ax9.set_ylabel("Magnitude")

        ax10 = fig2.add_subplot(gs2[1, 2])
        ax10.bar([agg_label], [safe(approx, "standard error")], color='#FF6347')
        ax10.set_title("Standard Error")
        ax10.set_ylabel("Magnitude")

        ax11 = fig2.add_subplot(gs2[1, 3])
        ax11.bar([agg_label], [safe(approx, "z value")], color='#DA70D6')
        ax11.set_title("Z Value")
        ax11.set_ylabel("Value")

        plt.savefig(os.path.join(acc_dir, f"{agg_label}_accuracy.png"))
        plt.close(fig2)

        # =========================
        # 📊 CONFIDENCE INTERVAL PLOT (FIXED)
        # =========================
        fig3 = plt.figure(figsize=(10, 6))
        ax = fig3.add_subplot(111)

        x = 0 # numeric position for plotting

        # CI plot with error bars
        ax.errorbar(
            x,
            approx_val,
            yerr=moe,
            fmt='o',
            capsize=8,
            label=f"Approx (CI: {lower:.2f}-{upper:.2f})",
            color='#1E90FF'
        )

        # Exact value line
        ax.axhline(
            exact_val,
            linestyle="--",
            linewidth=2,
            label=f"Exact Value ({exact_val:.2f})",
            color='#FF4500'
        )

        ax.set_xticks([x])
        ax.set_xticklabels([agg_label])

        ax.set_title(f"{agg_label.upper()} | Column: {column_name} | Exp {experiment_number} | CONFIDENCE INTERVAL")
        ax.set_ylabel("Value")
        ax.legend()

        # Add column name and sample size to the annotation
        ax.text(
            x,
            upper,
            f"Column: {column_name}\nn={sample_size}",
            ha='center',
            va='bottom',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5)
        )

        ax.text(
            x,
            lower,
            f"Lower: {lower:.2f}",
            ha='center',
            va='top',
            fontsize=9
        )
        
        plt.savefig(os.path.join(ci_dir, f"{agg_label}_confidence_interval.png"))
        plt.close(fig3)

        print(f"[Experiment {experiment_number}] Saved all plots for {agg_label}")

    
def main():
    # for i in range(3):
        
    superStore =  pd.read_csv("../datasets/1/Superstore.csv", encoding='latin1')


    print(superStore.head())
        # while True:
            
        #     number = float(input("please input the percentage of samples you would likes to perform a random sample"))

        #     if(number >60 or number < 1):
        #         print("please input a valid number through 1 to 60")
        #     else:
        #         break
        # number = np.random.uniform(1,60.0)
        # fraction = randomSampleNumberGenerator(number)
    while True:
        try:
            column_Name = input('\n please select the name of the column you want topreform a random sample on')
            max_iteration_list = [55,60,30]
            for experiment_number, (iteration) in enumerate(max_iteration_list):
                get_sum_Aggregation  =  getSumAggregation(superStore, column_Name)
                get_sum_Aprox_Aggregation = getAproxSumAggregation(superStore,column_Name,iteration,get_sum_Aggregation)
                
                
                get_Avg_Aggregation  =  getAvgAggregation(superStore, column_Name)
                get_Avg_Aprox_Aggregation = getAproxAvgAggregation(superStore,column_Name,iteration,get_Avg_Aggregation)
                
                
                get_Median_Aggregation  =  getMedianAggregation(superStore, column_Name)
                get_Median_Aprox_Aggregation = getAproxMedianAggregation(superStore,column_Name,iteration,get_Median_Aggregation)
                metrics = {
                    "aproximate sum":   get_sum_Aprox_Aggregation,
                    "exact sum":    get_sum_Aggregation,
                    "aproximate avg": get_Avg_Aprox_Aggregation,
                    "aproximate median": get_Median_Aprox_Aggregation,
                    "exact avg": get_Avg_Aggregation,
                    "exact median": get_Median_Aggregation
                }
                print(f"Heree is the metrics variable *******\n {metrics}")
                print(f"here is experiment number ***** {experiment_number}")
                plotAllMetrics(metrics, experiment_number=experiment_number, column_name=column_Name)     
            break           
            
            
        except Error:
                print(f"invalid: {Error}")
    
main()