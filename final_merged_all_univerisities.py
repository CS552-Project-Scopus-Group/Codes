import os
import pandas as pd
from unidecode import unidecode

# Paths for the two Excel files to merge
file1_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\merged_data_emre.xlsx"
file2_path = r"C:\Users\emre.ozturk\Desktop\SCRAP\merged_data_baki.xlsx"
output_file = r"C:\Users\emre.ozturk\Desktop\SCRAP\final_merged_data.xlsx"

def convert_to_english(text):
    return unidecode(text)

def merge_two_excels(file1, file2, output_path):
    try:
        # Read the first Excel file
        df1 = pd.read_excel(file1)
        df1.columns = [convert_to_english(col) for col in df1.columns]
        df1 = df1.applymap(lambda x: convert_to_english(x) if isinstance(x, str) else x)

        # Read the second Excel file
        df2 = pd.read_excel(file2)
        df2.columns = [convert_to_english(col) for col in df2.columns]
        df2 = df2.applymap(lambda x: convert_to_english(x) if isinstance(x, str) else x)

        # Define the columns to merge on
        columns_to_merge_on = ["University", "Faculty", "Department", "Title, Name and Surname"]

        # Ensure both dataframes have the required columns
        df1 = df1[columns_to_merge_on]
        df2 = df2[columns_to_merge_on]

        # Merge the dataframes on the specified columns
        merged_df = pd.merge(df1, df2, on=columns_to_merge_on, how="outer")

        # Save the combined DataFrame to the output path
        merged_df.to_excel(output_path, index=False)
        print(f"Final merged Excel saved to {output_path}")
    except Exception as e:
        print(f"Error merging files: {e}")

merge_two_excels(file1_path, file2_path, output_file)
