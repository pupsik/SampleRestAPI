# import sys

# sys.path.insert(0, "//home/rita/Desktop/local/AirBnB-api")

import datetime
import json
import os
from datetime import date, datetime
from typing import Dict

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.automap import automap_base

from fast_api.v1.populate.loader import CSVLoader
from fast_api.v1.settings import ENGINE

FILE_PATH = filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "airbnb_nyc_clean.csv"
)


column_types = {
    "id": int,
    "name": str,
    "host_id": int,
    "host_identity_verified": bool,
    "host_name": str,
    "neighbourhood_group": str,
    "neighbourhood": str,
    "lat": float,
    "long": float,
    "instant_bookable": bool,
    "cancellation_policy": str,
    "room_type": str,
    "construction_year": int,
    "price": int,
    "service_fee": int,
    "minimum_nights": int,
    "number_of_reviews": int,
    "last_review": str,
    "reviews_per_month": float,
    "review_rate_number": int,
    "calculated_host_listings_count": int,
    "availability_365": int,
    "house_rules": str,
}


def populate_database() -> None:
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".db.lock")
    if os.path.exists(filepath):
        return "Database is already populated. Skipping"

    datasets = prepare_datasets()
    truncate_db(ENGINE)
    # Write resulting datasets to database
    for name, df in datasets.items():
        df.to_sql(name, ENGINE, if_exists="append", index=False)
    message = f"Update completed at {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"
    with open(filepath, "w+") as f:
        json.dump(message, f)
    return message


def prepare_datasets() -> Dict[str, pd.DataFrame]:
    # Load data from CSV
    loader = CSVLoader(file_path=FILE_PATH, column_types=column_types)
    data = loader.load()

    # Normalize the data
    cancellation_policy = pd.DataFrame(
        [
            (i + 1, value)
            for i, value in enumerate(
                list(set([row["cancellation_policy"] for row in data]))
            )
        ],
        columns=["cancellation_policy_id", "cancellation_policy_name"],
    )

    room_type = pd.DataFrame(
        [
            (i + 1, value)
            for i, value in enumerate(list(set([row["room_type"] for row in data])))
        ],
        columns=["room_type_id", "room_type_name"],
    )

    unique_host_ids = set()
    filtered_data = []

    for row in data:
        host_id = row["host_id"]

        if host_id not in unique_host_ids:
            unique_host_ids.add(host_id)

            filtered_data.append(
                {
                    col: row[col]
                    for col in ["host_id", "host_identity_verified", "host_name"]
                }
            )
    host = pd.DataFrame(filtered_data)

    df = (
        pd.DataFrame(data)
        .merge(
            cancellation_policy,
            left_on="cancellation_policy",
            right_on="cancellation_policy_name",
            how="inner",
        )
        .merge(room_type, left_on="room_type", right_on="room_type_name", how="inner")
    )
    df["last_review"] = pd.to_datetime(df["last_review"], format="%Y-%m-%d")
    excluded_columns = [
        "room_type",
        "room_type_name",
        "cancellation_policy",
        "cancellation_policy_name",
        "host_identity_verified",
        "host_name",
    ]
    selected_columns = [col for col in df.columns if col not in excluded_columns]

    listings = df[selected_columns]
    return {
        "tbl_pl_cancellation_policy": cancellation_policy,
        "tbl_pl_room_type": room_type,
        "tbl_host": host,
        "tbl_listings": listings,
    }


def truncate_db(engine):
    Base = automap_base()
    Base.prepare(autoload_with=engine)

    con = engine.connect()
    trans = con.begin()

    # Now clean up the tables
    for table in Base.metadata.tables.keys():
        if table.startswith("tbl_"):
            con.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
    trans.commit()
