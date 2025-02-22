import time

import numpy as np
from flask import Flask, render_template
import pandas as pd
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

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

if __name__ == "__main__":
    app.run(debug=True)
