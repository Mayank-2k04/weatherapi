import time
import numpy as np
from flask import Flask, render_template
import pandas as pd
from pandas.core.methods.to_dict import to_dict

app = Flask(__name__)


@app.route("/")
def home():
    station_list = pd.read_csv("weather_data/stations.txt", skiprows=17)
    station_list = station_list[['STAID','STANAME                                 ']]
    return render_template("home.html",data=station_list.to_html())


@app.route("/api/v1/<station>")
def alltime(station):
    data = pd.read_csv(f"weather_data/TG_STAID{str(station).zfill(6)}.txt", skiprows=20, parse_dates=['    DATE'])
    data["   TG"] = data["   TG"].mask(data["   TG"] == -9999, np.nan) / 10
    return data.to_dict(orient="records")


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    try:
        data = pd.read_csv(f"weather_data/TG_STAID{str(station).zfill(6)}.txt",skiprows=20, parse_dates=['    DATE'])
        f = "%Y%m%d"
        conv = time.strptime(date,f)
        date = time.strftime("%Y-%m-%d",conv)

        temperature = data.loc[data['    DATE'] == date]['   TG'].squeeze()
        temperature = np.nan if temperature == -9999 else temperature/10
        return {"station": station,
                "date": date,
                "temperature": temperature
                }
    except FileNotFoundError as f:
        return "Station not found"


@app.route("/api/v1/yearly/<station>/<year>")
def get_yearly(station, year):
    try:
        data = pd.read_csv(f"weather_data/TG_STAID{str(station).zfill(6)}.txt",skiprows=20)
        data["    DATE"] = data["    DATE"].astype(str)
        data["   TG"] = data["   TG"].mask(data["   TG"] == -9999, np.nan)
        result = data[data["    DATE"].str.startswith(str(year))]

        return result.to_dict(orient="records")



    except FileNotFoundError as f:
        return "Station not found"

if __name__ == "__main__":
    app.run(debug=True)
