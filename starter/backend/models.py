"""
models.py - Connects to db server and initiates database models
"""

from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#
class Question(db.Model):
    """Holds data for Questions"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        """__init for Question class
        Values stored represent the attributes of a Question
        Parameters
        ----------
        question : String
            the question being asked
        answer : String
            the answer to the question
        category : String
            the category of the question
        difficulty : Integer
            the difficulty of the question
        """

        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        """Inserts a database record"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a database record"""
        db.session.commit()

    def delete(self):
        """Deletes a database record"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """Holds data for Category"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        """__init__ for Category class
        Values stored represent the attributes of a Category
        Parameters
        ----------
        type : String
            the category type
        """

        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
