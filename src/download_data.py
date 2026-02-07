import kagglehub
import pandas as pd
import os


def fetch_and_save_data():
    # 1. Defined the destiny route 
    raw_data_path = os.path.join("data", "raw")
    
    if not os.path.exists(raw_data_path):
        os.makedirs(raw_data_path)
        print(f"Folder created: {raw_data_path}")

    # 2. Download dataset from Kaggle
    download_path = kagglehub.dataset_download("pradumn203/payment-date-prediction-for-invoices-dataset")
    
    # 3. Loacated the csv file into the download folder
    # Search everyone file that finalized in .csv

    files = [f for f in os.listdir(download_path) if f.endswith('.csv')]
    
    if not files:
        print("No founded csv files into the foder")
        return

    # Take the firts csv file founded
    source_file = os.path.join(download_path, files[0])
    target_file = os.path.join(raw_data_path, "invoices_raw.csv")

    # 4. Read and save on the folder
    df = pd.read_csv(source_file)
    df.to_csv(target_file, index=False)
    
    print(f"Dataset saved on: {target_file}")
    print(f"Total rows saved: {len(df)}")

if __name__ == "__main__":
    fetch_and_save_data()