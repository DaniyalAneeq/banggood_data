# 📦 Banggood Product Data Pipeline & Analysis

### *Data Engineering Hackathon -- Batch 3*

This project is a complete end-to-end data engineering pipeline built
for analyzing product trends on **Banggood.com** across five different
categories.\
It includes **web scraping**, **data cleaning**, **exploratory data
analysis (EDA)**, **SQL Server ingestion**, **SQL analytics**, and a
**final report with insights**.

## 📑 Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Project Architecture](#project-architecture)
-   [Tech Stack](#tech-stack)
-   [Folder Structure](#folder-structure)
-   [Pipeline Steps](#pipeline-steps)
    -   [1. Web Scraping](#1️⃣-web-scraping)
    -   [2. Data Cleaning &
        Transformation](#2️⃣-data-cleaning--transformation)
    -   [3. Exploratory Data Analysis
        (Python)](#3️⃣-exploratory-data-analysis-python)
    -   [4. SQL Server Ingestion](#4️⃣-sql-server-ingestion)
    -   [5. SQL Aggregated Queries](#5️⃣-sql-aggregated-queries)
-   [How to Run](#how-to-run)
-   [Outputs](#outputs)
-   [Conclusion](#conclusion)

## 📌 Overview

The goal of this project is to simulate a real-world data engineering
workflow where product information from Banggood is extracted, cleaned,
analyzed, stored in SQL Server, and later used for aggregated insights.

## ⭐ Features

✔ Scrapes selected categories with pagination\
✔ Cleans and transforms raw data\
✔ Creates derived features\
✔ Generates multiple EDA visualizations\
✔ Loads data into SQL Server\
✔ Runs SQL aggregated analytics\
✔ Produces final report and recommendations

## 🏗 Project Architecture

    [ Web Scraping ]
            ↓
    [ Raw Data (.csv) ]
            ↓
    [ Cleaning & Transformation (Pandas) ]
            ↓
    [ Processed Data ]
            ↓
    [ SQL Server Storage ]
            ↓
    [ SQL Aggregate Analysis ]
            ↓
    [ Final Report + Visualizations ]

## 🛠 Tech Stack

  Component         Tools Used
  ----------------- -----------------------------------
  Language          Python 3
  Scraping          requests, BeautifulSoup, Selenium
  Data Processing   Pandas, NumPy
  Visualization     Matplotlib, Seaborn
  Database          SQL Server
  Connectivity      pyodbc
  Reporting         Markdown / Jupyter Notebook

## 📁 Folder Structure

    project/
    │── scrapers/
    │── data/raw/
    │── data/processed/
    │── sql/
    │── analysis/
    │── images/
    └── README.md

## 🚀 Pipeline Steps

### **1️⃣ Web Scraping**

-   Scraped **5 categories** with pagination\
-   Extracted: name, price, rating, reviews, URL\
-   Saved raw CSVs in `data/raw/`

### **2️⃣ Data Cleaning & Transformation**

-   Cleaned numeric formats\
-   Handled missing values\
-   Removed duplicates\
-   Created derived features such as value_score, price_per_review

### **3️⃣ Exploratory Data Analysis (Python)**

Performed 5+ analyses:\
- Price distribution\
- Rating distribution\
- Price vs Rating correlation\
- Top reviewed products\
- Best value items

### **4️⃣ SQL Server Ingestion**

-   Created database schema\
-   Loaded cleaned CSVs\
-   Validated row counts

### **5️⃣ SQL Aggregated Queries**

Queries include:\
- Avg price per category\
- Avg rating per category\
- Top reviewed items\
- Product count\
- Best value items

## ▶️ How to Run

    uv pip install -r requirements.txt  
    uv run scrapers/main_scraper.py  
    python cleaning_script.py  
    python sql/load_to_sql.py  

## 📊 Outputs

✔ Clean CSVs\
✔ Visual graphs\
✔ SQL insights\
✔ Final report

## 🧠 Conclusion

This project demonstrates a complete data engineering workflow from
scraping to SQL analytics, showcasing strong Python, SQL, and data
engineering skills.
