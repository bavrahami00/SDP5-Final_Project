import sqlite3

DB_FILE = 'blog.db'


def init():
    #required actions to interact with sqlite
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # creates the users table
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT, money INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS guides(id INTEGER, user TEXT, name TEXT, rating REAL, cost INTEGER, buyers INTEGER, subject TEXT, guide TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS ratings(id INTEGER, user TEXT, rating INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS comments(id INTEGER, user TEXT, comment TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS discussions(id INTEGER, name TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS talk(id INTEGER, comment TEXT);")
    # required actions to save changes
    db.commit()
    db.close()


def add_user(username,password):
    # requierd actions to interact with sqlite
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # finds all instances where the username is the given username
    c.execute("SELECT * FROM users WHERE username = ?;" , (username,))
    ans = False;
    # if there is no instance of the username:
    if c.fetchone() is None:
        # the registration attempt succeeds and the username-password pair are inserted into the database
        c.execute("INSERT INTO users(username, password, money) VALUES(?, ?, 0);" , (username, password))
        ans = True
    # required actions to save changes
    db.commit()
    db.close()
    # returns true is there is no previous instance of the username; false otherwise
    return ans


def check_user(username,password):
    #required actions to interact with sqlite
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # finds all instances where username is the given username and password is the given password
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?;" , (username, password))
    # returns true if there is (at least) one instance of the given username and password; false otherwise
    ans = not c.fetchone() is None
    db.close()
    return ans


def get_money(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?;" , (username,))
    ans = c.fetchall()
    db.close()
    for row in ans:
        return row[2]


def add_money(username,amount):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE users SET money = money + ? WHERE username = ?;" , (amount, username))
    db.commit()
    db.close()


def get_unguides(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM guides WHERE user != ?;" , (username))
    g = c.fetchall()
    db.close()
    ans = []
    for row in g:
        next = {}
        next["user"] = row[1]
        next["name"] = row[2]
        next["rating"] = row[3]
        next["cost"] = row[4]
        next["buyers"] = row[5]
        next["subject"] = row[6]
        next["guide"] = row[7]
        ans.append(next)
    return ans


def get_guides(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM guides WHERE user = ?;" , (username))
    g = c.fetchall()
    db.close()
    ans = []
    for row in g:
        next = {}
        next["user"] = row[1]
        next["name"] = row[2]
        next["rating"] = row[3]
        next["cost"] = row[4]
        next["buyers"] = row[5]
        next["subject"] = row[6]
        next["guide"] = row[7]
        ans.append(next)
    return ans
