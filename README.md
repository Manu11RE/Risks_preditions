# 🛡️ Invoice Risk: Duplicate Prediction & Anomaly Detection/

## 📌 Project Overview
Duplicate payments are a multi-billion dollar problem in corporate finance. This project implements a **Machine Learning Pipeline** to detect high-risk duplicate invoices. Unlike simple exact-match queries, this system identifies "fuzzy" duplicates—cases where invoice numbers, dates, or amounts vary slightly due to human error or system glitches.



---

## 🚀 Key Features
* **Synthetic Data Augmentation:** Injects 5 specific real-world "corruption cases" (Fuzzy IDs, Amount Variations, Date Shifts) to test model robustness.
* **Hybrid Detection Engine:** Planned implementation combining **Deterministic Matching** with **Fuzzy Logic (Levenshtein)** and **Clustering**.
* **Scalable Architecture:** Designed to use "Blocking" techniques to handle large datasets without memory exhaustion.

---

## 📂 Repository Structure
```text
├── data/
│   ├── raw/             # Original Kaggle dataset
│   └── processed/       # Dataset with injected anomalies
├── notebooks/           # Exploratory Data Analysis & Visualization
├── src/                 # Source code
│   ├── download_data.py # Data ingestion script
│   ├── create_anomalies.py # Data corruption & augmentation logic
│   └── detect_risks.py  # ML/Algorithm for duplicate detection
├── requirements.txt     # Project dependencies
└── README.md            # You are here! 
```

## 🧪 Detection Scenarios
The system is designed to catch 5 distinct risk categories:

| Case | Name | Description | Complexity |
| :--- | :--- | :--- | :--- |
| **Case 1** | **Exact Duplicate** | Identical fields across the board. | 🟢 Low |
| **Case 2** | **Fuzzy Reference** | Typo in `doc_id` (e.g., `193043` vs `193048`). | 🟡 Medium |
| **Case 3** | **Amount Variation** | Same vendor/ref but different totals (Partial payments). | 🟡 Medium |
| **Case 4** | **Time Shift** | Same invoice submitted weeks apart. | 🟠 High |
| **Case 5** | **Hidden Risk** | Same amount/vendor but different IDs (Double Entry). | 🔴 Critical |

---

## 📊 Results (Work in Progress)
* **Status:** Data Augmentation phase completed.
* **Next Step:** Implementing the `RandomForest` classifier to distinguish between `original` and `duplicate` labels.