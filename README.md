# Employee Data Cleaning, EDA & Quality Pipeline

A Python-based data cleaning, validation, exploratory data analysis, visualization, and reporting pipeline designed to process messy employee-related datasets and convert them into **clean, validated, analysis-ready datasets and actionable data insights**.

The project demonstrates a complete real-world data-processing workflow using:

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Pytest
* Streamlit
* OpenPyXL
* YAML configuration
* Regular Expressions
* CSV / Excel
* Git / GitHub

The architecture separates **data processing, data analysis, visualization, and user interface responsibilities** so that each layer can be developed, tested, reused, and maintained independently.

---

# Project Objective

Real-world datasets are rarely clean.

Employee datasets can contain:

* Missing values
* Duplicate records
* Incorrect data types
* Inconsistent names
* Invalid emails
* Invalid phone numbers
* Different salary formats
* Mixed date formats
* Invalid numerical values
* Unknown employee references
* Unknown department references
* Invalid work hours
* Invalid overtime hours
* Outliers
* Highly correlated numerical variables
* Inconsistent categorical values

This project provides an automated pipeline that transforms such data into:

```text
Messy Raw Data
      ↓
Clean Data
      ↓
Validated Data
      ↓
Transformed Data
      ↓
EDA Results
      ↓
Visualizations
      ↓
Data Quality Report
      ↓
Streamlit Dashboard
```

---

# Features

## Data Ingestion

* Read CSV files
* Read Excel files
* Load datasets through Python
* Upload CSV files through Streamlit

## Data Profiling

* Detect number of rows
* Detect number of columns
* Display column names
* Detect data types
* Detect missing values
* Detect duplicate rows
* Generate column-level profiles

## Data Cleaning

* Clean column names
* Remove completely empty rows
* Remove duplicate records
* Convert common missing-value strings to `NaN`
* Clean employee names
* Standardize department names
* Standardize gender values
* Standardize employment status
* Clean locations
* Clean job titles

## Numeric Cleaning

* Convert salary values
* Convert monetary values
* Handle currency symbols
* Handle comma-separated numbers
* Convert `K` values
* Convert `LPA` values
* Convert Crore values
* Validate numeric ranges
* Detect invalid salary values
* Validate employee counts
* Validate work hours
* Validate overtime hours

## Date and Time Cleaning

* Parse different date formats
* Parse mixed date formats
* Standardize dates
* Parse different time formats
* Standardize time values
* Detect invalid dates
* Detect invalid times

## Validation

* Validate employee IDs
* Validate employee names
* Validate ages
* Validate emails
* Validate phone numbers
* Validate department references
* Validate employee references
* Validate salaries
* Validate budgets
* Validate work hours
* Validate overtime hours
* Validate attendance dates
* Validate payment dates
* Generate rejection reasons

## Transformation

* Calculate derived salary fields
* Calculate gross salary
* Calculate net salary
* Calculate useful analytical fields
* Prepare clean datasets for analysis

## Record Management

* Separate valid records
* Separate rejected records
* Store rejection reasons
* Export cleaned datasets
* Export rejected datasets

---

# Exploratory Data Analysis

After preprocessing and validation, the cleaned dataset enters the **EDA layer**.

EDA is responsible for understanding the structure, quality, distribution, relationships, and patterns within the cleaned data.

The EDA layer does **not** create Streamlit UI components and does not depend on the presentation layer.

It produces structured analysis results that can be consumed by:

* Streamlit
* Jupyter Notebook
* Reports
* APIs
* Future applications

---

# EDA Architecture

```text
Clean DataFrame
       |
       v
+----------------------+
|      EDA Engine      |
+----------------------+
       |
       +--------------------+
       |                    |
       v                    v
 Dataset Overview     Column Detection
       |                    |
       +----------+---------+
                  |
        +---------+---------+
        |         |         |
        v         v         v
    Numeric   Categorical  Datetime
     Analysis   Analysis   Analysis
        |         |         |
        +---------+---------+
                  |
          +-------+-------+
          |               |
          v               v
      Bivariate      Correlation
       Analysis       Analysis
          |               |
          +-------+-------+
                  |
                  v
             Outlier Analysis
                  |
                  v
            EDA Result
                  |
                  v
          Insight Generation
```

---

# EDA Project Structure

