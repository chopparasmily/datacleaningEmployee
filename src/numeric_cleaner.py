import re
import pandas as pd


def money_to_number(value):
    """Convert money formats like ₹50,000, 30K and 4.8 LPA to numbers."""
    if pd.isna(value):
        return pd.NA

    value=str(value).strip().lower().replace(",","").replace("₹","").replace("$","")
    if value in ["","unknown","null","nan","none"]:
        return pd.NA
# -?       \d+       (?:\.\d+)?
# │         │             │
# │         │             └── optional decimal part
# │         └── one or more digits
# └── optional minus sign
    match=re.search(r"-?\d+(?:\.\d+)?",value)
    if not match:
        return pd.NA

    number=float(match.group())

    if "crore" in value:
        number*=10000000
    elif "lpa" in value or "lakh" in value:
        number*=100000
    elif "k" in value:
        number*=1000

    return number


def clean_numbers(df):
    """Clean numeric, salary, bonus and work-hour columns."""
    money_cols=["Salary","Bonus","Basic Salary","HRA","Allowances","Deductions","Overtime Pay","Net Salary","Annual Budget"]

    for col in money_cols:
        if col in df:
            df[col]=df[col].map(money_to_number)

    numeric_cols=["Age","Employee Count","Work Hours","Overtime Hours"]

    for col in numeric_cols:
        if col in df:
            df[col]=pd.to_numeric(df[col],errors="coerce")

    if "Age" in df:
        df.loc[~df["Age"].between(18,65),"Age"]=pd.NA

    if "Employee Count" in df:
        df.loc[df["Employee Count"]<0,"Employee Count"]=pd.NA

    if "Work Hours" in df:
        df.loc[~df["Work Hours"].between(0,24),"Work Hours"]=pd.NA

    if "Overtime Hours" in df:
        df.loc[df["Overtime Hours"]<0,"Overtime Hours"]=pd.NA

    return df