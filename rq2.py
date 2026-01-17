import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. LOAD THE DATA
# ---------------------------------------------------------
df = pd.read_csv('cleaned_kidney_data.csv')

# ---------------------------------------------------------
# 2. CREATE THE PLOT
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Create the Scatter Plot
# Changed palette to 'deep' for different colors
sns.scatterplot(
    data=df,
    x='bmi',
    y='systolic_bp',
    hue='ckd_stage',
    style='ckd_stage',
    palette='deep',      # CHANGED: New color palette
    s=100,
    alpha=0.7
)

# Add Titles and Labels
plt.title('Relationship Between BMI and Systolic BP Across CKD Stages', fontsize=16)
plt.xlabel('Body Mass Index (BMI) [kg/m²]', fontsize=12)
plt.ylabel('Systolic Blood Pressure [mmHg]', fontsize=12)

# Move the legend outside
plt.legend(title='CKD Stage', bbox_to_anchor=(1.05, 1), loc='upper left')

# REMOVED: plt.grid() is gone
plt.tight_layout()

print("Displaying plot...")
plt.show()