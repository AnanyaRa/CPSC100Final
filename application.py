import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookupweather

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cal.db")

# Home screen that displays user's name, local weather, the date, and events for that day
@app.route("/")
@login_required
def index():
    name = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
    city = db.execute("SELECT city FROM users WHERE id=?", session["user_id"])
    for person in name:
        name = person['username']

    # Using lookupweather function to figure out the current weather of given city.
    for place in city:
        city = place['city']
    city = str(city)
    result = lookupweather(city)
    # CODE TO SHOW TODAY"S EVENTS
    x = datetime.datetime.now()
    if x.day<10:
        num = "0" + str(x.day)
    else:
        num = str(x.day)
    y = str(x.year) + "-" + str(x.month) + "-" + num
    days = db.execute("SELECT name FROM events WHERE date = ? AND user_id = ?", y, session["user_id"])
    return render_template("home.html", name=name, city=city, result=result, days=days)
    return apology("Error")

# allows users to add new event, adding it to the SQL table
@app.route("/newevent", methods=["GET", "POST"])
@login_required
def newevent():
    if request.method == "POST":

        # Ensures user enters a date for the event
        if not request.form.get("date"):
            return apology("must enter date for event", 400)

        # Ensures user enters a name for the event
        if not request.form.get("eventname"):
            return apology("must enter name for event", 400)

        # Ensures user enters either a Y or N for importance, not anything else (aside from entering nothing)
        if (request.form.get("check") != "Y") and (request.form.get("check") != "N"):
            if request.form.get("check"):
                return apology("must enter either Y or N for importance", 400)

        # Formatting date to be entered into the datetime functions properly
        specificId = db.execute("SELECT id FROM users WHERE id=?", session["user_id"])
        date = request.form.get("date")
        date = date.replace("[","")
        date = date.replace("]","")
        date = date.split("-")
        print(date)
        year = int(date[0])
        month = date[1]
        month = month.replace("0","")
        month = int(month)
        day = date[2]
        day = int(day)

        for person in specificId:
            name = person["id"]
            y = datetime.datetime.weekday(datetime.datetime(year, month, day))
            # print(y)

        # Using result of datetime function to assign a certain day of the week to given event
        if y==0:
            weekday="Monday"
        if y==1:
            weekday="Tuesday"
        if y==2:
            weekday="Wednesday"
        if y==3:
            weekday="Thursday"
        if y==4:
            weekday="Friday"
        if y==5:
            weekday="Saturday"
        if y==6:
            weekday="Sunday"

        # Entering event information into events SQL table
        event = db.execute("INSERT INTO events (name, description, date, start, end, important, user_id, weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", request.form.get("eventname"), request.form.get("description"), request.form.get("date"), request.form.get("starttime"), request.form.get("endtime"), request.form.get("check"), name, weekday)
        events = db.execute("SELECT name, description, date, start, end, important, entered, weekday FROM events WHERE user_id = ? ORDER BY date, start", session["user_id"])


        if not event:
            return apology("Must enter event")

        return render_template("allevents.html", events=events)

    else:
        return render_template("newevent.html")

# displays all added events by user
@app.route("/allevents")
@login_required
def allevents():
    events = db.execute("SELECT name, description, date, start, end, important, entered FROM events WHERE user_id = ? ORDER BY date, start", session["user_id"])
    return render_template("allevents.html", events=events)
    return apology("Error")

# deletes events from table using separate page
@app.route("/delete", methods =["GET", "POST"])
@login_required
def delete():
    events = db.execute("SELECT name, description, date, start, end, important, entered FROM events WHERE user_id = ? ORDER BY date, start", session["user_id"])
    # name = request.form.get("delete")
    if request.method == "POST":

        # Ensures user entered an actual event
        if not request.form.get("delete"):
            return apology("must enter an event to delete", 400)

        name = request.form.get("delete")
        db.execute("DELETE FROM events WHERE name = ? AND user_id = ?", name, session["user_id"])
        events = db.execute("SELECT name, description, date, start, end, important, entered FROM events WHERE user_id = ? ORDER BY date, start", session["user_id"])
        return render_template("allevents.html", events=events)
    else:
        return render_template("delete.html", events=events)
    return apology("Error")

#allows user to login & be given a user id
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    # return render_template("login.html")
    return apology("Error")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        name = request.form.get("username")
        if not name:
            return apology("must provide username", 400)

        # Ensure a city was submitted
        elif not request.form.get("city"):
            return apology("must enter city", 400)

        # Ensure a valid city was submitted
        elif lookupweather(request.form.get("city")) == None:
            return apology("must enter a valid city name", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide re-entered password", 400)

        pw = request.form.get("password")
        pw2 = request.form.get("confirmation")

        if not pw == pw2:
            return apology("passwords don't match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # check if username already exists
        if len(rows) == 1:
            return apology("username already exists", 400)

        pwhash = generate_password_hash(pw)
        city = request.form.get("city")
        db.execute("INSERT INTO users (username, hash, city) VALUES(?,?,?)", name, pwhash, city)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")
    return apology("Error")

# displays monthly calendar for user
@app.route("/month", methods=["GET", "POST"])
@login_required
def month():
    if request.method == "POST":
        return apology("Error")
    else:
        return render_template("month.html")

#displays only the events for the current week
@app.route("/calendar")
@login_required
def calendar():
    todayDay = datetime.datetime.now()
    # print(todayDay)
    changeDay = datetime.timedelta(1)
    counter = 0;
    beginning = todayDay

    # Formula to calculate the beginning date for a certain week
    while datetime.datetime.weekday(beginning) != 6:
        beginning = beginning - changeDay
        counter = counter + 1

    # Using above formula result to calculate the upper bound of the same week (the closest Saturday)
    changeWeek = datetime.timedelta(6)
    ending = beginning + changeWeek

    # Formatting string to enter into the SQL table properly
    if beginning.day<10:
        num = "0" + str(beginning.day)

    else:
        num = str(beginning.day)

    beginning = str(beginning.year) + "-" + str(beginning.month) + "-" + num

    if ending.day<10:
        num2 = "0" + str(ending.day)

    else:
        num2 = str(ending.day)

    ending = str(ending.year) + "-" + str(ending.month) + "-" + num2

    events = db.execute("SELECT name, date, description, start, end, important, weekday FROM events WHERE user_id = ? AND date <= ? AND date >= ? ORDER BY date, start", session["user_id"], ending, beginning)

    return render_template("calendar.html", events=events, beginning=beginning, ending=ending, todayDay=todayDay)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)