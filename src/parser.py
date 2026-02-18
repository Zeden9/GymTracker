import glob
import re
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from config import DB_CONFIG

DATE_PATTERN = re.compile(r"\d{2}\.\d{2}\.\d{4}")
SET_PATTERN = re.compile(
    r"(?:(\d+)(?:\s*kg)?\s*x\s*)?(\d+)\s*x\s*(\d+)(?:\s*-\s*(\d+))?"
)


def create_df(file: str) -> pd.DataFrame:
    """
    Parses the workout data from the given file and returns a DataFrame with the date and workout data. # noqa: E501
    Raw txt file contains workout data in a specific format, where each date is followed by lines describing the workout sets performed on that date.
    The function reads the file line by line, identifies lines that contain dates and workout sets, and organizes the data into a structured format.
    Each row in the resulting DataFrame contains a date and a comma-separated string of workout sets performed on that date.
    Args:
        file (str): The path to the input file containing the workout data.
    Returns:
        pd.DataFrame: A DataFrame with two columns: 'date' (datetime) and 'data' (str), where 'data' contains the workout sets performed on that date.
    """  # noqa: E501

    with open(file, "r", encoding="utf-8") as f:
        rows = []
        current_date = None
        current_data = []
        current_set = ""
        for line in f:
            line = line.strip()
            if not line:
                continue

            if DATE_PATTERN.match(line):
                if current_date:
                    rows.append({"date": current_date, "data": ",".join(current_data)})

                current_date = datetime.strptime(line, "%d.%m.%Y")
                current_data = []
            else:
                if SET_PATTERN.search(line):
                    current_set += line + " "
                    current_data.append(current_set.strip())
                    current_set = ""
                else:
                    current_set += line + " "

        if current_date:
            rows.append({"date": current_date, "data": ",".join(current_data)})

    return pd.DataFrame(rows)


def save_to_db(df: pd.DataFrame, db_url: str, table_name: str):
    """
    Saves the given DataFrame to a database table using SQLAlchemy.
    Args:
        df (pd.DataFrame): The DataFrame to be saved to the database.
        db_url (str): The database connection URL (e.g., 'sqlite:///workout_data.db').
        table_name (str): The name of the table where the data will be stored.
    """
    engine = create_engine(db_url)
    df = df.rename(columns={"data": "note_text"})[["note_text"]]

    df.to_sql(table_name, con=engine, if_exists="append", index=False)


files = glob.glob("data/raw/*.txt")

raw_dfs = [create_df(file) for file in files]

# raw_df = create_df("data/raw/klata_plecy.txt")

raw_df = pd.concat(raw_dfs, ignore_index=True)


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:"
    f"{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['dbname']}"
)
save_to_db(raw_df, DATABASE_URL, "raw_notes")
raw_df.to_csv("data/processed/raw_notes.csv", index=False)
# print(raw_df.head())
