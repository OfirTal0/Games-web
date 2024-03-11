import sqlite3

def query(sql:str="", db_name="users.db"):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        rows = cur.execute(sql)
        return list(rows)
    


def create_table(table="users"):
    sql = f"CREATE TABLE IF NOT EXISTS {table} (username TEXT, password TEXT, profileimg TEXT, country TEXT)"
    query(sql)

def create_table(table="trivia_data"):
    sql = f"CREATE TABLE IF NOT EXISTS {table} (category TEXT, question TEXT, options TEXT, correct_answer TEXT, use TEXT)"
    query(sql = sql,db_name = "games_data.db")

def create_table(table="games_scores"):
    sql = f"CREATE TABLE IF NOT EXISTS {table} (username TEXT, game TEXT, highest_score TEXT)"
    query(sql=sql,db_name="games.db")

def insert_new_user(table="users", values=""):
    sql = f"INSERT INTO {table} (username, password, profileimg, country, permission) VALUES ({values})"
    query(sql)

def get_users():
    existing_users=query(f"SELECT * FROM users")
    columns = [column[1] for column in query("PRAGMA table_info(users)")]
    users_list = []
    for row in existing_users:
        user_dict = dict(zip(columns, row))
        users_list.append(user_dict)
    return users_list

def get_games(text=""):
    if text =="":
        existing_games=query(sql = f"SELECT * FROM games",db_name="games.db")
    else:
        existing_games = query(sql=f"SELECT * FROM games WHERE game LIKE '%{text}%'", db_name="games.db")
    columns = [column[1] for column in query(sql = "PRAGMA table_info(games)",db_name="games.db")]
    games_list = []
    for row in existing_games:
        game_dict = dict(zip(columns, row))
        games_list.append(game_dict)
    return games_list

def get_users_scores():
    existing_scores=query(sql=f"SELECT * FROM games_scores",db_name="games.db")
    columns = [column[1] for column in query(sql = "PRAGMA table_info(games_scores)",db_name="games.db")]
    scores_list = []
    for row in existing_scores:
        score_dict = dict(zip(columns, row))
        scores_list.append(score_dict)
    return scores_list

def create_table_trivia(table="trivia_data"):
   sql = f'''
    CREATE TABLE IF NOT EXISTS {table} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT,
        use TEXT
    );
    ''' 
   query(sql = sql,db_name = "games.db")


# def insert_trivia_data(data_dict=combined_dict, table="trivia_data"):
#     with sqlite3.connect("games.db") as conn:
#         cur = conn.cursor()
#         for category, category_dict in data_dict.items():
#             for question in category_dict:
#                 sql = f"INSERT INTO {table} (category, question, option_a, option_b, option_c, option_d, correct_answer, use) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
#                 values = (category, question['question'], question['options']['a'], question['options']['b'], question['options']['c'], question['options']['d'], question['correct_answer'], question['use'])
#                 cur.execute(sql, values)



def check_new_score(game,username,profileimg,points):
    sql = f"SELECT * FROM 'games_scores' WHERE game='{game}'"
    users_score=query(sql=sql,db_name="games.db")
    new_user_game = True
    for user in  users_score:
        if user[0] == username:
            new_user_game = False
            if points > user[3]:
                message = 'You break your record! Good job'
                sql = f"UPDATE games_scores SET highest_score='{points}' WHERE username='{username}' AND game='{game}'"
                query(sql=sql,db_name="games.db")
            else:
                message = 'You didnt break your record! No worries, next time!'
    if new_user_game:
        message = 'First time - New record! Good job'
        sql = f"INSERT into games_scores VALUES ('{username}', '{profileimg}', '{game}', '{points}')"
        query(sql=sql,db_name="games.db")
    return message