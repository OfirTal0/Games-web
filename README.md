# GAMES WEB APPLICATION

A web-based application that helps users organize and manage their tasks and contacts effectively. 
Welcome to my Game Web Application!
This platform offers a collection of small games, including Simon Game, Cards War Game, Memory Game (JavaScript-based), and a Trivia Game (Python-based).
Users can enjoy playing these games and compete for the best scores!

## Features
### User Authentication
New users must sign up to access the games. Existing users can log in.
Forgot your password? No worries! Use the reset password option to regain access.
Login validation.

### Admin Section
Users with admin permissions have access to a special section for managing users settings.

### Games
1. Simon Game - A classic memory game to test and improve your memory skills. include sounds. 
2. Cards War Game - War is a very simple card game for two players. Buttle against the computer.
3. Memory Game - A card-matching game to test your concentration and memory (the game category can be choosen).
4. Trivia Game - Answer a series of questions and test your knowledge in various categories. Python-based trivia game.

## Scoreboard
The best scores for each user in each game are displayed in the score board section.
Top scores in each game are featured on the dashboard with the corresponding usernames.

## Getting Started

### Docker:

docker run -p 5000:5000 ofirtal/gameonweb

### Hosting:

http://ofirtal.pythonanywhere.com/

### Locally: 
1.Clone the repository:
  git clone https://github.com/OfirTal0/Games-Web.git
2.Navigate to the project directory:
  cd Games-Web
3.python -m pip install -r requirements.txt
4.python ./manage.py runserver
  
## Needs correction and completion:
Automatic update of the score to DB

Happy gaming! 🎮🚀
