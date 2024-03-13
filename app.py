from flask import Flask, render_template, request, redirect, session
import random
import json
from db import query, insert_new_user,get_users,check_new_score, get_users_scores,get_games,update_highest_score,insert_highest_score
app = Flask(__name__)


app.secret_key = 'OfirTalCode'

def top_users():
    users = get_users()
    sorted_users = sorted(users, key=lambda x:x['score'], reverse=True)
    top_three = sorted_users[:3]
    return top_three

def top_games():
    games = get_games()
    top_games = []
    for game in games:
        if game["top"] == "yes":
            top_games.append(game)
    return top_games

def top_players_dict():
    top_players_dict = {}
    scores = get_users_scores()
    for entry in scores:
        username = entry['username']
        game = entry['game']
        highest_score = entry['highest_score']
        profileimg = entry['profileimg']
        if game not in top_players_dict or (highest_score is not None and highest_score > top_players_dict[game]['highest_score']):
            top_players_dict[game] = {'username': username, 'profileimg':profileimg, 'game': game, 'highest_score': highest_score}
    return list(top_players_dict.values())

@app.route('/', methods = ['POST', 'GET'])
def home():
    top_players = top_players_dict()
    top_games_list = top_games()
    if 'username' in session:
        username = session['username']
        profileimg = session.get('profileimg', '')
        permission = session.get('permission', '')
        return render_template('dashbord.html',permission=permission,action='Display',login=True, username=username, profileimg=profileimg, top_players= top_players, top_games=top_games_list)
    else:
        permission=''
        return render_template('dashbord.html',permission='', username='', profileimg='', login=False,top_players= top_players,top_games=top_games_list)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "GET":
        if 'username' in session:
            return redirect('/')
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        existing_users = query(f"SELECT * FROM users WHERE username = '{username}' AND password='{password}'")

        if existing_users:
            user_data = existing_users[0]
            session['username'] = user_data[1]
            session['profileimg'] = user_data[3]  
            session['permission'] = user_data[5]
            return redirect('/')
        else:
            return render_template('login.html', error='No user was found, please sign up')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('profileimg', None)
    session.pop('admin',None)
    session.pop('permission',None)
    return redirect('/')

@app.route('/signup', methods = ['POST','GET'])
def signup(): 
        return render_template('signup.html')

@app.route('/games', methods = ['POST','GET'])
def games(): 
    games = get_games()
    return render_template('games.html', games=games)

@app.route('/score', methods = ['POST','GET'])
def score(): 
    scores = get_users_scores()
    return render_template('score.html', scores=scores)


@app.route('/register', methods = ['POST','GET'])
def register():
    username = request.form.get('username')
    existing_users=query(f"SELECT * FROM users WHERE username = '{username}'")
    if existing_users:
        return render_template('signup.html',error = f'username already exist. Please choose another')
    password = request.form.get('password')
    profileimg = request.form.get('profileimg','ghost')
    country = request.form.get('country')
    permission = 'view'
    insert_new_user(values=f"'{username}', '{password}', '{profileimg}', '{country}', '{permission}'")  
    session['username'] = username
    session['profileimg'] = profileimg
    session['permission'] = 'view'
    return redirect('/')


@app.route('/reset_my_password', methods = ['POST','GET'])
def reset_my_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    else:
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        verify_password = request.form.get('verify_password')
        if new_password == verify_password:
            user = query(sql = f"SELECT username FROM users WHERE username='{username}'")
            if len(user) > 0:
                query(sql = f"UPDATE users SET password = '{new_password}' WHERE username='{username}'")
                return render_template("login.html")
            else:
                error = 'no such user was found'
                return render_template("reset_password.html", error = error)
        else:
            error = 'The passwords do not match, try again'
            return render_template("reset_password.html", error = error)


#trivia game

