import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from sklearn.preprocessing import StandardScaler


dir = "C:\\Users\\chris\\Documents\\University\\Research project\\Code\\Experiment results\\"

py_color = "blue"
java_color = "red"
cs_color = "green"
linestyle = "solid"
alpha = 0.75

def plot_hist_line(exec_times, dist_name, h):
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(exec_times)

    x = np.arange(0, max(exec_times)+5)
    pdf_fitted = dist.pmf(x, *param[:-2], loc=param[-2], scale=param[-1])
    scale_pdf = np.trapz(h[0], h[1][:-1]) / np.trapz(pdf_fitted, x)
    pdf_fitted *= scale_pdf

    plt.plot(pdf_fitted, label=dist_name)

def plot_hist(exec_times, dist_names):
    iqr = scipy.stats.iqr(exec_times)
    number_of_bins = int(2 * (iqr//np.cbrt(len(exec_times))))
    bin_cutoffs = np.linspace(np.percentile(exec_times,0), np.percentile(exec_times,100),number_of_bins)
    h = plt.hist(exec_times, bins = 6, color='lightblue')

    for dist in dist_names:
        plot_hist_line(exec_times, dist, h)
    
    plt.xlim(0, np.percentile(exec_times,100))
    plt.ylim(((min(h[0])), max(h[0]) + 5))
    plt.legend()
    plt.ylabel('Amount of (expected) Observations')
    plt.xlabel('Execution Time (ms)')
    plt.grid(True)
    plt.show()

def load_exec_times(file_paths):
    exec_times = []
    for file_path in file_paths:
        results = json.load(open(file_path))
        exec_times.extend(results)

    return np.array(exec_times)

def load_memory_usage(file_path):
    memory_usage = json.load(open(file_path))
    return memory_usage

def compute_curves_exec_times(lang, problem_type):
    averages = []
    lower_ci = []
    upper_ci = []
    for n in range(1,11):
        exec_times = load_exec_times([dir+f"{lang}_{problem_type}_problem_results_{n}.json"])
        ci_lower, ci_upper = compute_ci(exec_times)
        lower_ci.append(ci_lower)
        upper_ci.append(ci_upper)
        average = np.average(exec_times)
        averages.append(average)
    np.array(averages)

    return lower_ci, upper_ci, averages


def compute_ci(exec_times):
    fit = scipy.stats.t.fit(exec_times)
    ci = scipy.stats.t.interval(0.95, *fit)

    return ci[0], ci[1]

def plot_graph_exec_times(problem_type):
    py_lower, py_upper, py_line = compute_curves_exec_times("py", problem_type)
    java_lower, java_upper, java_line = compute_curves_exec_times("java", problem_type)
    cs_lower, cs_upper, cs_line = compute_curves_exec_times("cs", problem_type)
    all_results = np.append(py_line, values=np.append(java_line, cs_line))

    x_axis = np.array([104857,209714,314571,419428,524285,629142,733999,838856,943713,1048576])

    plt.style.use("pltstyle")
    plt.figure(figsize=(12,8))

    plt.plot(x_axis, py_line, color=py_color, linestyle=linestyle, alpha=alpha, label="Python")
    plt.plot(x_axis, java_line, color=java_color, linestyle=linestyle, alpha=alpha, label="Java")
    plt.plot(x_axis, cs_line, color=cs_color, linestyle=linestyle, alpha=alpha, label="C#")

    plt.scatter(x_axis, py_line, color=py_color)
    plt.scatter(x_axis, java_line, color=java_color)
    plt.scatter(x_axis, cs_line, color=cs_color)

    plt.fill_between(x_axis, py_lower, py_upper, alpha=0.25, color=py_color)
    plt.fill_between(x_axis, java_lower, java_upper, alpha=0.25, color=java_color)
    plt.fill_between(x_axis, cs_lower, cs_upper, alpha=0.25, color=cs_color)

    plt.axis([min(x_axis),max(x_axis),min(all_results),max(all_results)])

    plt.ylim(min(all_results), max(all_results)+100)
    plt.xlim(min(x_axis), max(x_axis)+min(x_axis))
    plt.legend(fontsize='32', loc='upper left')
    plt.xlabel('$n$')
    plt.ylabel('Execution Time (ms)')
    plt.grid(True)
    plt.show()

def plot_graph_memory_usage(file_path):
    memory_usage = load_memory_usage(dir+file_path)
    py_line = memory_usage[0]
    java_line = memory_usage[1]
    cs_line = memory_usage[2]
    all_results = []
    for i in range(3):
        all_results.extend(memory_usage[i])
    print(all_results)
    x_axis = np.array([104857, 209714, 314571, 419428, 524285, 629142, 733999, 838856, 943713, 1048576])

    plt.style.use("pltstyle")
    plt.figure(figsize=(12, 8))

    plt.plot(x_axis, py_line, color=py_color, linestyle=linestyle, alpha=alpha, label="Python")
    plt.plot(x_axis, java_line, color=java_color, linestyle=linestyle, alpha=alpha, label="Java")
    plt.plot(x_axis, cs_line, color=cs_color, linestyle=linestyle, alpha=alpha, label="C#")

    plt.scatter(x_axis, py_line, color=py_color)
    plt.scatter(x_axis, java_line, color=java_color)
    plt.scatter(x_axis, cs_line, color=cs_color)

    plt.axis([min(x_axis), max(x_axis), min(all_results), max(all_results)])

    plt.ylim(min(all_results), max(all_results) + np.average(all_results))
    plt.xlim(min(x_axis), max(x_axis) + min(x_axis))
    plt.legend(fontsize='32', loc='upper left')
    plt.xlabel('$n$')
    plt.ylabel('Memory Usage (Bytes)')
    plt.grid(True)
    plt.show()
    
def main():

    #"memory_usage_results.json"
    file_names = ["py_dynamic_problem_results_10.json","py_dynamic_problem_results_9.json"]
    file_paths = [dir+file_names[0]]
    exec_times = load_exec_times(file_paths)
    dist_names = ["binom"]
    plot_hist(exec_times, dist_names)
    #plot_graph_exec_times("dynamic")
    #plot_graph_memory_usage("memory_usage_results.json")

if __name__ == "__main__":
    main()