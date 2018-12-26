"""
    Project Name: Catalog App
    File: __Init__ initializes app.
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
from flask import Flask

# Initialise the Flask app object
app = Flask(__name__)

import catalog.apis
import catalog.views
import catalog.authenticate


