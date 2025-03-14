import pandas as pd 
import matplotlib 
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


# Constants for the file
cell_types = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
sample_text = "sample_id"
total_count_text = "total_count"
freq_text = "_freq"
count_text = "_count"


# Function takes initial data and formats it into reasonable output data.
# Also adds total and frequency columns to the original dataframe
def parse_data(population_df) -> pd.DataFrame: 
    
    # Intialize output dataframe columns with cell names
    population_df[total_count_text] = None
    parsed_df = pd.DataFrame(columns=[sample_text, total_count_text])
    for cell_type in cell_types:
        parsed_df[cell_type + count_text] = None
        parsed_df[cell_type + freq_text] = None
        population_df[cell_type + freq_text] = None

    # Iterate through each sample
    for index, row in population_df.iterrows():
        # Get Sample ID
        parsed_df.at[index, sample_text] = row['sample']

        # Calculate Total Cell Count for sample
        total_count = 0
        for cell_type in cell_types:
            total_count += row[cell_type]
        parsed_df.at[index, total_count_text] = total_count
        population_df.at[index, total_count_text] = total_count

        # Calculate Cell Count and Frequency for each cell type
        for cell_type in cell_types:
            parsed_df.at[index, cell_type + count_text] = row[cell_type]
            parsed_df.at[index, cell_type + freq_text] = row[cell_type] / total_count
            population_df.at[index, cell_type + freq_text] = row[cell_type] / total_count
    
    return parsed_df


# Organizes data into responders and non-responders, omits non TR1 trials and non-PBMC samples
def analyze_data(population_df):
    responders = {}
    non_responders = {}

    # Intialize dictionaries with cell names
    for cell_type in cell_types:
        responders[cell_type] = []
        non_responders[cell_type] = []


    for index, row in population_df.iterrows():
        # Only use samples that got treatment tr1 and are PBMC
        if row['treatment'] != "tr1" or row['sample_type'] != "PBMC":
            continue
        
        # Add frequencies to correct response group
        for cell_type in cell_types:
            if row['response'] == "y":
                responders[cell_type].append(row[cell_type + freq_text])
            else:
                non_responders[cell_type].append(row[cell_type + freq_text])

    # Plot the data
    plot_data(responders, non_responders)

        
# Plots response data
def plot_data(responders, non_responders):

    # Initialize Subplots
    fig, axes = plt.subplots(1, 5, figsize=(15, 5))
    fig.suptitle("Treatment 1 Cell Frequencies")
    axes = axes.flatten()

    # Plot each cell type
    for index, cell_type in enumerate(cell_types):
        axes[index].boxplot([responders[cell_type], non_responders[cell_type]], labels=["Responders", "Non-Responders"])
        axes[index].set_title(cell_type)
        axes[index].set_ylabel("Frequency")
        axes[index].set_ylim([0, .5])


    # Display the plot
    plt.tight_layout()
    plt.show()


def main():

    # Load the data
    population_df = pd.read_csv("cell-count.csv")

    # Parse Data
    parsed_df = parse_data(population_df)

    # Export Data
    #parsed_df.to_csv("population_analysis.csv", index=False)

    # Analyze and Plot Data
    analyze_data(population_df)


if __name__=="__main__":
    main()