```text
src/
│
├── eda/
│   ├── __init__.py
│   ├── overview.py
│   ├── column_detector.py
│   ├── univariate.py
│   ├── categorical.py
│   ├── datetime_analysis.py
│   ├── bivariate.py
│   ├── correlation.py
│   ├── outliers.py
│   ├── eda_engine.py
│   └── report.py
```

---

# EDA Modules

## 1. `overview.py`

Generates high-level information about the dataset.

It calculates:

* Number of rows
* Number of columns
* Total cells
* Missing values
* Duplicate rows
* Numeric columns
* Categorical columns
* Datetime columns
* Column names

It also generates a column-level profile containing:

```text
Column
Data Type
Missing Count
Missing Percentage
Unique Values
```

---

## 2. `column_detector.py`

Automatically identifies different types of columns.

The detector can identify:

```text
Numeric
Categorical
Datetime
Boolean
Identifier
Text
Constant
Empty
```

This allows the EDA engine to decide which analysis should be applied to each column.

Example:

```text
Employee_ID       → Identifier
Age               → Numeric
Salary            → Numeric
Department        → Categorical
Joining_Date      → Datetime
Is_Active         → Boolean
Employee_Name     → Text
```

---

# 3. `univariate.py`

Performs numerical univariate analysis.

For numeric columns it calculates:

* Count
* Mean
* Median
* Standard deviation
* Minimum
* Maximum
* Q1
* Q3
* Skewness

Example:

```text
Salary

Mean       → 65000
Median     → 61000
Std        → 18000
Minimum    → 25000
Maximum    → 180000
Q1         → 52000
Q3         → 72000
Skewness   → 1.42
```

This helps understand the distribution of individual numerical variables.

---

# 4. `categorical.py`

Analyzes categorical columns.

It generates:

* Number of unique values
* Most frequent value
* Frequency table
* Percentage distribution

Example:

```text
Department

Engineering       35%
HR                20%
Finance           18%
Sales             15%
Operations        12%
```

---

# 5. `datetime_analysis.py`

Analyzes date and time columns.

It extracts:

* Start date
* End date
* Year distribution
* Month distribution
* Day-of-week distribution

Example:

```text
Joining Date

Start Date → 2021-01-05
End Date   → 2025-12-18
```

The analysis can then show how records are distributed across years and months.

---

# 6. `bivariate.py`

Analyzes relationships between two variables.

Currently it supports:

## Numeric vs Numeric

Example:

```text
Experience vs Salary
```

It calculates:

```text
Correlation
Rows Used
```

## Categorical vs Numeric

Example:

```text
Department vs Salary
```

It calculates:

```text
Count
Mean
Median
Minimum
Maximum
```

This helps identify differences between groups.

---

# 7. `correlation.py`

Calculates correlation between numerical columns.

Example:

```text
                Age   Salary   Experience
Age             1.00   0.42       0.38
Salary          0.42   1.00       0.78
Experience      0.38   0.78       1.00
```

The system can identify strong correlations based on a configurable threshold.

Example:

```text
Salary ↔ Experience
Correlation = 0.78
```

---

# 8. `outliers.py`

Performs numerical outlier analysis.

Two approaches are supported:

## IQR Method

The system calculates:

```text
Q1
Q3
IQR
Lower Bound
Upper Bound
```

Using:

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

## Z-Score Method

The system calculates Z-scores and identifies values beyond the configured threshold.

Example:

```text
Salary

IQR Outliers      → 12
Z-Score Outliers  → 8
```

---

# 9. `eda_engine.py`

The EDA engine coordinates all EDA modules.

The flow is:

```text
DataFrame
    ↓
Column Detection
    ↓
Overview
    ↓
Numeric Analysis
    ↓
Categorical Analysis
    ↓
Datetime Analysis
    ↓
Bivariate Analysis
    ↓
Correlation Analysis
    ↓
Outlier Analysis
    ↓
Complete EDA Result
```

The main function is:

```python
eda_result = generate_eda(clean_df)
```

---

# 10. `report.py`

The report layer converts EDA results into human-readable observations.

Examples:

```text
The dataset contains no missing values.

No duplicate rows were detected.

Salary and Experience have a correlation of 0.78.

Salary contains 12 potential IQR outliers.
```

The report contains:

* Dataset summary
* Column profile
* Column detection results
* Numeric analysis
* Categorical analysis
* Datetime analysis
* Bivariate analysis
* Correlation analysis
* Outlier analysis
* Automatically generated insights

---

