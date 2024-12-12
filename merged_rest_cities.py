import os
import pandas as pd
from unidecode import unidecode

# Base directory and output path
data_directory = r"C:\Users\emre.ozturk\Desktop\SCRAP\All_universities"
output_file = r"C:\Users\emre.ozturk\Desktop\SCRAP\merged_data_baki.xlsx"

def convert_to_english(text):
    return unidecode(text)

def find_and_merge_excels(base_path, output_path):
    all_data = []  # List to store all excel data

    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Check for excel files ending with "academic_staff"
            if file.endswith("academic_staff.xlsx"):
                file_path = os.path.join(root, file)
                try:
                    # Read the excel file and convert to English characters
                    df = pd.read_excel(file_path)
                    df.columns = [convert_to_english(col) for col in df.columns]
                    df = df.applymap(lambda x: convert_to_english(x) if isinstance(x, str) else x)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    # Combine all data into a single DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]  # Remove duplicate columns
        # Save the combined data to the output path
        combined_df.to_excel(output_path, index=False)
        print(f"Combined Excel saved to {output_path}")
    else:
        print("No relevant Excel files found.")

find_and_merge_excels(data_directory, output_file)