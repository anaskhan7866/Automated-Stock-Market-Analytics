# 📈 Automated Stock Market Analytics

An end-to-end automated stock market analytics pipeline built using **Python, Alpha Vantage API, MySQL, Power BI, GitHub, and GitHub Actions**.

The project automatically extracts stock market data, transforms and validates it using Python, stores it in MySQL, and presents analytical insights through interactive Power BI dashboards.

---

## 🚀 Project Overview

This project demonstrates a complete data analytics pipeline from data extraction to business intelligence reporting.

The pipeline follows:

```text
Alpha Vantage API
       ↓
   Python ETL
       ↓
Pandas Transformation
       ↓
     MySQL
       ↓
    Power BI
```
🏗️ Project Architecture

                    ┌──────────────────────┐
                    │   Alpha Vantage API  │
                    │   Stock Market Data  │
                    └──────────┬───────────┘
                               │
                               │ API Request
                               ▼
                    ┌──────────────────────┐
                    │      Python ETL      │
                    │                      │
                    │  Extract             │
                    │  Transform           │
                    │  Validate            │
                    │  Load                │
                    └──────────┬───────────┘
                               │
                               │ Clean Data
                               ▼
                    ┌──────────────────────┐
                    │        MySQL         │
                    │                      │
                    │   stock_prices       │
                    │   stock_analytics    │
                    └──────────┬───────────┘
                               │
                               │ Database Connection
                               ▼
                    ┌──────────────────────┐
                    │       Power BI       │
                    │                      │
                    │  Market Overview     │
                    │  Stock Performance   │
                    │  Risk & Trading      │
                    └──────────────────────┘


                    ┌──────────────────────┐
                    │    GitHub Actions    │
                    │                      │
                    │  Automated ETL       │
                    └──────────┬───────────┘
                               │
                               ▼
                          Python ETL


🛠️ Technologies Used

| Technology     | Purpose                        |
| -------------- | ------------------------------ |
| Python         | ETL development                |
| Pandas         | Data transformation            |
| Requests       | API communication              |
| Alpha Vantage  | Stock market data source       |
| MySQL          | Data storage and SQL analytics |
| Power BI       | Data visualization             |
| Git            | Version control                |
| GitHub         | Source code hosting            |
| GitHub Actions | ETL automation                 |
| python-dotenv  | Environment configuration      |


📊 Stocks Tracked

The pipeline currently tracks:

RELIANCE.BSE
TCS.BSE
INFY.BSE
IBM

Additional stocks can be added easily in src/etl.py.

🔄 ETL Pipeline
1. Extract

The Python ETL sends requests to the Alpha Vantage API to retrieve daily stock market data.

Example parameters:
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": symbol,
    "outputsize": "compact",
    "apikey": API_KEY
}
The API returns stock information in JSON format.

2. Transform

The JSON response is converted into a Pandas DataFrame.

The following fields are extracted:

symbol
date
open
high
low
close
volume

The transformation process includes:

Converting dates into proper date format
Converting prices into numeric values
Converting volume into numeric values
Handling invalid values
Removing invalid required records
Validating the API response

3. Load

The transformed data is loaded into MySQL.

The ETL checks whether a record with the same:
symbol + date
already exists.

This prevents duplicate historical records from being inserted.


🗄️ Database

stock_prices

The main table stores daily stock-price data.

stock_prices
│
├── symbol
├── date
├── open
├── high
├── low
├── close
└── volume
Each row represents one stock for one trading date.

stock_analytics

The analytics table contains calculated stock metrics used for analysis and Power BI.

Possible metrics include:

Daily Return
Cumulative Return
Moving Average
Volatility
Trading Volume
Price Range
Stock Performance

📈 Power BI Dashboard

The project contains three main dashboard sections.

1. Market Overview

Provides a high-level overview of the tracked stocks.

Includes:

Current Price
Average Price
Trading Volume
Overall Performance
Market Trends

2. Stock Performance

Used to analyze and compare individual stocks.

Includes:

Price trends
Stock comparison
Daily returns
Historical performance
Trading volume

3. Risk & Trading

Focuses on stock risk and trading behavior.

Includes:

Volatility
Daily Returns
Trading Volume
Price Range
Risk comparison

⚙️ Automation
The ETL pipeline is automated using GitHub Actions.

The workflow is located at:
.github/
└── workflows/
    └── etl.yml

The workflow performs:
GitHub Actions
      ↓
Checkout Repository
      ↓
Setup Python
      ↓
Install Dependencies
      ↓
Load Configuration
      ↓
Run ETL
      ↓
Alpha Vantage API
      ↓
MySQL

The workflow can also be manually triggered for testing.