# Visualization Layer

EDA answers:

> What did we discover?

Visualization answers:

> How can we represent those discoveries visually?

The project therefore keeps visualization code separate from EDA analysis.

---

# Visualization Architecture

```text
                 EDA Results
                      |
                      v
              Visualization Layer
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
 Numeric Plots   Category Plots   Date Plots
       |              |              |
       +--------------+--------------+
                      |
              +-------+-------+
              |               |
              v               v
       Relationship       Correlation
          Plots              Plots
              |               |
              +-------+-------+
                      |
                      v
                 Outlier Plots
                      |
                      v
                   Figures
```

---

# Visualization Project Structure

```text
src/
│
├── visualization/
│   ├── __init__.py
│   ├── numeric_plots.py
│   ├── categorical_plots.py
│   ├── datetime_plots.py
│   ├── relationship_plots.py
│   ├── correlation_plots.py
│   └── outlier_plots.py
```

---

# Visualization Modules

## 1. `numeric_plots.py`

Creates numerical visualizations.

Supported plots:

* Histogram
* KDE
* Boxplot

Example:

```text
Salary Distribution
Salary Boxplot
```

---

# 2. `categorical_plots.py`

Creates categorical visualizations.

Supported plots:

* Count plot
* Percentage plot

Example:

```text
Department Frequency
Department Percentage
```

---

# 3. `datetime_plots.py`

Creates date-based visualizations.

Supported plots:

* Year distribution
* Month distribution

---

# 4. `relationship_plots.py`

Creates relationship visualizations.

Supported plots:

* Scatter plot
* Regression plot
* Categorical vs numeric boxplot
* Violin plot

Examples:

```text
Experience vs Salary
Department vs Salary
```

---

# 5. `correlation_plots.py`

Creates correlation heatmaps.

Example:

```text
+--------------------------------+
|       Correlation Heatmap      |
+--------------------------------+
| Age        Salary   Experience |
| 1.00       0.42       0.38     |
| 0.42       1.00       0.78     |
| 0.38       0.78       1.00     |
+--------------------------------+
```

---

# 6. `outlier_plots.py`

Creates boxplots for numerical outlier inspection.

Example:

```text
Salary Outlier Analysis
```

---

# Why EDA and Visualization Are Separate

The separation follows a software-engineering principle:

> **Analysis should not depend on presentation.**

EDA produces:

```text
Numbers
Tables
Statistics
Patterns
Relationships
Insights
```

Visualization produces:

```text
Charts
Graphs
Figures
```

Streamlit displays them.

Therefore:

```text
EDA
 ↓
Analysis Results
 ↓
Visualization
 ↓
Figures
 ↓
Streamlit
 ↓
User
```

This makes the project easier to maintain and reuse.

For example, the same EDA engine could later be used by:

```text
Jupyter Notebook
       ↓
FastAPI
       ↓
Scheduled Reports
       ↓
Streamlit
       ↓
Data Quality Service
```

without rewriting the analysis logic.

---

# Streamlit Application

The project includes a Streamlit application that acts as the presentation layer.

The Streamlit UI does not perform the core cleaning or EDA calculations itself.

Instead, it consumes the results produced by the processing and analysis layers.

---

# Streamlit Architecture

```text
                    app.py
                      |
                      v
              Data Cleaning Pipeline
                      |
                      v
                 Clean DataFrame
                      |
                      v
                  EDA Engine
                      |
                      v
                 EDA Results
                      |
                      v
                Report Generator
                      |
                      v
                Streamlit Dashboard
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
    Metrics         Tables         Charts
       |              |              |
       +--------------+--------------+
                      |
                      v
                  Insights
```

---

# Streamlit Project Structure

```text
src/
│
└── streamlit_ui/
    ├── __init__.py
    ├── overview_view.py
    ├── numeric_view.py
    ├── categorical_view.py
    ├── datetime_view.py
    ├── bivariate_view.py
    ├── correlation_view.py
    ├── outlier_view.py
    └── dashboard.py
```

---

# Streamlit Modules

## `overview_view.py`

Displays:

* Dataset rows
* Dataset columns
* Missing values
* Duplicate rows
* Column profile

---

## `numeric_view.py`

Displays:

* Numeric statistics
* Histograms
* KDE distributions
* Boxplots

---

## `categorical_view.py`

Displays:

* Frequency tables
* Category counts
* Percentage distributions
* Count plots
* Percentage plots

