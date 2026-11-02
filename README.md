# Nintendo Video Game Sales Analytics

An end-to-end data analytics and cloud ETL project using **AWS S3, Python, pandas, boto3, PostgreSQL, Docker, SQLAlchemy, SQL, and Tableau** to analyze historical video game sales and Nintendo's performance in the global gaming market.

## Project Overview

This project implements a cloud-integrated data pipeline that extracts video game sales data from Amazon S3, cleans and validates records using Python, stores transformed data in S3, and loads it into a PostgreSQL database for analysis.

An interactive Tableau dashboard visualizes Nintendo's sales performance, regional market trends, top-selling games, and historical sales patterns.

## Technology Stack

- **Cloud:** Amazon Web Services (AWS S3, IAM)
- **Programming:** Python, pandas, boto3
- **Database:** PostgreSQL 17, SQLAlchemy, psycopg2
- **Infrastructure:** Docker, Docker Compose
- **Analytics:** SQL
- **Visualization:** Tableau
- **Version Control:** Git, GitHub

## ETL Architecture

```text
Amazon S3 (raw/vgsales.csv)
            |
            v
Python + boto3 (Extract)
            |
            v
pandas (Clean and Validate)
            |
            v
Amazon S3 (cleaned/vgsales_cleaned.csv)
            |
            v
Python + SQLAlchemy
            |
            v
PostgreSQL (Docker)
            |
            v
SQL Analysis + Tableau Dashboard
```

The transformation and database-loading stages run locally. Amazon S3 provides cloud-based storage for the raw and cleaned datasets.

## Data Processing

The original dataset contained **16,598 video game sales records**.

The cleaning pipeline:

1. Removed 271 records with missing release years.
2. Replaced missing publisher names with `Unknown`.
3. Converted release years to integers.
4. Checked for duplicate records.
5. Validated regional sales totals against reported global sales.
6. Checked for negative sales values.

**Final dataset: 16,327 cleaned records.**

The pipeline also identified 10 records with regional-versus-global sales differences above the selected validation threshold.

## Cloud ETL Implementation

### 1. S3 Extraction and Transformation

`s3_etl.py` downloads the raw CSV from Amazon S3 using boto3, processes it with pandas, and uploads the cleaned CSV to S3.

### 2. PostgreSQL Loading

`load_s3_to_postgres.py` retrieves the cleaned CSV directly from S3 and loads it into PostgreSQL using SQLAlchemy.

The script verifies data integrity by comparing the source and database row counts.

**Validated result: 16,327 S3 records and 16,327 PostgreSQL records.**

### 3. AWS Security

The project uses a dedicated IAM user with a custom least-privilege policy for accessing the required S3 objects.

AWS credentials are stored locally outside the repository and are not included in source code.

## SQL Analysis

Seven SQL analyses examine:

- Publisher sales performance
- Regional sales distribution
- Nintendo's best-selling games
- Video game platform rankings
- Historical sales trends
- Nintendo's performance relative to competitors

SQL scripts are available in the `sql/` directory.

## Tableau Dashboard

The interactive Tableau dashboard includes four visualizations:

1. Nintendo versus competitors
2. Regional sales patterns
3. Top-selling games
4. Sales by release year

A dynamic year filter allows exploration across different release periods.

The packaged Tableau workbook is available in the `dashboard/` directory.

## Project Structure

```text
Game: Tebalu Analysis/
├── raw/
│   └── vgsales.csv
├── cleaned/
│   └── vgsales_cleaned.csv
├── dashboard/
│   └── Nintendo_Game_Sales_Analytics.twbx
├── sql/
│   ├── create_tables.sql
│   └── sales_analysis.sql
├── data_cleaning.ipynb
├── s3_etl.py
├── load_s3_to_postgres.py
├── load_to_postgres.py
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Running the Pipeline

**Prerequisites:** Python, PostgreSQL through Docker Compose, an AWS S3 bucket containing the raw dataset, and appropriately scoped AWS credentials.

Install the Python dependencies:

```bash
pip install boto3 pandas sqlalchemy psycopg2-binary python-dotenv
```

Configure AWS credentials using a local AWS credentials profile, and configure the PostgreSQL environment variables in a local `.env` file.

Start the database:

```bash
docker compose up -d
```

Run the cloud transformation pipeline:

```bash
python s3_etl.py
```

Load the cleaned S3 data into PostgreSQL:

```bash
python load_s3_to_postgres.py
```

**Note:** The database loader replaces the existing rows in the target table. The PostgreSQL schema must already exist before running it. The example scripts use the project author's S3 bucket configuration; other users should update the bucket settings for their own AWS environment.

## Results

- Processed 16,598 raw records.
- Produced 16,327 cleaned records.
- Successfully transferred data between AWS S3 and PostgreSQL.
- Verified matching S3 and PostgreSQL row counts.
- Developed seven SQL analyses and four Tableau visualizations.

## Dataset

Historical Video Game Sales dataset, originally published on Kaggle. Sales figures are reported in millions of units. The dataset represents historical reported sales rather than current Nintendo sales figures.
