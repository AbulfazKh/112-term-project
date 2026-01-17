import pandas as pd
import numpy as np
import re

# ---------------------------------------------------------
# 1. LOAD THE DATA
# ---------------------------------------------------------
file_path = 'kidney_function_synthetic_1150_dirty.csv'
df = pd.read_csv(file_path)
print("Data loaded. Shape:", df.shape)

# ---------------------------------------------------------
# 2. STANDARDIZE COLUMN HEADERS
# ---------------------------------------------------------
# Removing special characters like parentheses and dots, replacing spaces with underscores
df.columns = (df.columns.str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace(r'[().]', '', regex=True)
              .str.replace('/', '_')
              .str.replace('?', ''))

# Custom mapping to fix specific messy column names
column_mapping = {
    'physical_activity_lvl': 'physical_activity_level',
    'serumcreatinine_mg_dl': 'serum_creatinine',
    'egfr_ml_min_173m2': 'egfr',
    'urine_acr_mg_g': 'urine_acr',
    'bmikg_m2': 'bmi'
}
df.rename(columns=column_mapping, inplace=True)

print("Columns renamed:", df.columns.tolist())

# ---------------------------------------------------------
# 3. CLEANING CATEGORICAL DATA (STRINGS)
# ---------------------------------------------------------
# We do this BEFORE dropping duplicates to ensure we catch duplicate rows
# that only differed by capitalization (e.g., "Male" vs "male").

cat_cols = ['sex', 'ethnicity', 'smoking_status', 'physical_activity_level', 'diabetes', 'hypertension', 'ckd_stage']


# Renamed function as requested
def new_format(series):
    # Converts to string, lowers case, strips whitespace, and removes punctuation
    cleaned = series.astype(str).str.lower().str.strip()
    cleaned = cleaned.str.replace(r'[.*?#!]', '', regex=True)
    return cleaned


# Apply the formatting function
for col in cat_cols:
    if col in df.columns:
        df[col] = new_format(df[col])

# Manual corrections for specific typos found in the dataset
if 'sex' in df.columns:
    df['sex'] = df['sex'].replace({
        'mlae': 'male', 'feamle': 'female', 'fmeale': 'female', 'femlae': 'female'
    })

if 'ethnicity' in df.columns:
    df['ethnicity'] = df['ethnicity'].replace({
        'tukrish': 'turkish', 'middleeastern': 'middle eastern',
        'sotuh asian': 'south asian', 'southasian': 'south asian'
    })

if 'smoking_status' in df.columns:
    df['smoking_status'] = df['smoking_status'].replace({
        'nveer': 'never', 'neevr': 'never', 'currnet': 'current'
    })

if 'physical_activity_level' in df.columns:
    df['physical_activity_level'] = df['physical_activity_level'].replace({
        'modreate': 'moderate'
    })

if 'ckd_stage' in df.columns:
    df['ckd_stage'] = df['ckd_stage'].replace({
        'nomral': 'normal'
    })

# Final formatting: Title Case and fixing NaN values
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].str.title()
        df[col] = df[col].replace('Nan', np.nan)

# ---------------------------------------------------------
# 4. REMOVE DUPLICATES
# ---------------------------------------------------------
# Now that text is standardized, we can effectively remove true duplicates.
rows_before = len(df)
df.drop_duplicates(inplace=True)
rows_after = len(df)
print(f"Duplicates removed: {rows_before - rows_after}")

# ---------------------------------------------------------
# 5. CLEANING NUMERIC DATA
# ---------------------------------------------------------
# Fix the 'age' column formatting (removing '-')
if 'age' in df.columns:
    df['age'] = df['age'].astype(str).str.replace('-', '', regex=False)
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

target_num_cols = ['age', 'bmi', 'systolic_bp', 'serum_creatinine', 'egfr', 'urine_acr']

for col in target_num_cols:
    if col in df.columns:
        # Impute missing values with the Mean
        avg_value = df[col].mean()
        df[col] = df[col].fillna(avg_value)

        # Outlier Detection (Z-Score Method > 3 SD)
        col_mean = df[col].mean()
        col_std = df[col].std()

        # Define thresholds
        upper_limit = col_mean + (3 * col_std)
        lower_limit = col_mean - (3 * col_std)

        # Identify and cap outliers
        is_outlier = (df[col] < lower_limit) | (df[col] > upper_limit)
        if is_outlier.any():
            df.loc[is_outlier, col] = col_mean

# Impute missing categorical values with the Mode
for col in cat_cols:
    if col in df.columns:
        most_frequent = df[col].mode()[0]
        df[col] = df[col].fillna(most_frequent)

# ---------------------------------------------------------
# 6. EXPORT CLEAN DATA
# ---------------------------------------------------------
print("\n--- Final Data Overview ---")
print(df.info())
print(df.describe())

df.to_csv('cleaned_kidney_data.csv', index=False)
print("\nProcessing complete. File saved as 'cleaned_kidney_data.csv'.")