---

## `datetime_view.py`

Displays:

* Start date
* End date
* Year analysis
* Month analysis
* Date-based visualizations

---

## `bivariate_view.py`

Displays:

* Correlation between numerical variables
* Scatter plots
* Regression plots
* Group statistics
* Categorical vs numeric boxplots
* Violin plots

---

## `correlation_view.py`

Displays:

* Correlation matrix
* Correlation method
* Correlation threshold
* Strong correlations
* Correlation heatmap

---

## `outlier_view.py`

Displays:

* IQR outlier counts
* Z-score outlier counts
* Outlier boxplots

---

## `dashboard.py`

Coordinates all Streamlit views.

The dashboard combines:

```text
Overview
    ↓
Numeric Analysis
    ↓
Categorical Analysis
    ↓
Datetime Analysis
    ↓
Bivariate Analysis
    ↓
Correlation Analysis
    ↓
Outlier Analysis
    ↓
Data Insights
```

---

# Complete Project Architecture

The complete project now follows a layered architecture.

```text
                         USER
                          |
                          v
                  +---------------+
                  |   Streamlit   |
                  |      UI       |
                  +-------+-------+
                          |
                          v
                  +---------------+
                  |   Dashboard   |
                  +-------+-------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
       EDA / Analysis          Visualization
              |                       |
              |                Matplotlib
              |                Seaborn
              |                       |
              +-----------+-----------+
                          |
                          v
                   Clean DataFrame
                          |
                          v
                Data Processing Layer
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
    Cleaner           Validator        Transformer
       |                  |                  |
       +------------------+------------------+
                          |
                          v
                      Raw Data
```

---

# Complete End-to-End Pipeline

```text
Raw CSV / Excel
       |
       v
+----------------+
|     Reader     |
+----------------+
       |
       v
+----------------+
|    Profiler    |
+----------------+
       |
       v
+----------------+
|    Cleaner     |
+----------------+
       |
       v
+----------------+
| String Cleaner |
+----------------+
       |
       v
+----------------+
| Numeric Cleaner|
+----------------+
       |
       v
+----------------+
|  Date Cleaner  |
+----------------+
       |
       v
+----------------+
|   Validator    |
+----------------+
       |
       +--------------------+
       |                    |
       v                    v
   Valid Records       Rejected Records
       |
       v
+----------------+
|  Transformer   |
+----------------+
       |
       v
 Clean DataFrame
       |
       v
+----------------+
|   EDA Engine   |
+----------------+
       |
       +------------------------+
       |                        |
       v                        v
 Statistical Analysis      Data Patterns
       |                        |
       +------------+-----------+
                    |
                    v
             Report Generator
                    |
                    v
              Visualization
                    |
                    v
             Streamlit Dashboard
                    |
                    v
                  USER
```

---

# Project Structure

```text
employee_data_cleaning/
│
├── data/
│   ├── raw/
│   │   ├── employees.csv
│   │   ├── departments.csv
│   │   ├── attendance.csv
│   │   └── payroll.csv
│   │
│   ├── processed/
│   │
│   └── rejected/
│
├── src/
│   ├── __init__.py
│   │
│   ├── reader.py
│   ├── profiler.py
│   ├── cleaner.py
│   ├── string_cleaner.py
│   ├── numeric_cleaner.py
│   ├── date_cleaner.py
│   ├── validator.py
│   ├── transformer.py
│   ├── exporter.py
│   ├── pipeline.py
│   │
│   ├── eda/
│   │   ├── __init__.py
│   │   ├── overview.py
│   │   ├── column_detector.py
│   │   ├── univariate.py
│   │   ├── categorical.py
│   │   ├── datetime_analysis.py
│   │   ├── bivariate.py
│   │   ├── correlation.py
│   │   ├── outliers.py
│   │   ├── eda_engine.py
│   │   └── report.py
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── numeric_plots.py
│   │   ├── categorical_plots.py
│   │   ├── datetime_plots.py
│   │   ├── relationship_plots.py
│   │   ├── correlation_plots.py
│   │   └── outlier_plots.py
│   │
│   └── streamlit_ui/
│       ├── __init__.py
│       ├── overview_view.py
│       ├── numeric_view.py
│       ├── categorical_view.py
│       ├── datetime_view.py
│       ├── bivariate_view.py
│       ├── correlation_view.py
│       ├── outlier_view.py
│       └── dashboard.py
│
├── tests/
│   ├── test_reader.py
│   ├── test_cleaner.py
│   ├── test_numeric_cleaner.py
│   ├── test_date_cleaner.py
│   └── test_validator.py
│
├── config/
│   └── cleaning_rules.yaml
│
├── conftest.py
├── main.py
├── app.py
├── requirements.txt
└── README.md
```

