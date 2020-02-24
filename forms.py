from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    hide = BooleanField('Hide', default=False)
    order_number = StringField('Order number', validators=[DataRequired()])
    overlay_title = StringField('Overlay Title', validators=[DataRequired()])
    overlay_text = StringField('Overlay Text', validators=[DataRequired()])
    link = StringField('Link', default='#')
    submit = SubmitField('Add Project')
