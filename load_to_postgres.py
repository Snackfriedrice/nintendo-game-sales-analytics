
from pathlib import Path
import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 1. Locate the cleaned CSV file
project_dir = Path(__file__).resolve().parent
csv_path = project_dir / "cleaned" / "vgsales_cleaned.csv"

# 2. Read the cleaned dataset
df = pd.read_csv(csv_path)

# 3. Match CSV columns to PostgreSQL table columns
df.columns = df.columns.str.lower()

# 4. Connect to PostgreSQL running in Docker
db_url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER", "game_user"),
    password=os.environ["DB_PASSWORD"],
    host="localhost",
    port=5434,
    database="game_sales",
)

engine = create_engine(db_url)

# 5. Replace existing records without dropping the table
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE video_game_sales"))

    df.to_sql(
        "video_game_sales",
        con=connection,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

# 6. Verify the loaded records
with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM video_game_sales")
    )
    row_count = result.scalar_one()

print(f"CSV rows: {len(df)}")
print(f"PostgreSQL rows: {row_count}")

assert row_count == len(df), "Row count mismatch!"
print("ETL load completed successfully!")
