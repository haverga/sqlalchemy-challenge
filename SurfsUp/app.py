from flask import Flask, jsonify

# Import dependencies for data analysis (you can reuse your existing code here)
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt 

# Create a Flask app
app = Flask(__name__)

# Create a connection to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database tables into classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Define the homepage route
@app.route("/")
def home():
    """List all available routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date<br/>"
        "/api/v1.0/start_end_date"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    # Query the last 12 months of precipitation data
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    # Convert the query results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations."""
    # Query the station data and return it as JSON
    session = Session(engine)
    station_data = session.query(Station.station, Station.name).all()
    session.close()
    
    station_list = [{"Station": station, "Name": name} for station, name in station_data]
    
    return jsonify(station_list)

# Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station in the last 12 months."""
    # Query the most active station based on the number of temperature observations
    session = Session(engine)
    station_counts = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()

    # Get the most active station ID
    most_active_station_id = station_counts[0][0]

    # Query the last 12 months of temperature observation data for the most active station
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = (dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    # Convert the query results to a list of dictionaries
    temperature_list = [{"Date": date, "Temperature": tobs} for date, tobs in temperature_data]
    
    return jsonify(temperature_list)

@app.route("/api/v1.0/start_date/<start_date>")
def start_date(start_date):
    session = Session(engine)
    temperature_stats = session.query(
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()
    session.close()
    
    if not temperature_stats[0][0]:
        return jsonify({"error": f"No temperature data found after {start_date}"})
    
    temperature_stats_json = {
        "Minimum Temperature": temperature_stats[0][0],
        "Maximum Temperature": temperature_stats[0][1],
        "Average Temperature": temperature_stats[0][2]
    }
    
    return jsonify(temperature_stats_json)

# Define the start and end date route
@app.route("/api/v1.0/start_end_date/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    """Return the temperature statistics for a given date range."""
    # Add your code to calculate temperature statistics and return them as JSON
    session = Session(engine)
    temperature_stats = session.query(
        func.min(Measurement.tobs), 
        func.max(Measurement.tobs), 
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    
    # Convert the query results to a JSON response
    temperature_stats_json = {
        "Minimum Temperature": temperature_stats[0][0],
        "Maximum Temperature": temperature_stats[0][1],
        "Average Temperature": temperature_stats[0][2]
    }
    
    return jsonify(temperature_stats_json)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
