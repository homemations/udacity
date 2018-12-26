"""
    Project Name: Catalog App
    File: views - provides all the HTML endpoints
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask import session as login_session
from sqlalchemy import desc, literal
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from catalog.model import Category, Item, User
from catalog.dbConnect import dbConnect
from catalog.authenticate import getUserID

@app.route('/')
@app.route('/catalog/')
# main site homepage that list out categories links and last 4 items added
def showHome():
    dbSession = dbConnect()
    categorys = dbSession.query(Category).all()
    lastItems = dbSession.query(Item).order_by(desc(Item.id))[0:6]
    dbSession.close()
    return render_template('home.html',
                           categorys=categorys,
                           latestItems=lastItems)

@app.route('/catalog/<categoryName>/items/')
def showItems(categoryName):
    dbSession = dbConnect()
    try:
        category = dbSession.query(Category).filter_by(name=categoryName).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % categoryName)
        return redirect(url_for('showHome'))

    categorys = dbSession.query(Category).all()
    items = (dbSession.query(Item).filter_by(category=category).
             order_by(Item.name).all())
    dbSession.close()
    if not items:
        flash("There are currently no animals in this category.")
    return render_template('items.html',
                           categorys=categorys,
                           category=category,
                           items=items)

@app.route('/catalog/<categoryName>/<itemName>/')
def showItem(categoryName, itemName):
    dbSession = dbConnect()
    try:
        category = dbSession.query(Category).filter_by(name=categoryName).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % categoryName)
        dbSession.close()
        return redirect(url_for('showHome'))

    try:
        item = dbSession.query(Item).filter_by(name=itemName).one()
    except NoResultFound:
        flash("The item '%s' does not exist." % itemName)
        dbSession.close()
        return redirect(url_for('showItems', categoryName=categoryName))

    user = dbSession.query(User).filter_by(id=item.userID).one()
    ownerName = user.name
    ownerEmail = user.email

    categorys = dbSession.query(Category).all()
    dbSession.close()
    return render_template('item.html',
                           categorys=categorys,
                           category=category,
                           item=item,
                           ownerName=ownerName,
                           ownerEmail=ownerEmail)

@app.route('/catalog/myitems/')
# Users items after login
def showMyItems():
    if 'username' not in login_session:
        return redirect('/login')

    userID = getUserID(login_session['email'])

    dbSession = dbConnect()
    categorys = dbSession.query(Category).all()
    items = dbSession.query(Item).filter_by(userID=userID).all()
    dbSession.close()

    if not items:
        flash("You do not have any software development languages in the database.")
        redirect(url_for('showHome'))

    return render_template('myItems.html',
                           categorys=categorys,
                           items=items)

@app.route('/catalog/new/', methods=['GET', 'POST'])
# Create a new language for authenitcated user
def createItem():
    # Must be a logged in user to create new item
    if 'username' not in login_session:
        return redirect('/login')

    dbSession = dbConnect()

    if request.method == 'POST':
        # Make sure that item name does not use the reserved name of items
        if request.form['name'] == "items":
            flash("Error: do not use a language name of 'items', it's a reserved word.")
            return redirect(url_for('showHome'))

        # Make sure that an item name was entered
        if not request.form['name']:
            flash("Error: new language was not created because no name was provided.")
            return redirect(url_for('showHome'))

        # Make sure that item name entered is not already in the DB
        item = dbSession.query(Item).filter(Item.name == request.form['name'])
        alreadyExists = (dbSession.query(literal(True)).
                          filter(item.exists()).scalar())
        if alreadyExists is True:
            flash("Error: There is already a language named '%s' in the database"
                  % request.form['name'])
            dbSession.close()
            return redirect(url_for('showHome'))

        category = (dbSession.query(Category)
                    .filter_by(name=request.form['category']).one())
        newItem = Item(category=category,
                        name=request.form['name'],
                        description=request.form['description'],
                        userID=login_session['userID'])

        dbSession.add(newItem)
        dbSession.commit()

        flash("New language was successfully created!")
        categoryName = category.name
        itemName = newItem.name
        dbSession.close()
        return redirect(url_for('showItem',
                                categoryName=categoryName,
                                itemName=itemName))
    else:
        categorys = dbSession.query(Category).all()

        # See, if any, which category page new item was click on.
        refCategory = None
        if request.referrer and 'catalog' in request.referrer:
            ref_url_elements = request.referrer.split('/')
            if len(ref_url_elements) > 5:
                refCategory = ref_url_elements[4]

        dbSession.close()
        return render_template('itemAdd.html',
                               categorys=categorys,
                               refCategory=refCategory)

@app.route('/catalog/<categoryName>/<itemName>/edit/',
           methods=['GET', 'POST'])
@app.route('/catalog/<itemName>/edit/', methods=['GET', 'POST'])
def editItem(itemName, categoryName=None):
    if 'username' not in login_session:
        flash("Error: You must be logged in to edit a language.")
        return redirect('/login')

    dbSession = dbConnect()

    try:
        item = dbSession.query(Item).filter_by(name=itemName).one()
    except NoResultFound:
        flash("Error: The language name '%s' does not exist." % itemName)
        return redirect(url_for('showHome'))

    if login_session['userID'] != item.userID:
        flash("Error:  You cannot edit a language you did not add.")
        category = dbSession.query(Category).filter_by(id=item.categoryID).one()
        categoryName = category.name
        itemName = item.name
        dbSession.close()
        return redirect(url_for('showItem',
                                categoryName=categoryName,
                                itemName=itemName))

    if request.method == 'POST':
        if request.form['name'] != item.name:
            # Enforce rule that item names are unique
            qry = dbSession.query(Item).filter(Item.name == request.form['name'])
            alreadyExists = (dbSession.query(literal(True)).filter(qry.exists())
                              .scalar())
            if alreadyExists is True:
                original_category = (dbSession.query(Category)
                                     .filter_by(id=item.categoryID).one())
                flash("Error: There is already a language with the name '%s'"
                      % request.form['name'])
                dbSession.close()
                return redirect(url_for('showItems',
                                        categoryName=original_category.name))
            item.name = request.form['name']

        form_category = (dbSession.query(Category)
                         .filter_by(name=request.form['category']).one())
        if form_category != item.category:
            item.category = form_category

        item.description = request.form['description']
        dbSession.add(item)
        dbSession.commit()

        flash("Selected language was successfully edited")
        categoryName = form_category.name
        itemName = item.name
        dbSession.close()
        return redirect(url_for('showItem',
                                categoryName=categoryName,
                                itemName=itemName))
    else:
        categorys = dbSession.query(Category).all()
        dbSession.close()
        return render_template('itemEdit.html',
                               categorys=categorys,
                               item=item)

@app.route('/catalog/<itemName>/delete/', methods=['GET', 'POST'])
def deleteItem(itemName):
    if 'username' not in login_session:
        return redirect('/login')

    dbSession = dbConnect()

    try:
        item = dbSession.query(Item).filter_by(name=itemName).one()
    except NoResultFound:
        flash("Error: The language '%s' does not exist." % itemName)
        dbSession.close()
        return redirect(url_for('showHome'))

    if login_session['userID'] != item.userID:
        flash("Error:  You cannot delete a language you did not add.")
        category = dbSession.query(Category).filter_by(id=item.categoryID).one()
        categoryName = category.name
        itemName = item.name
        dbSession.close()
        return redirect(url_for('showItem',
                                categoryName=categoryName,
                                itemName=itemName))

    if request.method == 'POST':
        dbSession.delete(item)
        dbSession.commit()
        category = dbSession.query(Category).filter_by(id=item.categoryID).one()
        flash("'%s' language was successfully deleted!" %itemName)
        categoryName = category.name
        dbSession.close()
        return redirect(url_for('showItems', categoryName=categoryName))
    else:
        categorys = dbSession.query(Category).all()
        dbSession.close()
        return render_template('itemDelete.html',
                               categorys=categorys,
                               item=item)
