# mini_eda_module.py

import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import os

def format_number(num):
    return f"{num:,.2f}"

def mini_eda(df, pdf_filename):
    # Create a PDF file
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Create a subfolder for images
    img_folder = 'mini_eda_images'
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    # Iterate through each column in the dataframe
    for col in df.columns:
        # Count of non-null rows
        non_null_count = df[col].count()
        story.append(Paragraph(f"Column: {col}", styles['Heading2']))
        story.append(Paragraph(f"Non-Null Rows: {format_number(non_null_count)}", styles['BodyText']))

        # Missing values
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        story.append(Paragraph(f"Missing Values: {format_number(missing_count)} ({format_number(missing_pct)}%)", styles['BodyText']))

        # Distinct values
        distinct_count = df[col].nunique()
        distinct_pct = (distinct_count / len(df)) * 100
        story.append(Paragraph(f"Distinct Values: {format_number(distinct_count)} ({format_number(distinct_pct)}%)", styles['BodyText']))

        # Check if the column is numerical or categorical
        if pd.api.types.is_numeric_dtype(df[col]):
            # Numerical column
            min_val = df[col].min()
            max_val = df[col].max()
            mean_val = df[col].mean()
            q5 = df[col].quantile(0.05)
            q25 = df[col].quantile(0.25)
            q50 = df[col].quantile(0.50)
            q75 = df[col].quantile(0.75)
            q95 = df[col].quantile(0.95)
            story.append(Paragraph(f"Min: {format_number(min_val)}", styles['BodyText']))
            story.append(Paragraph(f"Max: {format_number(max_val)}", styles['BodyText']))
            story.append(Paragraph(f"Mean: {format_number(mean_val)}", styles['BodyText']))
            story.append(Paragraph(f"5th Percentile (Q5): {format_number(q5)}", styles['BodyText']))
            story.append(Paragraph(f"25th Percentile (Q25): {format_number(q25)}", styles['BodyText']))
            story.append(Paragraph(f"50th Percentile (Q50): {format_number(q50)}", styles['BodyText']))
            story.append(Paragraph(f"75th Percentile (Q75): {format_number(q75)}", styles['BodyText']))
            story.append(Paragraph(f"95th Percentile (Q95): {format_number(q95)}", styles['BodyText']))

            # Check if the column can be divided into less than 20 groups
            if distinct_count <= 20:
                # Plot distribution
                plt.figure(figsize=(10, 6))
                df[col].value_counts().sort_index().plot(kind='bar')
                plt.title(f"Distribution of {col}")
                plt.xlabel(col)
                plt.ylabel("Count")
                img_filename = os.path.join(img_folder, f"{col}_distribution.png")
                plt.savefig(img_filename)
                plt.close()
                story.append(Spacer(1, 12))
                story.append(Image(img_filename, width=400, height=300))
            else:
                story.append(Paragraph(f"Min: {format_number(min_val)}", styles['BodyText']))
                story.append(Paragraph(f"Max: {format_number(max_val)}", styles['BodyText']))
        else:
            # Categorical column
            story.append(Paragraph(f"Distinct Values: {format_number(distinct_count)}", styles['BodyText']))

            # Top 10 + others
            top_10 = df[col].value_counts().nlargest(10)
            others_count = len(df) - top_10.sum()
            others_pct = (others_count / len(df)) * 100
            story.append(Paragraph("Top 10 + Others:", styles['BodyText']))
            for value, count in top_10.items():
                pct = (count / len(df)) * 100
                story.append(Paragraph(f"{value}: {format_number(count)} ({format_number(pct)}%)", styles['BodyText']))
            story.append(Paragraph(f"Others: {format_number(others_count)} ({format_number(others_pct)}%)", styles['BodyText']))

            # Plot distribution
            plt.figure(figsize=(10, 6))
            top_10.plot(kind='bar')
            plt.title(f"Top 10 Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            img_filename = os.path.join(img_folder, f"{col}_top10_distribution.png")
            plt.savefig(img_filename)
            plt.close()
            story.append(Spacer(1, 12))
            story.append(Image(img_filename, width=400, height=300))

        # Add a page break after each column
        story.append(PageBreak())

    # Build the PDF
    pdf.build(story)