---

# Datasets

The project contains four deliberately messy datasets.

---

# 1. Employees

Contains employee information such as:

* Employee ID
* Employee Name
* Age
* Gender
* Department
* Job Title
* Email
* Phone
* City
* Joining Date
* Joining Time
* Salary
* Bonus
* Employment Status
* Manager ID

Example problems:

```text
Rahul Kumar

PRIYA123

Sneha@123

Ramesh!!!

98765 43210

+91-9988776655

₹6,50,000

650000 INR

₹4.8 LPA

15/02/2024

March 5 2024
```

---

# 2. Departments

Contains:

* Department ID
* Department Name
* Department Head
* Location
* Employee Count
* Annual Budget
* Created Date
* Status

The dataset contains:

* Inconsistent department names
* Inconsistent locations
* Missing values
* Duplicate records
* Different number formats
* Different budget formats
* Different date formats
* Invalid employee counts

---

# 3. Attendance

Contains:

* Attendance ID
* Employee ID
* Employee Name
* Attendance Date
* Check In
* Check Out
* Work Hours
* Status
* Location
* Shift

The dataset contains:

* Invalid dates
* Invalid times
* Negative work hours
* Missing values
* Duplicate records
* Unknown employee IDs

---

# 4. Payroll

Contains:

* Payroll ID
* Employee ID
* Employee Name
* Pay Month
* Basic Salary
* HRA
* Allowances
* Deductions
* Bonus
* Overtime Hours
* Overtime Pay
* Net Salary
* Payment Date
* Payment Status
* Bank Account

The dataset contains:

* Different salary formats
* Mixed dates
* Invalid overtime hours
* Missing values
* Duplicate records
* Unknown employee IDs

---

# Data Cleaning Pipeline

## Step 1 — Read Data

`reader.py` loads CSV and Excel files using Pandas.

```python
df = read_file(path)
```

---

# Step 2 — Profile Data

`profiler.py` provides:

* Number of rows
* Number of columns
* Column names
* Missing values
* Duplicate rows
* Data types

---

# Step 3 — Basic Cleaning

`cleaner.py`:

* Cleans column names
* Removes duplicate rows
* Removes completely empty rows
* Converts common missing-value strings into `NaN`

---

# Step 4 — String Cleaning

`string_cleaner.py`:

* Cleans employee names
* Removes unwanted numbers and symbols
* Standardizes department names
* Standardizes gender values
* Standardizes status values
* Cleans locations
* Cleans job titles

Examples:

```text
PRIYA123        → Priya

Sneha@123       → Sneha

male            → Male

F               → Female

engineering     → Engineering

Human Resources → HR
```

---

# Step 5 — Numeric Cleaning

`numeric_cleaner.py` converts different monetary formats into numerical values.

Examples:

```text
₹6,50,000   → 650000

30K         → 30000

4.8 LPA     → 480000

1.2 Crore   → 12000000
```

It also validates numeric ranges.

Examples:

```text
Age              → 18–65

Employee Count   → >= 0

Work Hours       → 0–24

Overtime Hours   → >= 0
```

---

# Step 6 — Date and Time Cleaning

`date_cleaner.py` handles different formats.

Examples:

```text
2024-01-15

15/02/2024

2023/12/01

01-03-2024

March 5 2024
```

Times are standardized into formats such as:

```text
09:30:00
```

Invalid dates and times are converted to missing values and subsequently handled by validation.

---

# Step 7 — Validation

`validator.py` checks whether records satisfy the required rules.

Examples:

* Missing Employee ID
* Missing Employee Name
* Invalid Age
* Invalid Email
* Invalid Employee ID reference
* Invalid Department reference
* Invalid Attendance Date
* Invalid Payment Date
* Invalid Work Hours
* Invalid Overtime Hours
* Negative salary values
* Negative budget values

Each record receives:

```text
valid
rejection_reason
```

Example:

```text
valid = False

rejection_reason = "Invalid Age"
```

Multiple validation errors can also be recorded for the same record.

---

# Step 8 — Transformation

