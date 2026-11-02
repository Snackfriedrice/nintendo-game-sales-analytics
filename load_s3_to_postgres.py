
import os
from io import BytesIO

import boto3
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv


load_dotenv()

# 1. AWS S3 configuration
BUCKET_NAME = "nintendo-game-sales-analytics-633800809769-us-east-2-an"
CLEANED_KEY = "cleaned/vgsales_cleaned.csv"

# 2. Extract cleaned data directly from S3
s3 = boto3.client("s3", region_name="us-east-2")

response = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=CLEANED_KEY
)

df = pd.read_csv(BytesIO(response["Body"].read()))

print(f"Downloaded {len(df)} cleaned rows from S3!")

# 3. Match PostgreSQL column names
df.columns = df.columns.str.lower()

# 4. Connect to PostgreSQL in Docker

db_url = URL.create(
    "postgresql+psycopg2",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host="localhost",
    port=5434,
    database=os.environ["POSTGRES_DB"],
)


engine = create_engine(db_url)

# 5. Load into the existing PostgreSQL table
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE video_game_sales"))

    df.to_sql(
        "video_game_sales",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

# 6. Verify loaded row count
with engine.connect() as connection:
    row_count = connection.execute(
        text("SELECT COUNT(*) FROM video_game_sales")
    ).scalar_one()

print(f"S3 rows: {len(df)}")
print(f"PostgreSQL rows: {row_count}")

assert row_count == len(df), "Row count mismatch!"

print("S3 to PostgreSQL load completed successfully!")
