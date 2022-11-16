import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import or_
from models import setup_db, Question, Category
import sys
QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
        )
        return response

    def paginate_questions(request, selection):

        
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [book.format() for book in selection]
        current_questions = questions[start:end]

        return current_questions
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # Get All categories
    @app.route("/categories", methods=["GET"])
    def get_categories():

        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}
        return jsonify(
            {
                "success": True,
                "categories": formatted_categories
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    # Get questions
    @app.route("/questions", methods=["GET"])
    def get_questions():
        selection = Question.query.all()
            
        

        questions = paginate_questions(request, selection)
        if len(questions) ==0:
            abort(404)
        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}
        return jsonify(
            {
                "success": True,
                "questions": questions,
                "categories":formatted_categories,
                "total_questions": len(Question.query.all()),
                "current_category":None
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # Delete questions
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    # @cross_origin
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify(
                {
                    "success": True
                }
            )
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # Create new question or Search question
    @app.route("/questions", methods=["POST"])
    def create_question():
        
        body = request.get_json()
        try:
            question = body.get("question", None)
            answer = body.get("answer", None)
            category = body.get("category", None)
            difficulty = body.get("difficulty", None)
            searchTerm = body.get("searchTerm", None)
            if searchTerm: 
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(searchTerm))
                )
                current_questions = paginate_questions(request,selection)
                if len(current_questions) == 0:
                    abort(404)
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                        "current_category":None
                    }
                )
            else:
                question_new = Question(question=question,answer=answer,category=category,difficulty=difficulty)
                question_new.insert()
                return jsonify(
                    {
                        "success": True
                    }
                )
            
        except:
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # Get questions based on category
    @app.route("/categories/<int:categorie_id>/questions", methods=["GET"])
    # @cross_origin
    def get_question(categorie_id):
        try:
            selection = Question.query.filter(Question.category == categorie_id)
            questions = paginate_questions(request,selection)
            category = Category.query.filter(Category.id == categorie_id).first()
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": category.type
                }
            )
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # get random questions within the given category
    @app.route("/quizzes", methods=["POST"])
    # @cross_origin
    def get_random_quizzes():
        
        body = request.get_json()
        try:
            previous_questions = body.get("previous_questions")
            category_id = body['quiz_category']['id']

            selection = Question.query.filter(or_(Question.category == category_id, category_id == '0'),
                                              or_(len(previous_questions) == 0,~Question.id.in_(previous_questions)))
            questions = [book.format() for book in selection]
            if len(questions) == 0:
                current_question = None
            else:
                current_question = random.choice(questions)
            
            return jsonify(
                {
                    "success": True,
                    "question": current_question
                }
            )
        except:
            print(sys.exc_info())
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    return app


