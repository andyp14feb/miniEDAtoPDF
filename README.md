# Mini EDA Module

This repository contains a Python module to perform a quick exploratory data analysis (EDA) on a given dataset. The module generates a PDF report with essential statistical details about each column in the dataset, including non-null values, missing values, distinct values, and numerical summaries. Additionally, the module creates distribution plots for numerical and categorical columns and saves the temporary images in a subfolder for easy management.



> **Disclaimer**: This code was created with the assistance of AI (OpenAI's ChatGPT). While the logic and structure were generated and refined by AI, it is important to review and customize the code to fit specific use cases and data requirements.
> 
> 

## Features

- **Generate PDF Report**: Creates a detailed EDA report in PDF format.
- **Column Summary**: For each column, it calculates:
  - Non-null values count
  - Missing values count and percentage
  - Distinct values count and percentage
  - For numerical columns, provides basic statistics (min, max, mean, percentiles).
- **Visualizations**: Creates bar plots for:
  - Distribution of numerical columns (if distinct values are ≤ 20)
  - Top 10 most frequent values for categorical columns
- **Temporary Image Management**: Saves generated plots to a subfolder `mini_eda_images` for easy management and cleanup.

## Requirements

- Python 3.x
- Pandas
- Matplotlib
- ReportLab

You can install the required libraries using pip:

```bash
pip install pandas matplotlib reportlab
```

## ## Usage

### 1. Import the module

In your Python script or notebook, import the `mini_eda` function from the module:

```
from mini_eda_module import mini_eda
```

### 2. Load your dataset

Load your dataset using Pandas:

```
import pandas as pd

# Load your dataset (adjust the path as needed)
df = pd.read_csv('./your_data.csv')
```

### 3. Generate the EDA Report

Call the `mini_eda` function and provide the dataset and output PDF filename:

```
pdf_filename = 'eda_report.pdf'
mini_eda(df, pdf_filename)
```

This will generate a PDF report (`eda_report.pdf`) with a summary of the dataset and distribution plots. The images will be saved in a folder named `mini_eda_images`.

### 4. Check the generated report

The generated PDF (`eda_report.pdf`) will contain:

- A summary for each column in your dataset

- Distribution plots for numerical and categorical columns (if applicable)

## Folder Structure

The folder structure will look like this:

```
├── mini_eda_module.py          # Python module with the EDA function
├── mini_eda_images/            # Folder where images are saved temporarily
│   ├── <column_name>_distribution.png
│   └── <column_name>_top10_distribution.png
├── your_notebook_or_script.py  # Your Jupyter notebook or Python script using the module
└── eda_report.pdf              # The generated EDA report

```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests. Contributions are welcome!

## Contact

For any inquiries, feel free to open an issue on the GitHub repository or reach out via email.



### 
