import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 3

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    cat_pairs = {}
    categories = Category.query.order_by(Category.id).all()
    for category in categories:
      cat_pairs[category.id] = category.type  

    return cat_pairs
   
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'categories': retrieve_categories(),
      'currentCategory': 'All',
      'total_questions': len(Question.query.all())
    }) 
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(400)

      question.delete()

      return retrieve_questions()

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    search = body.get('searchTerm', None)
    print("This is search " + str(search))

    try:
      if search:
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))

        if not questions:
          abort(404)

        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
          abort(404)

        selected = [question.format() for question in questions]

        return jsonify({
          'success': True,
          'questions': current_questions,
          'categories': retrieve_categories(),
          'currentCategory': search,
          'total_questions': len(selected)
        }) 

      else:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category) 
        question.insert()

        return retrieve_questions()

    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_for_category(category_id):
    # shows the questions for the chosen category_id
    questions = Question.query.filter(Question.category == category_id)

    if not questions:
      abort(400)

    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'categories': retrieve_categories(),
      'currentCategory': category_id,
      'total_questions': len(Question.query.all())
    }) 

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    print("HERE")
    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    if quiz_category is None:
      question = Question.query.filter(Question.id == 3).one_or_none()

      if question is None:
        abort(400)

      print("Good")

    else:
      question = Question.query.filter(Question.id == 3).one_or_none()

      if question is None:
        abort(400)

      print(question.answer)

    return jsonify({
      'id': question.id,
      'question': question.question,
      'answer': question.answer
    }) 

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(400)
  def invalid_question(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Invalid Question"
    }), 400

  @app.errorhandler(404)
  def no_questiona_for_category(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "There are no questions for this request"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable error"
      }), 422

  return app

    
