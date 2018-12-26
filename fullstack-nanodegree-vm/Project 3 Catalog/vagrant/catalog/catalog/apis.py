"""
    Project Name: Catalog App
    File: createSampleDB creates a new db with sample data
    Author: Stephen Harris
    Created Date:  12/18/2018
"""
from flask import jsonify, redirect, url_for, flash
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from catalog.model import Category, Item
from catalog.dbConnect import dbConnect

@app.route('/catalog/categorys.json/')
def categorys():
    dbSession = dbConnect()
    categories = dbSession.query(Category).all()
    serializeCatergorys = [i.serialize for i in categories]
    dbSession.close()
    return jsonify(Category=serializeCatergorys)

@app.route('/catalog/category/<categoryID>.json/')
def category(categoryID):
    dbSession = dbConnect()
    try:
        category = dbSession.query(Category).filter_by(id=categoryID).one()
    except NoResultFound:
        dbSession.close()
        flash("Error: The category  ID '%s' does not exist." % categoryID)
        return redirect(url_for('showHome'))

    dbSession.close()
    return jsonify(Category=category.serialize)

@app.route('/catalog/categoryname/<categoryName>.json/')
def categoryName(categoryName):
    dbSession = dbConnect()
    try:
        category = dbSession.query(Category).filter_by(name=categoryName).one()
    except NoResultFound:
        dbSession.close()
        flash("Error: The category '%s' does not exist." % categoryName)
        return redirect(url_for('showHome'))

    dbSession.close()
    return jsonify(Category=category.serialize)

@app.route('/catalog/items.json/')
def items():
    dbSession = dbConnect()
    categories = dbSession.query(Category).all()
    serializeCatergoriesItems = [i.categoriesItemsSerialize for i in categories]
    dbSession.close()
    return jsonify(Category=serializeCatergoriesItems)

@app.route('/catalog/item/<itemID>.json/')
def itemID(itemID):
    dbSession = dbConnect()
    try:
        item = dbSession.query(Item).filter_by(id=itemID).one()
    except NoResultFound:
        dbSession.close()
        flash("Error: The item ID '%s' does not exist." % itemID)
        return redirect(url_for('showHome'))

    dbSession.close()
    return jsonify(Item=item.serialize)

@app.route('/catalog/itemname/<itemName>.json/')
def itemName(itemName):
    dbSession = dbConnect()
    try:
        item = dbSession.query(Item).filter_by(name=itemName).one()
    except NoResultFound:
        dbSession.close()
        flash("Error: The item name '%s' does not exist." % itemName)
        return redirect(url_for('showHome'))

    dbSession.close()
    return jsonify(Item=item.serialize)
