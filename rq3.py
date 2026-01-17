import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# LOAD CLEAN DATA
# ---------------------------------------------------------
df = pd.read_csv('cleaned_kidney_data.csv')

# ---------------------------------------------------------
# PREPARE DATA FOR PLOTTING
# ---------------------------------------------------------
# Define the order for categorical variables so they appear logically on the graph
activity_order = ["Low", "Moderate", "High"]
smoking_order = ["Never", "Former", "Current"]

# Convert columns to ordered categories
df["physical_activity_level"] = pd.Categorical(
    df["physical_activity_level"], categories=activity_order, ordered=True
)
df["smoking_status"] = pd.Categorical(
    df["smoking_status"], categories=smoking_order, ordered=True
)

# ---------------------------------------------------------
# CREATE PLOT (RQ3)
# ---------------------------------------------------------
# Set style
sns.set_theme(style="whitegrid")

# Custom colors
palette = {
    "Never": "#3498db",   # Blue
    "Former": "#f39c12",  # Orange
    "Current": "#e74c3c"  # Red
}

# Create the Box Plot (using catplot for faceting by activity level)
g = sns.catplot(
    data=df,
    x="smoking_status",
    y="urine_acr",
    col="physical_activity_level",
    kind="box",
    order=smoking_order,
    col_order=activity_order,
    palette=palette,
    height=5,
    aspect=0.8
)

# ---------------------------------------------------------
# FORMATTING
# ---------------------------------------------------------
g.set_axis_labels("Smoking Status", "Urine ACR (mg/g)")
g.set_titles("{col_name} Activity")

plt.subplots_adjust(top=0.85)
g.fig.suptitle('Impact of Smoking and Physical Activity on Urine ACR', fontsize=16)

print("Displaying Isil's Plot (RQ3)...")
plt.show()