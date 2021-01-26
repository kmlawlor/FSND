import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
'''
#db_drop_and_create_all()

## ROUTES
@app.route('/headers')
def headers():
    # @TODO unpack the request header
    auth_header = request.headers.get('Authorization')
    print(auth_header.split(' ')[1])
    return 'not implemented'

'''
Implement the public get actors endpoint
'''
@app.route('/actors')
@requires_auth('get:actors')
def retrieve_actors(payload):
    current_actors = Actor.query.order_by(Actor.id).all()

    if len(current_actors) == 0:
        print("None")
        abort(404)

    print('Actors Retrieved:' + str(len(Actor.query.all()))) 
    actors = []
    strTable = "<table>"
    strTable += "<tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th></tr>"
    for actor in current_actors:
        d = Actor()
        d.id = actor.id
        d.name = actor.name
        d.age = actor.age
        d.gender = actor.gender
        print(d)
        actors.append(d) 
        strTable += "<tr><td>" + str(actor.id) + "</td><td>" + actor.name  + "</td><td>" +  actor.age  + "</td><td>" + actor.gender  + "</td></tr>" 

    strTable += "</table>" 
    return strTable

'''
Implement create actor endpoint
'''
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):   
    new_name = request.form.get('name')
    new_age = request.form.get('age')
    new_gender = request.form.get('gender')

    try:
        print("Trying")
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        print("Still Trying")
        actor.insert()
        print("Tried")

        return actor.name + " added"
    
    except Exception as e:
        print(e)
        abort(422)

'''
Implement update actors endpoint
'''
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def actors_update(payload,actor_id):
    try:
        new_name = request.form.get('name')
        new_age = request.form.get('age')
        new_gender = request.form.get('gender')

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(400)

        print(actor.id)
        actor.name = new_name
        actor.age = new_age
        actor.gender = new_gender
        actor.update()

        #return actor.name + " updated"
        return retrieve_actors() 

    except Exception as e:
        print(e)
        abort(422)
 
'''
Delete endpoint
'''
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload,actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(408)

        actor.delete()

        return retrieve_actors()

    except Exception as e:
        print(e)
        abort(422)


'''
Implement the public get movies endpoint
'''
@app.route('/movies')
@requires_auth('get:movies')
def retrieve_movies(payload):
    current_movies = Movie.query.order_by(Movie.title).all()

    if len(current_movies) == 0:
        abort(414)     

    print('Movies Retrieved:' + str(len(Movie.query.all()))) 
    movies = []
    strTable = "<table>"
    strTable += "<tr><th>ID</th><th>Title</th><th>Date</th></tr>"
    for movie in current_movies:
        d = Movie()
        d.id = movie.id
        d.title = movie.title
        d.release_date = movie.release_date
        movies.append(d) 
        strTable += "<tr><td>" + str(movie.id) + "</td><td>" + movie.title  + "</td><td>" +  movie.release_date  +  "</td></tr>" 

    strTable += "</table>" 
    return strTable
    #return jsonify({"success": True, "code": 200, "movies": movies})

'''
Implement create movie endpoint
'''
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):   
    new_title = request.form.get('title')
    new_release_date = request.form.get('release_date')
 
    try:
        movie = Movie(title=new_title, release_date=new_release_date)
        movie.insert()

        return movie.title + " added"
    
    except Exception as e:
        print(e)
        abort(422)

'''
Implement update movies endpoint
'''
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def movies_update(payload,movie_id):
    try:
        new_title = request.form.get('title')
        new_release_date = request.form.get('release_date')
 
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(400)

        print(movie.id)
        movie.title = new_title
        movie.release_date = new_release_date
        movie.update()

        return retrieve_movies() 

    except Exception as e:
        print(e)
        abort(422)
 
'''
Delete endpoint
'''
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload,movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(408)

        movie.delete()

        return retrieve_movies()

    except Exception as e:
        print(e)
        abort(422)


## ERRORS
'''
Error handlers
'''
@app.errorhandler(422)
def unprocessable(error):
    print(error)
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def no_actors(error):
    return jsonify({
        "success": False,
        "error": 404, 
         "message": "actors not found"
    }), 404

@app.errorhandler(408)
def actor_not_found(error):
    print(error)
    return jsonify({
        "success": False,
        "error":408,
        "message": "Specific actor not found"
    }), 408

@app.errorhandler(414)
def no_actors(error):
    return jsonify({
        "success": False,
        "error": 414, 
         "message": "movies not found"
    }), 414

@app.errorhandler(418)
def actor_not_found(error):
    return jsonify({
        "success": False,
        "error":418,
        "message": "Specific movie not found"
    }), 418
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
