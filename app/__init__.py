import os
from flask import Flask, render_template, session, url_for, redirect, request, flash
from utl import ops


app = Flask(__name__)

app.secret_key = os.urandom(32)

ops.init()

#=====DECORATOR=FUNCTIONS===================================================
# Decorator functions to eliminate redundancy:

# Login checking
def protected(route_function):
    def login_check(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    login_check.__name__ = route_function.__name__
    return login_check

#============================================================================





# root redirects to login if the user isn't logged in, and home if they are
@app.route("/")
def root():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    # else redirect to login
    return redirect(url_for("login"))


@app.route("/login")
def login():
    # if already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for("home"))
    # make sure the login attempt has both a username and a password
    if len(request.args) == 2:
        # if username or password is blank, flash error
        if request.args["username"] == "" or request.args["password"] == "":
            flash("Please do not leave any fields blank")
        else:
            # database checks the username and password
            if ops.check_user(request.args["username"], request.args["password"]):
                # Username is added to the session information
                session["username"] = request.args["username"]
                # The user is now logged in and goes to the home page
                return redirect(url_for("home"))
            else:
                flash("Invalid username/password combination")
    return render_template("login.html")


# register page and validation
@app.route("/register")
def register():
    # if user is logged in, redirect to home
    if "username" in session:
        return redirect(url_for("home"))
    if len(request.args) >= 3:
        # if any one of the three fields are blank, flash error
        if request.args["username"] == "" or request.args["password1"] == "" or request.args["password2"] == "":
            flash("Please do not leave any fields blank.")
        # if the passwords don't match, flash error
        elif request.args["password1"] != request.args["password2"]:
            flash("Passwords don't match.")
        # else if adding the user (to the database) is successful, username must be unique
        elif ops.add_user(request.args["username"], request.args["password1"]):
            # if the username is unique, session is added and user is redirected to home
            session["username"] = request.args["username"]
            return redirect(url_for("home"))
        else:
            flash("Username not unique.")
    # render register template
    return render_template('register.html')


@app.route("/logout")
def logout():
    if "username" in session:
        # remove the login from the session
        session.pop("username")
    # go back to login
    return redirect(url_for("login"))


@protected
@app.route("/home")
def home():
    return render_template("home.html")


@protected
@app.route("/coins")
def money():
    if len(request.args) == 1:
        ops.add_money(session["username"], request.args["amount"])
    return render_template("coins.html", cash=ops.get_money(session["username"]))

if __name__ == "__main__":
    app.debug = True
    app.run()
