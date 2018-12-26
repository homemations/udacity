"""
    Project Name: Catalog App
    File: Authenticate enables UAM Facebook Oauth
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
# Helper Libraries
import random, string

# Flask Libraries
from flask import make_response
from flask import session as login_session
from flask import render_template, request, redirect, url_for, flash

# OAUTH Libraries
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

# WEB Libraries
import json
import httplib2
import requests

from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from catalog.model import User, Category
from catalog.dbConnect import dbConnect


@app.route('/login')
# Login screen for user maintenance
def showLogin():
    # Create a state token to prevent request forgery.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    dbSession = dbConnect()
    categorys = dbSession.query(Category).all()
    dbSession.close()

    return render_template('login.html', STATE=state, categorys=categorys)

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data

    # Exchange client token for long-lived server-side token
    fb_client_secrets_file = (app.config['OAUTH_SECRETS_LOCATION'] +
                              'fbClientSecrets.json')
    app_id = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_id']
    app_secret = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.12/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    # Use token to get user info from API.
    url = 'https://graph.facebook.com/v2.12/me?%s&fields=name,id,email' % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to proplerly
    # logout, let's strip out the information before the equals sign in
    # our token.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = ('https://graph.facebook.com/v2.12/me/picture?%s&redirect=0'
           '&height=200&width=200') % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # Check if the user exists in the database. If not create a new user.
    userID = getUserID(login_session['email'])
    if userID is None:
        userID = create_user()
    login_session['userID'] = userID

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def fbdisconnect():
    facebook_id = login_session['facebook_id']

    # The access token must be included to successfully logout.
    access_token = login_session['access_token']

    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)

    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]

    if result == '{"success":true}':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']

        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['userID']
        del login_session['provider']

        flash("You have successfully been logged out.")
        return redirect(url_for('showHome'))

    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('showHome'))


def createUser():
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session = connect_to_database()
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.close()
    return user.id


def getUserID(email):
    dbSession = dbConnect()
    try:
        user = dbSession.query(User).filter_by(email=email).one()
        dbSession.close()
        return user.id
    except NoResultFound:
        dbSession.close()
        return None
