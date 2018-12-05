from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email, Length


class AddUserForm(FlaskForm):
    """Add user form."""

    username = StringField(
        "Username", validators=[InputRequired(),
                                Length(min=1, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField(
        "Email", validators=[InputRequired(),
                             Length(min=1, max=50),
                             Email()])
    first_name = StringField(
        "First Name", validators=[InputRequired(),
                                  Length(min=1, max=30)])
    last_name = StringField(
        "Last Name", validators=[InputRequired(),
                                 Length(min=1, max=30)])


class UserLoginForm(FlaskForm):
    """Log user in."""

    username = StringField(
        "Username", validators=[InputRequired(),
                                Length(min=1, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])


class AddFeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField(
        "Title", validators=[InputRequired(),
                             Length(min=1, max=100)])
    content = TextAreaField("Content", validators=[InputRequired()])
