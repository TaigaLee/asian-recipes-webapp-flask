import os
from peewee import *
import datetime

from flask_login import UserMixin

from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('recipes.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE

class Recipe(Model):
    name = CharField()
    poster = ForeignKeyField(User, backref='recipes')
    origin = CharField()
    ingredients = TextField()
    instructions = TextField()
    image = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([Recipe, User], safe=True)
    print("Connected to database and created tables")

    DATABASE.close()
