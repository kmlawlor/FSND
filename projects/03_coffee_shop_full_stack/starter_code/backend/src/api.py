import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
'''
db_drop_and_create_all()

## ROUTES
'''
Implement the public get drinks endpoint
'''
@app.route('/drinks')
@requires_auth('get:drinks')
def retrieve_drinks():
    current_drinks = Drink.query.order_by(Drink.id).all()

    if len(current_drinks) == 0:
        abort(404)

    print('Drinks Retrieved:' + str(len(Drink.query.all())))
    drinks = []
    for drink in current_drinks:
        print(drink.recipe)
        d = Drink()
        d.title = drink.title
        d.recipe = drink.recipe
        drinks.append(d.short())
 
    return jsonify({"success": True, "drinks": drinks}), 200

'''
Implement get drink detail endpoint
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinksdetails_processed(payload):
    current_drinks = Drink.query.order_by(Drink.id).all()

    if len(current_drinks) == 0:
        abort(404)

    print('Drinks Retrieved:' + str(len(Drink.query.all())))
    drinks = []
    for drink in current_drinks:
        print(drink.recipe)
        d = Drink()
        d.title = drink.title
        d.recipe = drink.recipe
        drinks.append(d.long())
 
    return jsonify({"success": True, "code": 200, "drinks": drinks})

'''
Implement create drink endpoint
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():   
    new_title = request.form.get('title')
    new_recipe = json.dumps(request.form.get('recipe'))

    try:
        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()

        return jsonify({"success": True, "drinks": drink.long()}), 200
    
    except:
        abort(422)

'''
Implement update endpoint
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drinks_update(payload, drink_id):
    try:
        body = request.get_json()

        new_title = body.get('title', None)
        new_recipe = json.dumps(body.get('recipe', None))

        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(400)

        drink.title = new_title
        drink.recipe = new_recipe
        drink.update()

        return jsonify({"success": True, "drinks": drink.long()}), 200

    except:
        abort(422)
 
'''
Delete endpoint
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        print("Payload----------->" + str(payload))
        print("DrinkId----------->" + str(drink_id))
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(400)

        drink.delete()

        return retrieve_drinks()

    except:
        abort(422)

## ERRORS
'''
Error handlers
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def no_drinks(error):
    return jsonify({
        "success": False,
        "error": 404, 
         "message": "Drinks not found"
    }), 404

@app.errorhandler(400)
def drink_not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Specific drink not found"
    }), 400
'''
Error handler for AuthError
'''
@app.errorhandler(401)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.code,
        "message": ex.description
    })