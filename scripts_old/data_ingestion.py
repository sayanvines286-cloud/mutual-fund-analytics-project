import pandas as pd
import os

raw_folder = "Data/raw"

print("=" * 50)
print("DATA INGESTION STARTED")
print("=" * 50)

if not os.path.exists(raw_folder):
    print(f"Folder not found: {raw_folder}")
else:
    files = os.listdir(raw_folder)

    csv_files = [f for f in files if f.endswith(".csv")]

    print(f"CSV Files Found: {len(csv_files)}")

print("DATA INGESTION COMPLETED")
import pandas as pd
import os

raw_folder = "Data/raw"

print("=" * 60)
print("DATA INGESTION STARTED")
print("=" * 60)

csv_files = [f for f in os.listdir(raw_folder) if f.endswith(".csv")]

print(f"\nCSV Files Found: {len(csv_files)}\n")

for file in csv_files:
    file_path = os.path.join(raw_folder, file)

    print("\n" + "=" * 60)
    print(f"FILE: {file}")
    print("=" * 60)

    try:
        df = pd.read_csv(file_path)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"Error reading {file}: {e}")

print("\n" + "=" * 60)
print("DATA INGESTION COMPLETED")
print("=" * 60)
