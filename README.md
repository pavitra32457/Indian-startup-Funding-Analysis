Here’s a detailed **README.md** file for your `main.py` project:

---

# Startup Funding Data Analysis

## 📌 Overview

This project analyzes a **startup funding dataset** to clean, process, and visualize funding trends in India.
It performs **data cleaning**, **aggregation**, and **visualization** to extract insights about:

* Yearly & Monthly funding trends
* Top sectors and cities by funding
* Top startups and investors
* Investment type distribution

## 📂 Dataset

The analysis is based on a CSV file named:

```
startup_funding.csv
```

### Expected Columns:

* `Sr No`
* `Date dd/mm/yyyy`
* `Startup Name`
* `Industry Vertical`
* `SubVertical`
* `City  Location`
* `Investors Name`
* `InvestmentnType`
* `Amount in USD`
* `Remarks` *(optional)*

## ⚙️ Features

1. **Data Cleaning**

   * Drops irrelevant columns (`Remarks`)
   * Fills missing values with `"Unknown"`
   * Removes extra spaces & non-breaking spaces
   * Converts text to lowercase for consistency
   * Converts funding amount to numeric values
   * Parses dates into datetime format

2. **Data Aggregation**

   * Calculates yearly and monthly total funding & deal counts
   * Groups funding by sector, city, startup, and investor
   * Analyzes top investment types

3. **Visualizations**

   * Yearly funding trends (line chart)
   * Top sectors by total funding (bar chart)
   * Top cities by total funding (bar chart)
   * Top startups by total funding (bar chart)
   * Top investors by total funding and deals (bar chart)
   * Investment types by funding & deals (bar chart)

## 🛠️ Requirements

Install dependencies using:

```bash
pip install pandas matplotlib seaborn
```

## ▶️ How to Run

1. Place `startup_funding.csv` in the correct path (update path in code if needed).
2. Run the script:

```bash
python main.py
```

3. The program will:

   * Print aggregated data tables
   * Show multiple plots for funding trends and rankings

## 📊 Sample Outputs

* **Yearly Funding Trends:**
  Shows growth/decline patterns in startup investments over the years.
* **Top 10 Sectors & Cities:**
  Reveals where most investment is concentrated.
* **Top Startups & Investors:**
  Highlights key players in the ecosystem.
* **Investment Type Analysis:**
  Compares funding distribution across investment types.