def get_trivia_data_dict():
    existing_trivia_data=query(sql = f"SELECT * FROM trivia_data", db_name="games.db")
    trivia_data_dict = []
    keys = ["id","category","question","option_a","option_b","option_c","option_d","correct_answer","use"]
    for row in existing_trivia_data:
        row = list(row)
        my_dict= dict(zip(keys,row))
        trivia_data_dict.append(my_dict)
    return trivia_data_dict

@app.route('/trivia', methods = ['POST','GET'])
def trivia_game_start(): 
    query(sql = f"UPDATE trivia_data SET use = 'no'", db_name="games.db")
    if 'username' in session:
        username = session['username']
        profileimg = session['profileimg']
        session['trivia_points'] = 0
        session['trivia_mistakes'] = 0
        return render_template('trivia_game.html',trivia_display = 'start', username=username, profileimg=profileimg, points=session['trivia_points'])
    else:
        return render_template('login.html')

def get_avalible_ques():
    avalible_ques = query(sql = f"SELECT * FROM trivia_data WHERE use = 'no'", db_name="games.db")
    avalible_ques_dict = []
    keys = ["id","category","question","option_a","option_b","option_c","option_d","correct_answer","use"]
    for row in avalible_ques:
        row = list(row)
        my_dict= dict(zip(keys,row))
        avalible_ques_dict.append(my_dict)
    return avalible_ques_dict
 
def get_avalible_categories_list():
    categories_list = []
    avalible_ques = get_avalible_ques()
    for ques in avalible_ques:
        categories_list.append(ques["category"])
    avalible_categories = set(categories_list)
    avalible_categories = list(avalible_categories)
    return avalible_categories


@app.route('/trivia_game_options', methods = ['POST', 'GET'])
def trivia_game_options():
    username = session['username']
    profileimg = session['profileimg']
    if session['trivia_mistakes'] == 3:
        message = f'You were wrong 3 times!  Game Over'
        return render_template('trivia_game.html',trivia_display = 'endgame', message = message, username=username, profileimg=profileimg, points=session['trivia_points'] )
    avalible_categories = get_avalible_categories_list()
    if len(avalible_categories) == 1: 
        category1 = avalible_categories[0]
        category2 = avalible_categories[0]
    elif len(avalible_categories) == 0:
        message = f'No more questions left. Your score is {session['trivia_points']}, Great Job! '
        return render_template('trivia_game.html',trivia_display = 'endgame', message = message, username=username, profileimg=profileimg, points=session['trivia_points'])
    else:
        category1, category2 = random.sample(avalible_categories, 2)
    return render_template('trivia_game.html',trivia_display = 'options', username=username, profileimg=profileimg, points=session['trivia_points'], category1=category1, category2=category2)

@app.route('/trivia_questions', methods = ['POST', 'GET'])
def questiongame():
    global correct_answer
    username = session['username']
    profileimg = session['profileimg']
    choosen_category = request.form["category"]
    avalible_ques = query(sql = f"SELECT * FROM trivia_data WHERE use = 'no' and category == '{choosen_category}'", db_name="games.db")
    avalible_ques_dict = []
    keys = ["id","category","question","option_a","option_b","option_c","option_d","correct_answer","use"]
    for row in avalible_ques:
        row = list(row)
        my_dict= dict(zip(keys,row))
        avalible_ques_dict.append(my_dict)
    rand_ques = random.choice(avalible_ques_dict)
    question = rand_ques["question"]
    option1 = rand_ques["option_a"]
    option2 = rand_ques["option_b"]
    option3 = rand_ques["option_c"]
    option4 = rand_ques["option_d"]
    correct_answer = rand_ques["correct_answer"]
    id = rand_ques["id"]
    query(sql = f"UPDATE trivia_data SET use = 'yes' WHERE id = '{id}'", db_name="games.db")
    return render_template('trivia_game.html',trivia_display = 'questions', username=username, profileimg=profileimg, points=session['trivia_points'], question=question,option1=option1,option2=option2,option3=option3,option4=option4, correct_answer=correct_answer )


