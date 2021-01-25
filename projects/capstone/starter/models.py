import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

#database_filename = "database.db"  
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

database_name = "capstone"
database_path = "postgresql://{}/{}".format('postgres:admin@localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    #app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #migrate = Migrate(app, db)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Actor
a persistent actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    name = Column(String(80), unique=False)
    age = Column(String(2), unique=False)
    gender =  Column(String(6), nullable=False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()
    '''
    def insert(self):
        print("here")
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.title = 'Black Coffee'
            actor.update()
    '''
    def update(self):
        db.session.commit()
'''
Movie
a persistent actor entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    release_date =  Column(String(20), nullable=False)


    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = actor = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.title = 'Black Coffee'
            actor.update()
    '''
    def update(self):
        db.session.commit()
