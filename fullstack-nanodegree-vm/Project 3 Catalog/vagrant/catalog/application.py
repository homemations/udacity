"""
    Project Name: Catalog App
    File: Application python entry point.
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
import os.path

from catalog import app
from catalog.model import createDB
from catalog.createSampleDB import dbLoad

if __name__ == '__main__':
    # Application configuration settings
    app.config['dburi'] = 'sqlite:///catalog.db'
    app.config['OAUTH_SECRETS_LOCATION'] = ''

    # Change 'app.secret_key' prior to moving code to prod.
    app.secret_key = 'super_secret_key'  

    # Create a sample database if none present.
    if os.path.isfile('catalog.db') is False:
        createDB(app.config['dburi'])
        dbLoad()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
