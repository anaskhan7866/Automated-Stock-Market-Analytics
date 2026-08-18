import os
import time
import logging
import requests
import pandas as pd
import mysql.connector
from dotenv import load_dotenv


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "stock_market")

API_URL = "https://www.alphavantage.co/query"

STOCKS = [
    "RELIANCE.BSE",
    "TCS.BSE",
    "INFY.BSE",
    "IBM"
]

# Alpha Vantage free API:
# Keep requests separated to avoid rate-limit problems.
REQUEST_DELAY = 10


# ============================================================
# 2. LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# 3. VALIDATE CONFIGURATION
# ============================================================

if not API_KEY:
    raise ValueError(
        "ALPHA_VANTAGE_API_KEY is missing from the .env file."
    )

if not DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD is missing from the .env file."
    )


# ============================================================
# 4. EXTRACT DATA FROM ALPHA VANTAGE
# ============================================================

def extract_stock_data(symbol):

    logger.info(f"Requesting data for {symbol}")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        logger.error(
            f"HTTP error for {symbol}: {e}"
        )

        return None

    except ValueError:

        logger.error(
            f"Invalid JSON response for {symbol}"
        )

        return None


    # --------------------------------------------------------
    # Check Alpha Vantage response
    # --------------------------------------------------------

    if "Time Series (Daily)" not in data:

        if "Note" in data:

            logger.warning(
                f"API rate limit reached for {symbol}: "
                f"{data['Note']}"
            )

        elif "Information" in data:

            logger.warning(
                f"API information for {symbol}: "
                f"{data['Information']}"
            )

        elif "Error Message" in data:

            logger.error(
                f"API error for {symbol}: "
                f"{data['Error Message']}"
            )

        else:

            logger.error(
                f"Unknown API response for {symbol}: {data}"
            )

        return None


    # --------------------------------------------------------
    # Convert API response to DataFrame
    # --------------------------------------------------------

    time_series = data["Time Series (Daily)"]

    records = []

    for date, values in time_series.items():

        records.append({
            "symbol": symbol,
            "date": date,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"]
        })

    df = pd.DataFrame(records)

    # --------------------------------------------------------
    # Data types
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(df["date"]).dt.date

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid rows

    df = df.dropna(
        subset=[
            "symbol",
            "date",
            "close"
        ]
    )

    logger.info(
        f"{symbol}: extracted {len(df)} rows"
    )

    return df


# ============================================================
# 5. MYSQL CONNECTION
# ============================================================

def create_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        logger.info(
            "Connected to MySQL successfully."
        )

        return connection

    except mysql.connector.Error as e:

        logger.error(
            f"MySQL connection failed: {e}"
        )

        return None


# ============================================================
# 6. INSERT ONLY NEW RECORDS
# ============================================================

def insert_new_records(connection, df):

    if df is None or df.empty:

        logger.warning(
            "No data to insert."
        )

        return 0


    cursor = connection.cursor()

    insert_query = """
        INSERT INTO stock_prices
        (
            symbol,
            date,
            open,
            high,
            low,
            close,
            volume
        )
        SELECT
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        WHERE NOT EXISTS (
            SELECT 1
            FROM stock_prices
            WHERE symbol = %s
              AND date = %s
        )
    """

    inserted = 0

    for _, row in df.iterrows():

        values = (
            row["symbol"],
            row["date"],
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            int(row["volume"]),

            # duplicate check
            row["symbol"],
            row["date"]
        )

        try:

            cursor.execute(
                insert_query,
                values
            )

            if cursor.rowcount > 0:
                inserted += 1

        except mysql.connector.Error as e:

            logger.error(
                f"Insert failed for "
                f"{row['symbol']} "
                f"{row['date']}: {e}"
            )


    connection.commit()

    cursor.close()

    logger.info(
        f"{inserted} new records inserted."
    )

    return inserted


# ============================================================
# 7. MAIN ETL PROCESS
# ============================================================

def main():

    logger.info(
        "========== ETL PROCESS STARTED =========="
    )

    connection = create_connection()

    if connection is None:

        logger.error(
            "Stopping ETL because MySQL connection failed."
        )

        return


    total_inserted = 0

    try:

        for index, symbol in enumerate(STOCKS):

            logger.info(
                f"Processing {symbol}"
            )

            df = extract_stock_data(symbol)

            if df is not None:

                inserted = insert_new_records(
                    connection,
                    df
                )

                total_inserted += inserted


            # ------------------------------------------------
            # Wait before next API request
            # ------------------------------------------------

            if index < len(STOCKS) - 1:

                logger.info(
                    f"Waiting {REQUEST_DELAY} seconds "
                    f"before next API request..."
                )

                time.sleep(REQUEST_DELAY)


    finally:

        connection.close()

        logger.info(
            "MySQL connection closed."
        )


    logger.info(
        f"Total new records inserted: {total_inserted}"
    )

    logger.info(
        "========== ETL PROCESS COMPLETED =========="
    )


# ============================================================
# 8. RUN
# ============================================================

if __name__ == "__main__":
    main()