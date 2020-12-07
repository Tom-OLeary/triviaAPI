"""
Tom O'Leary
trivia_API __init__.py - Creates app and handles endpoints
Python 3.7
"""

# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# ----------------------------------------------------------------------------#
# Global Variables
# ----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10


# ----------------------------------------------------------------------------#
# Helpers
# ----------------------------------------------------------------------------#
def paginate_questions(request, selection):
    # Paginates the questions to 10 per page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# ----------------------------------------------------------------------------#
# App Config
# ----------------------------------------------------------------------------#
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        # Set up access-control
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    # ----------------------------------------------------------------------------#
    # Categories
    # ----------------------------------------------------------------------------#
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Creates endpoint to handle GET requests for all available categories
        categories = Category.query.all()
        data = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': data
        }), 200

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        # Creates endpoint to handle GET request for questions by category
        selection = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, selection)

        if len(questions) == 0:
            abort(404, 'Invalid category id')

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(selection),
            'current_category': category_id
        }), 200

    # ----------------------------------------------------------------------------#
    # Questions
    # ----------------------------------------------------------------------------#
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        # Creates endpoint to handle GET requests for questions
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories},
            'current_category': None,
            'questions': current_questions,
            'total_questions': len(selection)
        }), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # Creates endpoint to handle the deletion of a question
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            }), 200

        except():
            abort(404)

    @app.route('/questions', methods=['POST'])
    def new_question():
        # Creates endpoint to handle the posting of a new question (requires all fields)
        required = ['question', 'answer', 'category', 'difficulty']
        data = []

        try:
            for item in required:
                data.append(request.json.get(item))

            if any(not x for x in data):
                abort(400, 'Missing required fields')

            entry = Question(*data)
            entry.insert()

            return jsonify({
                'success': True,
                'question': entry.format()
            }), 200
        except():
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search():
        # Creates endpoint to handle searching for a question with any phrase
        try:
            search_item = request.json.get('searchTerm', None)
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_item)))

            questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions)
            }), 200

        except():
            abort(422)

    # ----------------------------------------------------------------------------#
    # Quizzes
    # ----------------------------------------------------------------------------#
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        # Creates endpoint to handle POST request to initiate the quiz game
        try:
            body = request.get_json()

            quiz_category = body.get('quiz_category', None)
            previous_questions = body.get('previous_questions', None)

            if quiz_category is None:
                abort(422)

            quiz_dict = {
                1: quiz_category['id'] == 0 and previous_questions is not None,
                2: quiz_category['id'] == 0 and previous_questions is None,
                3: quiz_category['id'] != 0 and previous_questions is not None,
                4: quiz_category['id'] != 0 and previous_questions is None
            }

            results_dict = {
                1: Question.query.filter(Question.id.notin_(previous_questions)).all(),
                2: Question.query.all(),
                3: Question.query.filter(Question.category == quiz_category['id'],
                                         Question.id.notin_(previous_questions)).all(),
                4: Question.query.filter(Question.category == quiz_category['id']).all()
            }

            keys = list(quiz_dict.keys())
            vals = list(quiz_dict.values())

            option = keys[vals.index(True)]
            result = results_dict.get(option)
            data = random.choice(result) if len(result) > 0 else ''

            return jsonify({
                'success': True,
                'question': data.format()
            }), 200

        except():
            abort(422)

    # ----------------------------------------------------------------------------#
    # Error Handlers
    # ----------------------------------------------------------------------------#
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app