from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class EventForm(FlaskForm):
    movieSearch = StringField('Movie', validators=[DataRequired()])
    submit = SubmitField('Submit')
