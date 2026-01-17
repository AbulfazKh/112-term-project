import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD CLEAN DATA
# ---------------------------------------------------------
# Make sure 'cleaned_kidney_data.csv' is in the same folder
df = pd.read_csv("cleaned_kidney_data.csv")

# ---------------------------------------------------------
# 2. PREPARE DATA (Age Grouping)
# ---------------------------------------------------------
# Create Age Groups (Binning) as specified in the PDF
# We group the numeric 'age' column so the bar chart is readable
age_bins = [0, 30, 45, 60, 75, 100]
age_labels = ['Youth (<30)', 'Adult (30-45)', 'Middle-Age (45-60)', 'Senior (60-75)', 'Elderly (75+)']

df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

# ---------------------------------------------------------
# 3. SET VISUAL STYLE
# ---------------------------------------------------------
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# 4. CREATE THE PLOT (RQ1)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# We use a Bar Plot to compare average eGFR levels
# x = Age Groups, y = eGFR value, hue = Diabetes status (splits the bars)
sns.barplot(
    data=df,
    x='age_group',
    y='egfr',
    hue='diabetes',
    palette='viridis',
    errorbar=None  # Removes the confidence interval lines to keep bars clean
)

# ---------------------------------------------------------
# 5. LABELS AND TITLE
# ---------------------------------------------------------
plt.title('Impact of Age and Diabetes on Kidney Function (eGFR)', fontsize=14)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Average eGFR (mL/min/1.73m²)', fontsize=12)
plt.legend(title='Diabetes Status', loc='upper right')

# Add a reference line for "Healthy" eGFR (approx 90)
plt.axhline(y=90, color='gray', linestyle='--', alpha=0.5, label='Healthy Reference')

# Adjust layout and show
plt.tight_layout()
print("Displaying Havva's Plot (RQ1)...")
plt.show()