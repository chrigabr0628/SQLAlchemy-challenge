# Import the dependencies.

import pandas as pd
import numpy as np 
import  matplotlib.pyplot as plt 
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Flask Setup
##########################################
app = Flask(__name__)#######



#################################################
# Database Setup
#################################################
# define engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Routes
##########################################
@app.route("/")
def welcome():
       return (
        f"Welcome to the Climate Analysis App!"
        f"<br/>"
        f"Available Routes:"
        f"<br/>"
        f"/api/v1.0/precipitation"
        f"<br/>"
        f"/api/v1.0/stations"
        f"<br/>"
        f"/api/v1.0/tobs"
        f"<br/>"
        f"/api/v1.0/<start>"
        f"<br/>"
        f"/api/v1.0/<start>/<end>"
        f"<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prior_year_date = last_date - dt.timedelta(days=365)
    data_prcp_score = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prior_year_date).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    previous_year = last_date - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previous_year).all()
    temperatures = list(np.ravel(results))
    return jsonify(temps=temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start='2017-06-01',end='2017-06-30'):
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temperatures = list(np.ravel(results))
        return jsonify(temperatures)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures=temperatures)    


if __name__ == "__main__":
    app.run(debug=True)




    #######
