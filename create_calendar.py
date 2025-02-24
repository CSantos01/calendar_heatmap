import os
import csv
from pathlib import Path
import pandas as pd

this_dir = Path(__file__).resolve().parent
output_dir = this_dir / 'output'
output_dir.mkdir(exist_ok=True)

def extract_date_from_filename(filename):
    # Assuming the filename format is 'day_month.csv' (e.g., '12_05.csv')
    base_name = os.path.basename(filename)
    name, _ = os.path.splitext(base_name)
    month, day = name.split('_')
    return month, int(day)

def read_csv_files(folder_path, doi="Total"):
    csv_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            month, day = extract_date_from_filename(filename)
            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == doi:
                        csv_data.append({
                            'day': day,
                            'month': month,
                            'data': int(row[1])
                        })
    return csv_data

# Example usage
folder_path = output_dir / 'events'
for doi in ['Total', 'Events', 'Births', 'Deaths']:
    csv_data = read_csv_files(folder_path, doi)
    df = pd.DataFrame(csv_data)

    # Reorder months
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['month'] = pd.Categorical(df['month'], categories=months_order, ordered=True)

    # Create a pivot table with months as rows, days as columns, and count of events as values
    pivot_table = df.pivot_table(index='month', columns='day', values='data', fill_value=0, aggfunc='sum').astype(int)

    # Save the pivot table to a CSV file
    pivot_table.to_csv(output_dir / f'calendar_summary_{doi}.csv')
    print(f"Calendar summary saved to {output_dir / f'calendar_summary_{doi}.csv'}")

    # Calculate mean and std for each month
    mean_per_month = df.groupby('month')['data'].mean().round(1).sort_values(ascending=False)
    std_per_month = df.groupby('month')['data'].std().round(1).sort_values(ascending=False)
    # Calculate mean and std for each day
    mean_per_day = df.groupby('day')['data'].mean().round(1).sort_values(ascending=False)
    std_per_day = df.groupby('day')['data'].std().round(1).sort_values(ascending=False)

    # Save mean and std to CSV files
    mean_per_month.to_csv(output_dir / f'mean_per_month_{doi}.csv', header=['mean'])
    std_per_month.to_csv(output_dir / f'std_per_month_{doi}.csv', header=['std'])
    mean_per_day.to_csv(output_dir / f'mean_per_day_{doi}.csv', header=['mean'])
    std_per_day.to_csv(output_dir / f'std_per_day_{doi}.csv', header=['std'])

    print(f"Mean and std per month saved to {output_dir / f'mean_per_month_{doi}.csv'} and {output_dir / f'std_per_month_{doi}.csv'}")
    print(f"Mean and std per day saved to {output_dir / f'mean_per_day_{doi}.csv'} and {output_dir / f'std_per_day_{doi}.csv'}")