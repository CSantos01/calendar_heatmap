import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess

this_dir = Path(__file__).resolve().parent
output_dir = this_dir / 'output'
output_dir.mkdir(exist_ok=True)

# Read the CSV file
for doi in ["Total", "Events", "Births", "Deaths"]:
    file_path = output_dir / f'calendar_summary_{doi}.csv'
    data = pd.read_csv(file_path, index_col=0)

    # Calculate mean and standard deviation for each month and day
    data['Mean'] = data.mean(axis=1)
    data['Std'] = data.std(axis=1)
    mean_row = data.mean().round(0)
    std_row = data.std().round(0)
    data.loc['Mean'] = mean_row
    data.loc['Std'] = std_row

    # Create the heatmap
    plt.figure(figsize=(18, 8))
    sns.heatmap(data.iloc[:-2, :-2], annot=True, fmt=".0f", cmap="YlGnBu", cbar=True)

    # Add mean and std to the heatmap
    for y in range(data.shape[0] - 2):
        plt.text(data.shape[1] - 1.5, y + 0.5, f'{data.iloc[y, -2]:.0f}', ha='center', va='center', color='black')
        plt.text(data.shape[1] - 0.5, y + 0.5, f'{data.iloc[y, -1]:.0f}', ha='center', va='center', color='black')
    for x in range(data.shape[1] - 2):
        plt.text(x + 0.5, data.shape[0] - 1, f'{data.iloc[-2, x]:.0f}', ha='center', va='center', color='black')
        plt.text(x + 0.5, data.shape[0] - 0.5, f'{data.iloc[-1, x]:.0f}', ha='center', va='center', color='black')

    # Add title and labels
    plt.title(f'Calendar Heatmap of {doi} Events')
    plt.xlabel('Days')
    plt.ylabel('Months')
    plt.savefig(output_dir / f'calendar_heatmap_{doi}.pdf')
    plt.close()

    print(f"Calendar heatmap saved to {output_dir / f'calendar_heatmap_{doi}.pdf'}")

    # # Save the DataFrame as a LaTeX table
    # latex_table = data.to_latex()
    # tex_file_path = output_dir / f'calendar_table_{doi}.tex'
    # with open(tex_file_path, 'w') as tex_file:
    #     tex_file.write("\documentclass{standalone}\n")
    #     tex_file.write("\\begin{document}\n")
    #     tex_file.write(latex_table)
    #     tex_file.write("\end{document}\n")
