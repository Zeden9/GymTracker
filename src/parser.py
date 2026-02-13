import re
from datetime import datetime

import pandas as pd

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


raw_df = create_df("data/raw/klata_plecy.txt")
print(raw_df.head())
