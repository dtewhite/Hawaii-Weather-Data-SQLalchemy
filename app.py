import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

Base = automap_base()

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        "Welcome to your vacation weather analysis<br/>"
        "Routes include:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/start/end<br/>"
        "Note that you must enter the start and end dates as Y-M-D"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    Measurement = Base.classes.measurement
    session = Session(engine)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').\
        order_by(Measurement.date).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    Station = Base.classes.station
    session = Session(engine)
    stations = session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    Measurement = Base.classes.measurement
    session = Session(engine)
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def vacation(start=None, end=None):
    Measurement = Base.classes.measurement
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        date_temp = session.query(*sel).filter(Measurement.date >= start).all()
        return jsonify(date_temp)
    
    date_temp = session.query(*sel).filter(Measurement.date >= start).\
        filter(Measurement.date < end).all()
    return jsonify(date_temp)
    

if __name__ == '__main__':
    app.run()