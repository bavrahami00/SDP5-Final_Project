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


@app.route("/home")
@protected
def home():
    return render_template("home.html", own_guides=ops.get_own_guides(session["username"]), pur_guides=ops.get_pur_guides(session["username"]))


@app.route("/coins")
@protected
def money():
    if len(request.args) == 1:
        ops.add_money(session["username"], request.args["amount"])
    return render_template("coins.html", cash=ops.get_money(session["username"]))


@app.route("/create")
@protected
def create():
    return render_template("create.html", subjects = ops.get_subjects())


@app.route("/created")
@protected
def make():
    if len(request.args) < 5:
        return redirect(url_for("home"))
    if request.args["title"] == "":
        flash("Do not leave the title blank")
        return redirect(url_for("create"))
    if request.args["subject"] == "Other" and request.args["other"] == "":
        flash("Please fill in a subject")
        return redirect(url_for("create"))
    if request.args["price"] == "":
        flash("Do not leave the price blank")
        return redirect(url_for("create"))
    price = 0
    try:
        price = int(request.args["price"])
    except:
        flash("Please enter a number")
        return redirect(url_for("create"))
    sub = request.args["subject"]
    if sub == "Other":
        sub = request.args["other"]
    ops.create_guide(session["username"],request.args["title"],request.args["price"],sub,request.args["guide"])
    return redirect(url_for("home"))


@app.route("/buy/<id>")
@protected
def get(id):
    if ops.has_bought(session["username"],id) or ops.buy_guide(session["username"],id):
        return redirect(url_for("guide",number=id))
    flash("You don't have enough money to buy this")
    return redirect(url_for("home"))


@app.route("/opinion/<id>")
@protected
def opinions(id):
    if len(request.args) >= 1:
        if request.args["comment"] != "":
            ops.add_comment(session["username"],id,request.args["comment"])
    return redirect(url_for("guide",number=id))


@app.route("/guide/<number>")
@protected
def guide(number):
    if ops.has_bought(session["username"],number):
        return render_template("guide.html", info = ops.get_guide_info(number), comments = ops.get_comments(number))
    return redirect(url_for("home"))


@app.route("/market")
@protected
def market():
    return render_template("market.html", guides = ops.get_unguides(session['username']))


@app.route("/forum")
@protected
def forum():
    if len(request.args) == 1:
        if request.args["title"] == "":
            flash("Do not leave the name blank")
        else:
            ops.create_discussion(request.args["title"])
    return render_template("forum.html", discussions = ops.get_discussions())


@app.route("/talk/<number>")
@protected
def talk(number):
    return render_template("talk.html", comments = ops.get_discussion(number), id=number)


@app.route("/talker/<id>")
@protected
def talker(id):
    if len(request.args) >= 1:
        if request.args["comment"] != "":
            ops.add_talk(session["username"],id,request.args["comment"])
    return redirect(url_for("talk",number=id))


if __name__ == "__main__":
    app.debug = True
    app.run()
