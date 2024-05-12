import os
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set options for pandas
pd.options.display.float_format = '{:,.2f}'.format
pd.options.mode.chained_assignment = None  # default='warn', to suppress SettingWithCopyWarning in pandas

def setup_directories(base_path, month):
    """Ensure all required directories exist."""
    paths = {
        'reports': os.path.join(base_path, f"{month}_automatically_generated_Reports"),
        'evidence': os.path.join(base_path, f"{month}_Evidence")
    }
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    return paths

def load_data(path, sheet_name="Sheet1"):
    """Load data from an Excel file into a DataFrame."""
    with pd.ExcelFile(path) as xls:
        return xls.parse(sheet_name)

def save_data(df, path, index=False):
    """Save DataFrame to a CSV file."""
    df.to_csv(path, sep=';', index=index)
    logging.info(f"Data saved to {path}")

def aggregate_data(df, group_field, sum_field):
    """Aggregate data by field and sum up another field."""
    return pd.DataFrame({'Sum': df.groupby([group_field])[sum_field].sum()}).reset_index()

def process_collections(collections_path):
    """Process all collection files in the specified directory."""
    all_collections = pd.DataFrame()
    for folder_name in os.listdir(collections_path):
        folder_path = os.path.join(collections_path, folder_name)
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.xlsx') and 'fbl5' not in file_name.lower():
                file_path = os.path.join(folder_path, file_name)
                collection = load_data(file_path)
                collection = collection.iloc[:, :23]  # Assuming the first 23 columns are needed
                all_collections = pd.concat([all_collections, collection], ignore_index=True)

    all_collections.reset_index(drop=True, inplace=True)
    return all_collections

def main():
    base_path = 'C:/automation-Nordea-factoring-reconciliation/'
    input_date = input('Please enter the last day of reported month (YYYYMMDD, for example: 20161231):')
    month = input_date[:6]

    # Setup directories
    paths = setup_directories(base_path, month)

    # Process collections
    collections_path = os.path.join(base_path, month, 'Collections')
    collections = process_collections(collections_path)
    collections_file_path = os.path.join(paths['evidence'], 'collections_evidence.csv')
    save_data(collections, collections_file_path)

    # Further processing and reporting can be added here

if __name__ == "__main__":
    main()
