from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    movieSearch = StringField('Movie', validators=[DataRequired()])
    submit = SubmitField('Submit')

