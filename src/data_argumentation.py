import pandas as pd
import numpy as np
from datetime import timedelta
import random
import os

def inject_anomalies(df, percentage=0.01):
    """
    Injects 5 specific types of duplicates/anomalies into the dataset
    to simulate real-world invoice risks.
    """
    # Ensure date column is in datetime format for calculations
    df['posting_date'] = pd.to_datetime(df['posting_date'])
    
    n_samples = int(len(df) * percentage)
    if n_samples == 0: n_samples = 1 # Handle very small datasets
    
    augmented_data = []

    # 1. Obtain random samples for each case
    cases_samples = {
        'case1': df.sample(n_samples),
        'case2': df.sample(n_samples),
        'case3': df.sample(n_samples),
        'case4': df.sample(n_samples),
        'case5': df.sample(n_samples)
    }

    #  CASE 1: Exact Duplicate 
    # Same code, vendor, doc ref, date, and amount
    c1 = cases_samples['case1'].copy()
    c1['label'] = 'duplicate_exact'
    augmented_data.append(c1)

    #  CASE 2: Similar Reference (Fuzzy) 
    # Same date/amount, but doc_id has a typo (last digit changed)
    c2 = cases_samples['case2'].copy()
    c2['doc_id'] = c2['doc_id'].apply(lambda x: str(x)[:-1] + str(random.randint(0,9)))
    c2['label'] = 'duplicate_fuzzy_ref'
    augmented_data.append(c2)

    #  CASE 3: Different Amount 
    # Same reference/vendor/date, but amount is slightly different (e.g., partial payment)
    c3 = cases_samples['case3'].copy()
    c3['total_open_amount'] = c3['total_open_amount'] * np.random.uniform(0.95, 1.05)
    c3['label'] = 'duplicate_diff_amount'
    augmented_data.append(c3)

    #  CASE 4: Different Date 
    # Same code/vendor/ref, but date is shifted (e.g., 15 days later)
    c4 = cases_samples['case4'].copy()
    c4['posting_date'] = c4['posting_date'] + pd.to_timedelta(np.random.randint(1, 30), unit='d')
    c4['label'] = 'duplicate_diff_date'
    augmented_data.append(c4)

    #  CASE 5: Risk Duplicate (Different ID) 
    # Same amount/vendor/date, but ID is completely different (High risk of double payment)
    c5 = cases_samples['case5'].copy()
    c5['doc_id'] = [str(np.random.randint(1000000, 9999999)) for _ in range(len(c5))]
    c5['label'] = 'risk_duplicate_different_id'
    augmented_data.append(c5)

    # Combine all anomalies
    df_anomalies = pd.concat(augmented_data, ignore_index=True)
    
    # Mark originals
    df['label'] = 'original'
    
    # Final concatenation and shuffle
    df_final = pd.concat([df, df_anomalies], ignore_index=True)
    return df_final.sample(frac=1).reset_index(drop=True)

def main():
    # File paths
    input_path = os.path.join("data", "raw", "invoices_raw.csv")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "invoices_with_anomalies.csv")

    # 1. Load Data
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run your download script first.")
        return

    df_raw = pd.read_csv(input_path)

    # 2. Inject Anomalies
    print(f"Injecting anomalies (1% per case)...")
    df_processed = inject_anomalies(df_raw, percentage=0.01)

    # 3. Save Results
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df_processed.to_csv(output_path, index=False)
    
    # 4. Final Report
    print("-" * 30)
    print(f"Success! Processed file saved at: {output_path}")
    print("\nSummary of records created:")
    print(df_processed['label'].value_counts())
    print("-" * 30)

if __name__ == "__main__":
    main()