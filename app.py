import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from config import database_key

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine(database_key)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Visitation = Base.classes.visitation

# 1. import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Visitation).all()
    session.close()
    
    cols = ['park_id', 'state', 'national_park', 'visitation_2022', 'total_recreation_visitor_hours_2022', 'visitation_2021', 'total_recreation_visitor_hours_2021', 'visitation_2020', 'total_recreation_visitor_hours_2020']
    result = [{col: getattr(d, col) for col in cols} for d in results]
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(debug=True)
