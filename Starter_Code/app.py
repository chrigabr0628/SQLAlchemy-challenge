from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

Base.classes.keys()


Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#################################################
# Flask Routes
#################################################

# Create homepage

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Anlysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[start]/[end]<br/>"
    )

# Create all available routes 

@app.route("/api/v1.0/precipitation")
def precipitation():
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_score = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prior_year).all()
    precip = {date: prcp for date, prcp in prcp_score}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start='06-01-2017',end=None):
    start = dt.datetime.strptime(start, "%m-%d-%Y")
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if end:
        end = dt.datetime.strptime(end, "%m-%d-%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)    


if __name__ == "__main__":
    app.run(debug=True)