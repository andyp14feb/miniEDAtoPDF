import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import os
import numpy as np
import datetime

def format_number(num):
    try:
        return f"{float(num):,.2f}"
    except Exception:
        return str(num)

def bin_labels_from_edges(edges):
    labels = []
    for i in range(len(edges) - 1):
        labels.append(f"{format_number(edges[i])} - {format_number(edges[i+1])}")
    return labels

def log_message(logfile, msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}\n"
    print(line.strip())
    with open(logfile, "a") as f:
        f.write(line)

def mini_eda(df, pdf_filename):
    logfile = pdf_filename.replace('.pdf', '.log')
    log_message(logfile, "==== mini_eda function started ====")
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    img_folder = 'mini_eda_images'
    os.makedirs(img_folder, exist_ok=True)

    log_message(logfile, f"Columns found: {list(df.columns)}")

    for col in df.columns:
        log_message(logfile, f"--- Processing column: {col} ---")
        story.append(Paragraph(f"Column: {col}", styles['Heading2']))
        non_null_count = df[col].count()
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        distinct_count = df[col].nunique()
        distinct_pct = (distinct_count / len(df)) * 100
        story.append(Paragraph(f"Non-Null Rows: {format_number(non_null_count)}", styles['BodyText']))
        story.append(Paragraph(f"Missing Values: {format_number(missing_count)} ({format_number(missing_pct)}%)", styles['BodyText']))
        story.append(Paragraph(f"Distinct Values: {format_number(distinct_count)} ({format_number(distinct_pct)}%)", styles['BodyText']))
        log_message(logfile, f"Non-Null: {non_null_count}, Missing: {missing_count}, Distinct: {distinct_count}")

        plot_generated = False
        error_message = None

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            notna = df[col].dropna()
            if notna.empty:
                error_message = "All values are missing after dropping NaNs."
                log_message(logfile, f"[{col}] {error_message}")
                story.append(Paragraph(error_message, styles['BodyText']))
            else:
                try:
                    if distinct_count > 20:
                        bins = 20
                        notna = notna.astype(float)
                        cat, bin_edges = pd.cut(notna, bins=bins, retbins=True, include_lowest=True)
                        labels = bin_labels_from_edges(bin_edges)
                        binned_series = pd.cut(df[col].astype(float), bins=bin_edges, labels=labels, include_lowest=True)
                        value_counts = binned_series.value_counts().sort_index()
                        log_message(logfile, f"[{col}] Value counts (binned): {value_counts.to_dict()}")
                        if value_counts.empty or value_counts.sum() == 0 or np.all(value_counts.isna()):
                            error_message = "No data in any bin to plot (all bins are empty or NaN)."
                            log_message(logfile, f"[{col}] {error_message}")
                            story.append(Paragraph(error_message, styles['BodyText']))
                        else:
                            plt.figure(figsize=(10, 6))
                            value_counts.plot(kind='bar')
                            plt.title(f"Binned Distribution of {col}")
                            plt.xlabel(f"Binned {col}")
                            plt.ylabel("Count")
                            img_filename = os.path.join(img_folder, f"{col}_binned.png")
                            plt.tight_layout()
                            plt.savefig(img_filename)
                            plt.close()
                            if os.path.isfile(img_filename):
                                story.append(Spacer(1, 12))
                                story.append(Image(img_filename, width=400, height=300))
                                plot_generated = True
                                log_message(logfile, f"[{col}] Binned plot saved: {img_filename}")
                            else:
                                error_message = f"Image file {img_filename} not created."
                                log_message(logfile, f"[{col}] {error_message}")
                                story.append(Paragraph(error_message, styles['BodyText']))
                    else:
                        value_counts = df[col].value_counts().sort_index()
                        log_message(logfile, f"[{col}] Value counts: {value_counts.to_dict()}")
                        if value_counts.empty or value_counts.sum() == 0 or np.all(value_counts.isna()):
                            error_message = "No data to plot (all values are empty or NaN)."
                            log_message(logfile, f"[{col}] {error_message}")
                            story.append(Paragraph(error_message, styles['BodyText']))
                        else:
                            plt.figure(figsize=(10, 6))
                            value_counts.plot(kind='bar')
                            plt.title(f"Distribution of {col}")
                            plt.xlabel(col)
                            plt.ylabel("Count")
                            img_filename = os.path.join(img_folder, f"{col}_distribution.png")
                            plt.tight_layout()
                            plt.savefig(img_filename)
                            plt.close()
                            if os.path.isfile(img_filename):
                                story.append(Spacer(1, 12))
                                story.append(Image(img_filename, width=400, height=300))
                                plot_generated = True
                                log_message(logfile, f"[{col}] Plot saved: {img_filename}")
                            else:
                                error_message = f"Image file {img_filename} not created."
                                log_message(logfile, f"[{col}] {error_message}")
                                story.append(Paragraph(error_message, styles['BodyText']))
                except Exception as e:
                    error_message = f"Error generating plot for {col}: {str(e)}"
                    log_message(logfile, f"[{col}] {error_message}")
                    story.append(Paragraph(error_message, styles['BodyText']))
        else:
            try:
                top_10 = df[col].value_counts().nlargest(10)
                others_count = len(df) - top_10.sum()
                others_pct = (others_count / len(df)) * 100
                story.append(Paragraph("Top 10 + Others:", styles['BodyText']))
                for value, count in top_10.items():
                    pct = (count / len(df)) * 100
                    story.append(Paragraph(f"{value}: {format_number(count)} ({format_number(pct)}%)", styles['BodyText']))
                story.append(Paragraph(f"Others: {format_number(others_count)} ({format_number(others_pct)}%)", styles['BodyText']))
                log_message(logfile, f"[{col}] Top 10: {top_10.to_dict()}")
                if top_10.empty or top_10.sum() == 0 or np.all(top_10.isna()):
                    error_message = "No data to plot for top categories (empty or NaN)."
                    log_message(logfile, f"[{col}] {error_message}")
                    story.append(Paragraph(error_message, styles['BodyText']))
                else:
                    plt.figure(figsize=(10, 6))
                    top_10.plot(kind='bar')
                    plt.title(f"Top 10 Distribution of {col}")
                    plt.xlabel(col)
                    plt.ylabel("Count")
                    img_filename = os.path.join(img_folder, f"{col}_top10.png")
                    plt.tight_layout()
                    plt.savefig(img_filename)
                    plt.close()
                    if os.path.isfile(img_filename):
                        story.append(Spacer(1, 12))
                        story.append(Image(img_filename, width=400, height=300))
                        plot_generated = True
                        log_message(logfile, f"[{col}] Top 10 plot saved: {img_filename}")
                    else:
                        error_message = f"Image file {img_filename} not created."
                        log_message(logfile, f"[{col}] {error_message}")
                        story.append(Paragraph(error_message, styles['BodyText']))
            except Exception as e:
                error_message = f"Error generating plot for {col}: {str(e)}"
                log_message(logfile, f"[{col}] {error_message}")
                story.append(Paragraph(error_message, styles['BodyText']))

        if not plot_generated and not error_message:
            msg = f"Graph for {col} could not be generated for unknown reasons."
            story.append(Paragraph(msg, styles['BodyText']))
            log_message(logfile, f"[{col}] {msg}")

        story.append(PageBreak())

    log_message(logfile, "==== mini_eda function finished ====")
    pdf.build(story)
