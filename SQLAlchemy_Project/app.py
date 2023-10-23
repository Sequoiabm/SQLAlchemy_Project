# import dependancies:
# datetime, numpy, sqlalchemy (base, sesison, create_engine, func), and Flask 
import datetime as dt
import numpy as np 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Create a database connection to the "hawaii.sqlite" database 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database tables into python classes
# prepare the base and map classes to tables
Base = automap_base()
Base.prepare(engine)

# Create classes for each table 
Measurement = Base.classes.measurement 
Station = Base.classes.station

# start a new session to interact with the database 
session = Session(engine)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Create a Flask App 
app = Flask(__name__)


# ----------------------------------------------------------------------
# Define App Routes: 
# ----------------------------------------------------------------------

# Define the root route
# This provides an overview of available routes
@app.route("/")
def welcome():
    return (

        f"Welcome to the hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p> 'start' and 'end' date should be in the format MMDDYYY.</p>"

    )

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Define a route to retrieve precipitation data for the last year
@app.route("/api/v1.0/precipitation")
def precipitation():
     # Calculate the date one year ago from the current date
    prev_year = dt.date(2017, 8 ,23) - dt.timedelta(days=365)

    # Query precipitation data for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    session.close()

     # Convert the query results into a dictionary
    precip = { date: prcp for date, prcp in precipitation }
    return jsonify(precip)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Define a route to retrieve a list of weather stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()

    # Flatten the results into a list
    station = list(np.ravel(results))
    return jsonify(stations=station)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Define a route to retrieve temperature observations for the last year
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

     # Query temperature observations for the last year for a specific station (USC00519281)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    session.close()

    # Convert the results into a list
    print()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Define a route to retrieve temperature statistics for a specific date range
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

     # If no end date is specified, retrieve temperature stats from the start date
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        session.close()

        # Convert the results into a list
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    # Retrieve temperature stats for a specific date range
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    print(start)
    print(end)
    print(results)
    
    session.close()

    # Convert the results into a list
    temps = list(np.ravel(results))

    return jsonify(temps=temps)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Run the app in debug mode if this script is executed
if __name__ == "__main__":
    app.run(debug=True)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------