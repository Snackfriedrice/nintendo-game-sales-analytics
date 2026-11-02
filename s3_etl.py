
import boto3
import pandas as pd
from io import BytesIO

# AWS S3 configuration
BUCKET_NAME = "nintendo-game-sales-analytics-633800809769-us-east-2-an"
RAW_KEY = "raw/vgsales.csv"
CLEANED_KEY = "cleaned/vgsales_cleaned.csv"

# Connect to Amazon S3
s3 = boto3.client("s3", region_name="us-east-2")

# Extract: Download raw CSV from S3
response = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=RAW_KEY
)

df = pd.read_csv(BytesIO(response["Body"].read()))

print(f"Successfully extracted {len(df)} rows from Amazon S3!")


# Transform: Clean the raw data

# Remove records with missing release years
df = df.dropna(subset=["Year"]).copy()

# Replace missing publisher names
df["Publisher"] = df["Publisher"].fillna("Unknown")

# Convert release years to integers
df["Year"] = df["Year"].astype(int)

# Validate regional sales totals
df["Calculated_Sales"] = (
    df["NA_Sales"]
    + df["EU_Sales"]
    + df["JP_Sales"]
    + df["Other_Sales"]
)

df["Sales_Difference"] = abs(
    df["Global_Sales"] - df["Calculated_Sales"]
)

# Check for inconsistencies
print("Sales discrepancies:", (df["Sales_Difference"] > 0.010001).sum())

sales_cols = [
    "NA_Sales", "EU_Sales", "JP_Sales",
    "Other_Sales", "Global_Sales"
]

print("Negative sales values:", (df[sales_cols] < 0).sum().sum())
print("Duplicate records:", df.duplicated().sum())

# Remove temporary validation columns
df = df.drop(columns=["Calculated_Sales", "Sales_Difference"])

print(f"Transformation complete: {len(df)} cleaned rows!")



# Load: Upload cleaned CSV to Amazon S3

# Convert the cleaned DataFrame to CSV in memory
csv_buffer = df.to_csv(index=False)

# Upload the CSV to the cleaned/ folder in S3
s3.put_object(
    Bucket=BUCKET_NAME,
    Key=CLEANED_KEY,
    Body=csv_buffer.encode("utf-8"),
    ContentType="text/csv"
)

print(f"Successfully uploaded {len(df)} cleaned rows to S3!")
print(f"S3 location: s3://{BUCKET_NAME}/{CLEANED_KEY}")
