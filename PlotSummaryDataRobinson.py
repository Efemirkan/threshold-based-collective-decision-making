import matplotlib.pyplot as plt
import numpy as np

def PlotAccuracy(results, threshold_stddev, out_path):

    # Convert results into numpy array
    data = np.array(results, dtype=[('qual_stddev', float), ('threshold_stddev', float), ('accuracy', float)])

    # Create plot
    plt.figure(figsize=(8, 5))

    # Iterate over each threshold standard deviation
    for th_noise in threshold_stddev:

        # Pick the rows where the threshold matches th_noise
        mask = (data['threshold_stddev'] == th_noise)
        subset = data[mask]
        
        # Sort by increasing noise 
        order = np.argsort(subset['qual_stddev'])

        # Plot accuracy vs Nest Quality Noise for each threshold
        plt.plot(subset['qual_stddev'][order], subset['accuracy'][order], 
                 marker='o', label=f"Threshold Noise: {th_noise}")

    plt.xlabel("Nest Quality Noise") # label x-axis
    plt.ylabel("Accuracy") # label y-axis
    plt.title("Accuracy vs Nest Quality Noise for Each Threshold Noise") # set title
    plt.grid(True) # add grid
    plt.legend() # add lagend
    plt.savefig(out_path) # save figure the folder
    plt.close()

def PlotDecisionTime(results, threshold_stddev, out_path):

    # Convert results into numpy array
    data = np.array(results, dtype=[('qual_stddev', float), ('threshold_stddev', float), ('mean_time', float)])

    # Create plot
    plt.figure(figsize=(8, 5))

    # Iterate over each threshold standard deviation
    for th_noise in threshold_stddev:

        # Pick the rows where the threshold matches th_noise
        mask = (data['threshold_stddev'] == th_noise)
        subset = data[mask]
        
        # Sort by increasing noise 
        order = np.argsort(subset['qual_stddev'])

        # Plot mean decision time vs Nest Quality Noise for each threshold
        plt.plot(subset['qual_stddev'][order], subset['mean_time'][order], 
                 marker='o', label=f"Threshold Noise: {th_noise}")

    plt.xlabel("Nest Quality Noise") # label x-axis
    plt.ylabel("Mean Decision Time") # label y-axis
    plt.title("Decision Time vs Nest Quality Noise for Each Threshold Noise") # set title
    plt.grid(True) # add grid
    plt.legend() # add lagend
    plt.savefig(out_path) # save figure the folder
    plt.close()


def PlotSelectionDistribution(results, threshold_stddev, out_path):

    # Convert results into numpy array
    data = np.array(results,dtype=[('qual_stddev', float), ('threshold_stddev', float), ('accuracy', float), 
                                    ('mean_time', float), ('accepts', object)])

    # Sorted quality noise
    qual_stddev = sorted(list(set(data['qual_stddev'])))

    # Create one subplot for each threshold noise value
    fig, axes = plt.subplots(1, len(threshold_stddev), figsize=(16, 5))

    if len(threshold_stddev) == 1:
        axes = [axes]

    # Iterate over each threshold standard deviation
    for i, th_noise in enumerate(threshold_stddev):
        ax = axes[i]

        # Pick the rows where the threshold matches th_noise
        subset = data[data['threshold_stddev'] == th_noise]

        # Store selections for each nest 
        home_visits = []
        poor_visits = []
        good_visits = []

        # Iterate over each nest quality standard deviation
        for qual_noise in qual_stddev:

            # Pick the rows where the quality matches qual_noise
            row = subset[subset['qual_stddev'] == qual_noise][0]
            accepts = row['accepts'] # store accepted nest indices

            total = len(accepts) # total number of decisions

             # Calculate selections for each nest type
            home_visits.append(np.sum(accepts == 0) / total)
            poor_visits.append(np.sum(accepts == 1) / total)
            good_visits.append(np.sum(accepts == 2) / total)

         # Plot stacked bar chart
        ax.bar(qual_stddev, home_visits, label="Home", color="gray")

        # Stack poor nest selections
        ax.bar(qual_stddev, poor_visits, bottom=home_visits, label="Poor nest", color="yellow")
        # Stack good nest selections
        ax.bar(qual_stddev, good_visits, bottom=np.array(home_visits) + np.array(poor_visits), 
               label="Good nest", color="red")

        ax.set_title(f"Threshold Noise = {th_noise}") # set subplots ttitles
        ax.set_xlabel("Nest Quality Noise") # label x-axis
        ax.set_xticks(qual_stddev) # # Set x as nest quality noises

        # Label y-axis onl at the first
        if i == 0:
            ax.set_ylabel("Nest Selection")

    plt.legend(bbox_to_anchor=(0.5, 1.10)) # add lagend
    plt.tight_layout()
    fig.savefig(out_path, bbox_inches="tight") # save figure the folder
    plt.close(fig)