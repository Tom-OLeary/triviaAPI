# Full Stack API

## Trivia
This is a React.js and Python based trivia game. It allows players to answer random questions based on category.

#### Functionality
1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Running the project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. 
Reference the frontend and backend README files located below for more specific set-up requirements.

## About the Stack
### Backend

The `./backend` directory contains a  Flask and SQLAlchemy server which defines endpoints and creates modelsfor the
 database.
 
[View the README.md within ./backend for more details.](starter/backend/README.md)

### Frontend

The `./frontend` directory contains a React frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](starter/frontend/README.md)

## Acknowledgements
The Udacity team for providing the front end code as well as the initial Questions and Category Models.
