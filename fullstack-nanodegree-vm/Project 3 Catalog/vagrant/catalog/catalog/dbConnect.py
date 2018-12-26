"""
    Project Name: Catalog App
    File: ConnectDB 
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
# Import required libraries for db framework
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import catalog app libraries
from catalog import app
from catalog.model import Base

# Connects to the database and returns an sqlalchemy session object.
def dbConnect():
    engine = create_engine(app.config['dburi'])
    Base.metadata.bind = engine
    dbSession = sessionmaker(bind=engine)
    return dbSession()