🔐 Configuration & Security
Sensitive credentials are not hard-coded in the Python source code.

The project uses environment variables.

Example:

ALPHA_VANTAGE_API_KEY=your_api_key


DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=stock_market

A configuration template is provided in:

.env.example

The real .env file is excluded from Git using .gitignore.

GitHub Actions uses repository secrets for sensitive credentials.

📁 Project Structure
Automated-Stock-Market-Analytics/
│
├── .github/
│   └── workflows/
│       └── etl.yml
│
├── Detailed/
│   ├── Stock_Market_Analytics_ETL_Line_by_Line_Explanation.pdf
│   ├── Stock_Market_Analytics_Interview_QA_Complete.pdf
│   └── Stock_Market_Analytics_Project_Architecture.pdf
│
├── src/
│   ├── etl.py
│   └── test_stocks.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

🐍 ETL Script

The main ETL script is:

src/etl.py

The script contains the following stages:

Configuration
      ↓
Logging
      ↓
Configuration Validation
      ↓
API Extraction
      ↓
Data Transformation
      ↓
MySQL Connection
      ↓
Duplicate Check
      ↓
Database Insert
      ↓
ETL Completion

📝 Logging

The ETL uses Python's logging module to monitor execution.

Example:

2026-08-18 02:00:01 - INFO - ETL PROCESS STARTED
2026-08-18 02:00:02 - INFO - Connected to MySQL successfully.
2026-08-18 02:00:02 - INFO - Processing RELIANCE.BSE
2026-08-18 02:00:03 - INFO - RELIANCE.BSE: extracted 100 rows
2026-08-18 02:00:04 - INFO - 3 new records inserted.

Logging helps monitor:

API failures
API rate limits
Database errors
Number of extracted records
Number of inserted records
ETL execution status

🛡️ Error Handling

The ETL handles different types of failures.

API Request Errors
except requests.RequestException:

Handles network and HTTP request-related problems.

Invalid JSON
except ValueError:

Handles invalid API responses.

MySQL Errors
except mysql.connector.Error:

Handles database-related errors.

The pipeline also checks Alpha Vantage responses for:

Rate-limit messages
Information messages
API errors
Unexpected responses

🧪 Testing

Basic tests are located in:

src/test_stocks.py

The project can be tested locally using:

python src/test_stocks.py

GitHub Actions also validates the Python environment and ETL syntax.

▶️ Running Locally
1. Clone the repository
git clone https://github.com/anaskhan7866/Automated-Stock-Market-Analytics.git
cd Automated-Stock-Market-Analytics
2. Create a virtual environment
Windows
python -m venv venv

Activate it:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

ALPHA_VANTAGE_API_KEY=your_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=stock_market

5. Run the ETL
python src/etl.py

📚 Detailed Documentation

Detailed project documentation is available in the Detailed/ directory.

It includes:

ETL line-by-line explanation
Complete project architecture
Interview questions and answers

🚀 Future Improvements

Planned improvements include:

Cloud-hosted MySQL
Automated Power BI refresh
Incremental data loading
Bulk database insertion
Database-level UNIQUE constraints
Retry with exponential backoff
Stronger data-quality validation
Automated unit testing
Centralized logging
Monitoring and alerts
Docker deployment
Cloud deployment
Additional stocks and markets
Intraday stock data
Advanced financial analytics
🎯 Key Learning Outcomes

This project demonstrates practical experience with:

Python
API integration
Functions
Exception handling
Environment variables
Logging
Pandas
ETL development
SQL / MySQL
Database connectivity
SQL queries
Transactions
Parameterized queries
Duplicate prevention
Data storage
Data Analytics
Data cleaning
Stock returns
Moving averages
Volatility
Performance comparison
Power BI
Dashboard development
KPIs
Interactive filtering
Data visualization
Business insights
Automation / DevOps
Git
GitHub
GitHub Actions
Scheduled workflows
Environment configuration
Secrets management
👨‍💻 Author
Anas Khan

Data Analytics | Python | SQL | Power BI

📌 Project Goal

The goal of this project is to demonstrate how raw external stock-market data can be transformed into a reliable and automated analytics pipeline and presented through an interactive business intelligence dashboard.

The project combines:

API Integration
      +
Python ETL
      +
Data Engineering
      +
MySQL
      +
Power BI
      +
Automation

into one complete end-to-end analytics project.

🔗 Data Source

Stock market data is provided by:

Alpha Vantage

https://www.alphavantage.co/



### One thing before you commit it


Your repository is **currently named `Stock-Market-Analytics`**, while this README assumes the final name will be:


```text
Automated-Stock-Market-Analytics




