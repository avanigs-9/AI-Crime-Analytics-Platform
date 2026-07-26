from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Optional
import random

app = FastAPI(title="Crime Analytics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV
df = pd.read_csv("crime_data.csv")


@app.get("/")
def home():
    return {"message": "Crime Analytics API Running Successfully"}


# Dashboard Stats
@app.get("/api/stats")
def get_stats():
    return {
        "total_crimes": len(df),
        "districts": df["District"].nunique(),
        "crime_types": df["Crime_Type"].nunique(),
        "latest_year": int(df["Year"].max())
    }


# Crime Records
@app.get("/api/crimes")
def get_crimes(
    district: Optional[str] = None,
    crime_type: Optional[str] = None,
    year: Optional[int] = None
):

    filtered_df = df.copy()

    if district:
        filtered_df = filtered_df[
            filtered_df["District"].str.lower() == district.lower()
        ]

    if crime_type:
        filtered_df = filtered_df[
            filtered_df["Crime_Type"].str.lower() == crime_type.lower()
        ]

    if year:
        filtered_df = filtered_df[
            filtered_df["Year"] == year
        ]

    statuses = ["Open", "Solved", "Active"]
    severities = ["Low", "Medium", "High"]

    records = []

    for index, row in filtered_df.iterrows():

        records.append({
            "id": str(index + 1),
            "case_id": f"CR{index+1:03}",

            "crime_type": row["Crime_Type"],
            "area": row["District"],

            "latitude": None,
            "longitude": None,

            "date_time": f"{row['Year']}-01-01T10:00:00",

            "status": random.choice(statuses),
            "severity": random.choice(severities),

            "description": f"{row['Crime_Type']} reported in {row['District']}",

            "created_at": f"{row['Year']}-01-01T10:00:00"
        })

    return records


# Insights
@app.get("/api/insights")
def get_insights():

    highest_district = df.groupby("District")["Cases"].sum().idxmax()
    highest_cases = int(df.groupby("District")["Cases"].sum().max())

    common_crime = df.groupby("Crime_Type")["Cases"].sum().idxmax()

    latest_year = int(df["Year"].max())

    return {
        "highest_crime_district": highest_district,
        "highest_cases": highest_cases,
        "most_common_crime": common_crime,
        "latest_year": latest_year
    }


# Charts
@app.get("/api/chart-data")
def chart_data():

    district_data = (
        df.groupby("District")["Cases"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    crime_type_data = (
        df.groupby("Crime_Type")["Cases"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    yearly_data = (
        df.groupby("Year")["Cases"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "district_data": district_data,
        "crime_type_data": crime_type_data,
        "yearly_data": yearly_data
    }


# Dropdown Filters
@app.get("/api/filters")
def get_filters():
    return {
        "districts": sorted(df["District"].unique().tolist()),
        "crime_types": sorted(df["Crime_Type"].unique().tolist()),
        "years": sorted(df["Year"].unique().tolist())
    }