`transformer.py` creates useful calculated fields.

For payroll data:

```text
Basic Salary
     +
HRA
     +
Allowances
     +
Bonus
     +
Overtime Pay
     -
Deductions
     ↓
Calculated Net Salary
```

The transformation layer prepares validated data for downstream analysis.

---

# Step 9 — Export

`exporter.py` separates records into:

```text
data/processed/
```

and:

```text
data/rejected/
```

Example:

```text
employees_cleaned.csv
employees_rejected.csv

departments_cleaned.csv
departments_rejected.csv

attendance_cleaned.csv
attendance_rejected.csv

payroll_cleaned.csv
payroll_rejected.csv
```

---

# Step 10 — EDA

After cleaning, validation, and transformation:

```text
Clean DataFrame
       ↓
EDA Engine
       ↓
Overview
       ↓
Column Detection
       ↓
Numeric Analysis
       ↓
Categorical Analysis
       ↓
Datetime Analysis
       ↓
Bivariate Analysis
       ↓
Correlation Analysis
       ↓
Outlier Analysis
       ↓
EDA Results
```

---

# Step 11 — Generate Insights

The report layer converts analytical results into readable observations.

Example:

```text
The dataset contains no missing values.

No duplicate rows were detected.

Salary and Experience have a correlation of 0.78.

Salary contains 12 potential IQR outliers.
```

These insights can be displayed in the Streamlit dashboard.

---

# Step 12 — Visualization

The visualization layer creates charts from the cleaned data and analysis requirements.

Supported visualizations include:

```text
Histogram
KDE
Boxplot
Count Plot
Percentage Plot
Bar Plot
Scatter Plot
Regression Plot
Violin Plot
Correlation Heatmap
Outlier Plot
```

---

# Step 13 — Streamlit Dashboard

The Streamlit application combines the complete pipeline into an interactive interface.

The user can:

1. Upload a CSV file
2. Preview raw data
3. Run the cleaning pipeline
4. View cleaned data
5. View EDA results
6. View numerical statistics
7. View categorical analysis
8. View datetime analysis
9. View bivariate relationships
10. View correlation analysis
11. View outlier analysis
12. View charts
13. View automatically generated insights

---

# Streamlit Application Flow

```text
Upload CSV
    ↓
Raw Data Preview
    ↓
Data Cleaning
    ↓
Validation
    ↓
Clean Data Preview
    ↓
EDA
    ↓
Report Generation
    ↓
Dashboard
    ↓
+----------------------+
| Dataset Overview     |
+----------------------+
          ↓
+----------------------+
| Numeric Analysis     |
+----------------------+
          ↓
+----------------------+
| Categorical Analysis |
+----------------------+
          ↓
+----------------------+
| Datetime Analysis    |
+----------------------+
          ↓
+----------------------+
| Bivariate Analysis   |
+----------------------+
          ↓
+----------------------+
| Correlation Analysis |
+----------------------+
          ↓
+----------------------+
| Outlier Analysis     |
+----------------------+
          ↓
+----------------------+
| Data Insights        |
+----------------------+
```

---

# Running the Project

## 1. Clone the repository

```bash
git clone <your-repository-url>

cd employee_data_cleaning
```

---

# 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Run the Complete Data Pipeline

```bash
python main.py
```

The pipeline processes the datasets and exports:

```text
data/processed/
data/rejected/
```

---

# 5. Run Tests

```bash
pytest
```

The test suite covers important components including:

* File reading
* Basic cleaning
* Numeric cleaning
* Money conversion
* Date parsing
* Validation
* Email validation
* Phone cleaning

---

# 6. Run Streamlit

```bash
streamlit run app.py
```

The application opens the interactive dashboard.

---

# Example Pipeline Result

The deliberately messy sample datasets can produce results similar to:

```text
Dataset          Valid       Rejected
---------------------------------------
Employees          20            10
Departments        17             3
Attendance         30             5
Payroll            27             5
```

The exact results depend on the contents of the input datasets and the configured validation rules.

---

# Technologies Used

## Programming

* Python

## Data Processing

* Pandas
* NumPy

## Data Visualization

* Matplotlib
* Seaborn

## User Interface

* Streamlit

## File Processing

* CSV
* Excel
* OpenPyXL

## Validation and Cleaning

* Regular Expressions
* Pandas validation logic
* YAML configuration

## Testing

* Pytest

