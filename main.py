import os
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import numpy as np
import requests
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import google.generativeai as genai
from credentials import *
import sys
import shutil
print('****************************** SCRIPT START ******************************')

#### CONFIGURE API KEY ####
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

### IMPORTANT FUNCTIONS ###
def load_data(file):
    r"""Loads the data by pd.read_csv. Run uv autolysis.py and dataset.csv"""
    try:
        data = pd.read_csv(file)
        return data
    except UnicodeDecodeError:
        data = pd.read_csv(file, encoding='ISO-8859-1')
        return data
    except:
        raise Exception("Dataset File is missing. Use uv run autolysis.py <CSV FILE PATH>")

def give_name(file_path: str):
    r"""
    Returns the filtered filename without . and \.
    """
    if "\\" in file_path:
        file_path = file_path.split("\\")[-1]
    if "." in file_path:
        file_path = file_path.split(".")[0]
    return file_path

def detect_datetime_column(data):
    r"""Detects columns with datetime data."""
    for col in data.columns:
        try:
            parsed = pd.to_datetime(data[col])
            if parsed.notna().sum() > 0.8 * len(data):
               return col
        except:
            continue
    return None

def sort_data_by_datetime(data):
    datetime_col = detect_datetime_column(data)
    if datetime_col:
        data[datetime_col] = pd.to_datetime(data[datetime_col], errors="coerce")
        data = data.sort_values(by=datetime_col)
    return data

def time_series_plot(data, time_col):
    global name
    numeric_cols = data.select_dtypes(include=["number"]).columns
    
    if len(numeric_cols) == 0:
        return
    
    plt.figure(figsize=(10, 6))
    
    for col in numeric_cols[:3]:  # limit for clarity
        plt.plot(data[time_col], data[col], label=col)
    
    plt.legend()
    plt.title("Time Series Trends")
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.savefig(f"{name}/time_series_plot.png")
    plt.close()
    
    return f"{name}/time_series_plot.png"

def missing_plot(data):
    r"""Creates a bar chart for missing data by columns."""
    global name

    missing_cols = []
    missing_values = []
    for col in data.columns:
        if data[col].isna().sum() > 0:
            missing_cols.append(col)
            missing_values.append(data[col].isna().sum())
    if missing_cols:
        plt.figure(figsize=(10, 6))
        plt.bar(missing_cols, missing_values, color="blue", alpha=0.7, edgecolor="black")
        plt.title(f"Missing Data by Column in {give_name(file_path=name).capitalize()} Dataset")
        plt.xlabel("Columns")
        plt.ylabel("Number of Missing Values")
        plt.xticks(rotation=45, ha="right")
        plt.savefig(f"{name}/missing_plot.png")
        plt.close()
        return f"{name}/missing_plot.png"

def create_correlation_heatmap(data):
    r"""
    Generates a heatmap of correlations between numerical features in the dataset.

    Parameters:
    data (DataFrame): The dataset as a pandas DataFrame.
    save_path (str): Path to save the heatmap image.
    """
    global name
    # Select numerical columns
    numeric_data = data.select_dtypes(include=['number'])
    
    if numeric_data.empty:
        print("No numerical data available for correlation heatmap.")
        return

    # Calculate the correlation matrix
    correlation_matrix = numeric_data.corr()

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    seaborn.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(f"{name}/correlation_heatmap.png")
    return f"{name}/correlation_heatmap.png"

def description_of_data(data):
    r"""Gives a short description of the data."""
    return str(data.describe(include="all"))

def number_of_important_columns_plot(data):
    r"""Plots cumulative explained variance using PCA."""
    global name
    numeric_data = data.select_dtypes(include=["number"])

    if numeric_data.empty:
        raise ValueError("No numeric columns found in the dataset.")

    imputer = SimpleImputer(strategy="mean")
    numeric_data_imputed = imputer.fit_transform(numeric_data)

    n_components = min(numeric_data.shape[1], numeric_data.shape[0])
    pca = PCA(n_components=n_components)
    pca.fit(numeric_data_imputed)

    cum_variance = pca.explained_variance_ratio_.cumsum()

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, n_components + 1), cum_variance, marker="o", linestyle="--")
    plt.title(f"Cumulative Explained Variance by PCA Components in {name.capitalize()} Dataset")
    plt.xlabel("Number of Principal Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.grid(True)
    plt.axhline(y=0.9, color="r", linestyle="--", label="90% Variance Threshold")
    plt.legend(loc="lower right")
    plt.savefig(f"{name}/number_of_important_columns.png")
    plt.close()
    return f"{name}/number_of_important_columns.png"

def plot_all_scatter_pairs(data):
    r"""Creates scatter plots for all pairs of numeric columns in the dataset."""
    global name
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        raise ValueError("No numeric columns found in the dataset.")

    seaborn.pairplot(numeric_data, diag_kind="kde", plot_kws={"alpha": 0.6})
    plt.suptitle(f"Scatter Plots for Numeric Columns in {name} dataset", y=1.02)
    plt.savefig(f"{name}/scatter_plot.png")
    plt.close()
    return f"{name}/scatter_plot.png"

def generate_directory():
    r"""Creates a directory for storing results."""
    global name
    try:
        os.makedirs(name)
    except FileExistsError:
        pass

def get_story(data, images):
    r"""Generates a narrative from the data and plots."""
    model = genai.GenerativeModel("gemini-pro")

    plot_descriptions = "\n".join(
        [f"Plot {i+1}: {img}" for i, img in enumerate(images)]
    )
    prompt = f"""
    You are a data analyst.

    Analyze the dataset summary and the generated plots.

    Dataset Summary:
    {data}

    Plots:
    {plot_descriptions}

    Write a clear, structured report including:
    - Key patterns
    - Important correlations
    - Data quality issues
    - Actionable insights
    """

    response = model.generate_content(prompt)
    return response.text

def write_readme(story):
    r"""Writes the generated story to a README.md file."""
    global name
    readme_path = f"{name}/README.md"
    with open(readme_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write(story)
    print(f"README.md file created at {readme_path}")

# Main execution starts here

filename = sys.argv[1]

# Load dataset
data = load_data(filename)

# Create a clean name for output folder
name = give_name(filename)

# Create folder to store results
generate_directory()

# Check if dataset has any datetime column
time_col = detect_datetime_column(data)

# If yes, sort data based on time
if time_col:
    data = sort_data_by_datetime(data)

# Generate basic analysis plots
plot_files = [
    missing_plot(data),
    number_of_important_columns_plot(data),
    plot_all_scatter_pairs(data),
    create_correlation_heatmap(data)
]

# Add time series plot if applicable
if time_col:
    plot_files.append(time_series_plot(data, time_col))

# Generate summary + insights
data_summary = description_of_data(data)
story = get_story(data_summary, plot_files)

# Save insights to README
write_readme(story)

# Zip the output folder for download

shutil.make_archive(name, 'zip', name)

print("****************************** SCRIPT END ******************************")