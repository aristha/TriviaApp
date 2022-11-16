# API Development and Documentation Final Project

## Trivia App 

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

### Getting Started

Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.
To run the application run the following commands:
```console
export DB_HOST=127.0.0.1:5433 # host DB postgresql
export DB_USER=postgres # USER DB
export DB_PASSWORD=admin # password DB
export DB_NAME=trivia
export FLASK_APP=flaskr
export FLASK_DEBUG=true # enables debug mode
flask run
```


These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend
From the frontend folder, run the following commands to start the client:
```console
npm install  // only once to install dependencies
npm start 
```


By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:
```console
export DB_HOST=127.0.0.1:5433 # host DB postgresql
export DB_USER=postgres # USER DB
export DB_PASSWORD=admin # password
export DB_NAME=trivia
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

### Error Handling
Errors are returned as JSON objects in the following format:
```console
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable
### Endpoints
#### GET /categories
- General:
  - Returns a categories success value
  - Sample: `curl http://127.0.0.1:5000/categories `
```console
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
#### GET /questions
- General:
  - Return a list of questions, number of total questions, current category, categories.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
  - Sample: `curl http://127.0.0.1:5000/questions?page=1 `
```console
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "b",
            "category": 1,
            "difficulty": 2,
            "id": 24,
            "question": "a is ?"
        }
    ],
    "success": true,
    "total_questions": 23
}
```

#### DELETE /questions/<int:question_id>
- General:
  - DELETE question using a question ID.
  - Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1 `
```console
{
    "success": true
}
```
#### POST /questions>
- General:
  - Creates a new question using the submitted question and answer text,
    category, and difficulty score
  - Sample: `curl  http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who discovered penicillin?", "answer":"Alexander Fleming", "category":"1",, "difficulty":"3"}' `
```console
{
    "success": true
}
```
#### POST /questions>
- General:
  - return Question based on a search term
  - Sample: `curl  http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"branch"}' `
```console
{
    "success": true,
    "questions":[
      {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
    ],
    "total_questions":100,
    "current_category":1
}
```

#### GET /categories/<int:categorie_id>/questions
- General:
  - return Question questions based on category
  - Sample: `curl  http://127.0.0.1:5000/categories/1/questions`
```console
{
    "success": true,
    "questions":[
      {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
    ],
    "total_questions":1,
    "current_category":1
}
```

#### POST /quizzes>
- General:
  - return Question based on a search term
  - Sample: `curl  http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[4],"quiz_category":{"id":"1","type":"Science"}}' `
```console
{
    "success": true,
    "question": {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
    }
}
```