## Version Control

* Git
* GitHub

---

# Software Architecture Principles

This project follows several practical software-development principles.

## 1. Separation of Responsibilities

Each module has a specific responsibility.

```text
Cleaning
    ↓
Data preparation

EDA
    ↓
Data understanding

Visualization
    ↓
Visual representation

Streamlit
    ↓
User presentation
```

---

# 2. Reusable Components

The EDA layer does not depend on Streamlit.

The visualization layer does not contain business logic.

The Streamlit layer consumes the results.

Therefore, the same analysis code can potentially be reused in:

```text
Jupyter Notebook
Streamlit
FastAPI
Scheduled Reports
Data Quality Services
```

---

# 3. Modular Development

Instead of placing everything inside one large Python file:

```text
app.py
```

the project separates responsibilities into modules.

This improves:

* Maintainability
* Debugging
* Testing
* Reusability
* Readability
* Team development

---

# 4. Layered Pipeline

The application follows:

```text
Input
  ↓
Processing
  ↓
Validation
  ↓
Transformation
  ↓
Analysis
  ↓
Visualization
  ↓
Presentation
```

Each stage consumes the output of the previous stage.

---

# What This Project Demonstrates

This project demonstrates practical Data Science and software-development concepts.

## Data Engineering

* Data ingestion
* Data profiling
* Data cleaning
* Data normalization
* Data validation
* Data transformation
* Data export

## Data Quality

* Missing-value handling
* Duplicate detection
* Invalid-value detection
* Reference validation
* Rejected-record management
* Data-quality reporting

## Exploratory Data Analysis

* Dataset overview
* Column profiling
* Automatic column detection
* Univariate analysis
* Categorical analysis
* Datetime analysis
* Bivariate analysis
* Correlation analysis
* Outlier analysis
* Automated insights

## Data Visualization

* Distribution analysis
* Category analysis
* Relationship analysis
* Correlation visualization
* Outlier visualization

## Software Development

* Modular Python architecture
* Separation of responsibilities
* Reusable functions
* Configuration-based rules
* Error handling
* Automated testing
* Streamlit application development

---

# Future Improvements

Possible future improvements include:

## Data Processing

* YAML-based configurable cleaning rules
* Advanced schema validation
* Batch processing of multiple files
* Database ingestion
* PostgreSQL integration
* MySQL integration
* SQL Server integration
* MongoDB integration

## EDA

* Automatic feature-quality scoring
* Advanced distribution analysis
* Missing-data pattern analysis
* Statistical hypothesis testing
* ANOVA analysis
* Chi-square analysis
* Automated feature relationship detection
* More advanced insight generation

## Visualization

* Interactive Plotly visualizations
* Configurable chart selection
* Interactive filtering
* Advanced time-series visualization
* Dashboard-level chart configuration

## Reporting

* Automated HTML reports
* PDF data-quality reports
* Excel analytical reports
* Downloadable EDA reports
* Data-quality scoring

## Application

* Multi-file upload
* Dataset selection
* Dashboard filters
* User-configurable EDA parameters
* Downloadable cleaned datasets
* Downloadable rejected datasets
* Downloadable EDA reports

## Deployment

* Docker deployment
* Cloud deployment
* CI/CD with GitHub Actions
* Production logging
* Monitoring
* API integration

---

# Author

## Choppara Smily

Bachelors of Information Technology

GitHub:

https://github.com/chopparasmily

---

# Project Summary

This project demonstrates a complete journey from **messy raw employee data to a usable data-quality and analytics application**.

```text
                    RAW DATA
                       ↓
                  DATA READER
                       ↓
                  PROFILING
                       ↓
                   CLEANING
                       ↓
                 VALIDATION
                       ↓
                 TRANSFORMATION
                       ↓
             CLEAN / VALID DATA
                       ↓
                     EDA
                       ↓
          +------------+------------+
          |            |            |
       Numeric    Categorical   Datetime
          |            |            |
          +------------+------------+
                       ↓
                  BIVARIATE
                       ↓
                 CORRELATION
                       ↓
                   OUTLIERS
                       ↓
                INSIGHT REPORT
                       ↓
                VISUALIZATION
                       ↓
               STREAMLIT DASHBOARD
                       ↓
                     USER
```

The project therefore moves beyond simple data cleaning and demonstrates a complete **Data Processing → Data Quality → EDA → Visualization → Reporting → Application** workflow.