@app.route('/trivia_answer', methods = ['POST', 'GET'])
def answer():
    global correct_answer
    username = session['username']
    profileimg = session['profileimg']
    answer = request.form["answer"]
    message = ""
    if answer == correct_answer:
        points=int(session['trivia_points'])
        points += 2
        session['trivia_points'] = points
        message = f'Good job! You got 2 points'
    else:
        mistakes=int(session['trivia_mistakes'])
        mistakes += 1
        session['trivia_mistakes'] = mistakes
        message = f'Wrong choice! Try again next time'
    return render_template('trivia_game.html',trivia_display = 'answers', username=username, profileimg=profileimg, points=session['trivia_points'], message=message)


@app.route('/trivia_endgame', methods = ['POST', 'GET'])
def endgame():
    points = session['trivia_points']
    username = session['username']
    profileimg = session['profileimg']
    # message = check_new_score(game="trivia",username=username,profileimg=profileimg,points=points)
    query(sql = f"UPDATE trivia_data SET use = 'no'", db_name="games.db")
    trivia_highest_score = query(sql = f"SELECT highest_score FROM games_scores WHERE username= '{username}'and game = 'trivia'", db_name="games.db")
    if not trivia_highest_score:
        query(sql = f"INSERT INTO games_scores (username,profileimg,game,highest_score) VALUES ('{username}', '{profileimg}','trivia','{points}')", db_name="games.db")
    else:
        highest_score =trivia_highest_score[0][0]
        if  highest_score < points:
            query(sql = f"UPDATE games_scores SET highest_score = {points} WHERE username = '{username}' AND game = 'trivia'", db_name="games.db")

    session['trivia_points'] = 0
    session['trivia_mistakes'] = 0
    return render_template('trivia_game.html', trivia_display = 'start', username=username, profileimg=profileimg, points=points)



# simon game

@app.route('/simon', methods = ['POST','GET'])
def simon_game_start(): 
    if 'username' not in session:
        return render_template('login.html')
    else:
        username = session['username']
        profileimg = session['profileimg']
        try:
            simon_highest_score = query(sql = f"SELECT highest_score FROM games_scores WHERE username= '{username}'and game = 'simon'", db_name="games.db")
            score_value = simon_highest_score[0][0]
        except:
            score_value = 0
        return render_template('simongame.html', username=username, profileimg=profileimg,simon_highest_score=score_value)


#memory game

@app.route('/memory', methods=['POST', 'GET'])
def memory_game():
    if 'username' not in session:
        return render_template('login.html')
    else:
        username = session['username']
        profileimg = session['profileimg']
        return render_template('memorygame.html',username=username, profileimg=profileimg)
    

#admin page

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    selected_users = query(f"SELECT username, password, permission, profileimg, country FROM 'users'")
    return render_template('admin.html',action='Display',users=selected_users,permission= session['permission'])
   
@app.route('/adminaction', methods=['POST', 'GET'])
def adminaction():
    action = request.form.get('action')
    select_user =  request.form.get('selected_user')
    if action == 'Delete':
        sql = f"DELETE FROM users WHERE username = '{select_user}'"
        query(sql)
    elif action == 'Edit':
        global user_to_edit
        user_to_edit =  query(f"SELECT * FROM 'users' WHERE username='{select_user}'")
        if len(user_to_edit) == 0:
            error = "please select a user"
            selected_users = query(f"SELECT username, password, profileimg, country FROM 'users'")
            return render_template('admin.html',error=error,action='Display',users=selected_users,permission= session['permission'])
        id_to_edit = user_to_edit[0][0]
        username_to_edit=user_to_edit[0][1]
        password_to_edit= user_to_edit[0][2]
        profileimg_to_edit= user_to_edit[0][3]
        country_to_edit = user_to_edit[0][4]
        user_to_edit = {"id_to_edit":id_to_edit,"username_to_edit":username_to_edit,"password_to_edit":password_to_edit,"profileimg_to_edit":profileimg_to_edit,"country_to_edit":country_to_edit}
        return render_template('admin.html',country_to_edit=country_to_edit,profileimg_to_edit=profileimg_to_edit,password_to_edit=password_to_edit,username_to_edit=username_to_edit,action=action,permission= session['permission'])
    elif action == 'Add':
        return redirect('/signup')
    elif action == 'Display':
        selected_users = query(f"SELECT username, password, permission, profileimg, country FROM 'users'")
        return render_template('admin.html',action='Display',users=selected_users,permission= session['permission'])
    selected_users = query(f"SELECT username, password, permission, profileimg, country FROM 'users'")
    return render_template('admin.html',action='Display',users=selected_users,permission= session['permission'])

