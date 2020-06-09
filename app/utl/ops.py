import sqlite3

DB_FILE = 'blog.db'


def init():
    #required actions to interact with sqlite
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # creates the users table
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, password TEXT);")
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
        c.execute("INSERT INTO users(username, password) VALUES(?, ?);" , (username, password))
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


