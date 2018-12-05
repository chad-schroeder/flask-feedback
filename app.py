from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from secrets import FEEDBACK_API_KEY, DATABASE_URI
from werkzeug.exceptions import Unauthorized

from models import db, connect_db, User
from forms import AddUserForm, UserLoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = FEEDBACK_API_KEY
DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route("/")
def homepage():
    """Redirect to /register."""

    # check if the user is logged in
    if session.get("user_id"):
        username = session.get("user_id")
        return redirect(f"/users/{username}")
    else:
        return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def registration():
    """Register user."""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            # in case a unique constraint was violated
            form.username.errors = ["Username already exists."]
            return render_template("register.html", form=form)

        # log in the user to the session
        session["user_id"] = user.username

        # redirect to secret page for newly-registered user
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def user_login():
    """Login user."""

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)


@app.route("/users/<username>")
def secret_location(username):
    """Secret location."""

    # user_username must be in session to be logged in
    if "user_id" not in session or session["user_id"] != username:
        raise Unauthorized()

    else:
        user = User.query.filter_by(username=username).first()

        return render_template("secret.html", user=user)


@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    """Delete a user."""

    if "user_id" not in session or session["user_id"] != username:
        raise Unauthorized()

    else:
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()

        return redirect("/logout")


@app.route("/logout")
def logout_user():
    """Log out the user."""

    session.clear()

    return redirect("/")