@app.route('/adminedit', methods=['POST', 'GET'])
def adminedit():
    global user_to_edit
    save_cancel = request.form.get('save_cancel')
    if save_cancel == "Save":
        id_to_update = user_to_edit["id_to_edit"]
        username_to_update = request.form.get('username')
        profileimg_to_update = request.form.get('profileimg')
        password_to_update = request.form.get('password')
        country_to_update = request.form.get('country')
        permission_to_update = request.form.get('permission')
        query(f"UPDATE users set username='{username_to_update}',permission='{permission_to_update}', profileimg='{profileimg_to_update}',password='{password_to_update}', country='{country_to_update}' WHERE id='{id_to_update}'")
        selected_users = query(f"SELECT username, password, permission, profileimg, country FROM 'users'")
        return render_template('admin.html',action='Display',users=selected_users,permission= session['permission'])
    elif save_cancel == "Cancel":
        selected_users = query(f"SELECT username, password, permission, profileimg, country FROM 'users'")
        return render_template('admin.html',action='Display',users=selected_users,permission= session['permission'])


@app.route('/search', methods=['POST', 'GET'])
def search():        
    action = request.form.get('action')
    if action == 'user':
        text = request.form.get('search_user')
        error = ''
        results= query(f"SELECT username, password, permission, profileimg, country FROM users WHERE username LIKE '%{text}%' OR password LIKE '%{text}%' OR permission LIKE '%{text}%' OR profileimg LIKE '%{text}%' OR country LIKE '%{text}%'")
        if len(results) == 0:
            error= 'No results were found'
        return render_template('admin.html',error=error,action='Display',users=results,permission= session['permission'])
    elif action == 'game':
        text = request.form.get('search_game')
        error = ''
        games = get_games(text)
        if len(games) == 0:
            error= 'No results were found'
        else:
            results = games
        return render_template('games.html',games=results, error=error)
    

# war game


@app.route('/war', methods=['POST', 'GET'])
def war_game():
    if 'username' not in session:
        return render_template('login.html')
    else:
        username = session['username']
        profileimg = session['profileimg']
        return render_template('war_game.html',username=username, profileimg=profileimg)
    

# points
    

@app.route('/api/points', methods=['POST', 'GET'])
def get_points():
    if 'username' in session:
        if request.method == 'GET':
            username = session['username']
            user_highest_scores = query(sql=f"SELECT game, highest_score FROM games_scores WHERE username= '{username}'", db_name="games.db")
            scores_json = [{"game": score[0], "highest_score": score[1]} for score in user_highest_scores]
            return json.dumps(scores_json)
    else:
        return json.dumps({"error": "User not logged in"})

@app.route('/api/points/add', methods=['POST', 'GET'])
def memory_points():
    if request.method == 'POST':
        try:
            data_received = request.json
            username = session.get('username')
            profileimg =  session.get('profileimg')
            points = data_received.get('points')
            action = data_received.get('action')
            game = data_received.get('game')
            if action == 'update':
                update_highest_score(username,points,game)
            elif action == 'insert':
                insert_highest_score(username,profileimg,points,game)
            return json.dumps({"success": True, "message":f"the points is {points} in game {game}"})
        except:
            return json.dumps({"error": "No points provided in the request"})
