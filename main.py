import numpy as np
import PlotSummaryDataRobinson as psdr
import RobinsonCode as rc
import os
import yaml


def main():
    results = []
    
    # Plot folder
    plot_folder = "plots"    
    os.makedirs(plot_folder, exist_ok=True)
    
    # Read Parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)

    qual_stddev = params["qual_stddev"]
    threshold_stddev = params["threshold_stddev"]
    n = params["n"]
    threshold_mean = params["threshold_mean"]

    
    for th_noise in threshold_stddev:        

        for qual_noise in qual_stddev:            

            print(f"Nest Quality Noise={qual_noise}, Threshold Noise={th_noise}")

            np.random.seed(42) # Set random.seed for reproducible runs

            # Run RObinsonCode and take accuracy, mean_time, accepts values
            accuracy, mean_time, accepts = run_robinson(qual_val=qual_noise,n=n, 
                                                        threshold_mean=threshold_mean, threshold_stddev=th_noise)

            # Append values in results
            results.append((qual_noise, th_noise, accuracy, mean_time, accepts))

      
    # Accuracy vs Noise Plot
    accuracy_plot_path = os.path.join(plot_folder, "accuracy_vs_noise.png")
    acc_results = [(r[0], r[1], r[2]) for r in results]  # qual_noise, th_noise, accuracy
    psdr.PlotAccuracy(acc_results, threshold_stddev, accuracy_plot_path)

    # Decision time vs Noise Plot
    decision_time_plot_path = os.path.join(plot_folder, "decision_time_vs_noise.png")
    time_results = [(r[0], r[1], r[3]) for r in results] # qual_noise, th_noise, mean_time
    psdr.PlotDecisionTime(time_results, threshold_stddev, decision_time_plot_path)

    distribution_plot_path = os.path.join(plot_folder, "selection_distribution.png")
    psdr.PlotSelectionDistribution(results, threshold_stddev, distribution_plot_path)


def run_robinson(qual_val, n, threshold_mean, threshold_stddev):

    # probabilities of visiting each site from each other
    probs = np.array([[0.91, 0.15, 0.03], [0.06, 0.80, 0.06], [0.03, 0.05, 0.91]])

    # mean time to get between each nest
    time_means = np.array([[1, 36, 143], [36, 1, 116], [143, 116, 1]])

    # standard deviation of time to get between each nest
    time_stddevs = time_means / 5

    # mean quality of each nest. Note home is -infinity so it never gets picked
    quals = np.array([-np.inf, 4, 6])
    
    # standard deviation of quality: essentially this controls
    # how variable the ants assessment of each nest is.
    qual_stddev = np.array([0.0, qual_val, qual_val]) # set home nest qual_stddev=0 because quality already -np.inf

    # Run RobinsonCode function
    (accuracy, mean_decision_time, accepts) = rc.RobinsonCode(n, quals, probs, threshold_mean, threshold_stddev, 
                                                              qual_stddev, time_means, time_stddevs)

    # Take returns of accuracy, mean_decision_time, accepts
    return accuracy, mean_decision_time, accepts

if __name__ == "__main__":
    main()