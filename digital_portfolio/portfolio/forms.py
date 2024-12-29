from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PorfolioForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    tech_skills = TextAreaField('Technical Skills', validators=[DataRequired()])
    work_produced = TextAreaField('Work Produced to Date', validators=[DataRequired()])
    experience = TextAreaField('Work Experience', validators=[DataRequired()])
    contact = StringField('Contact Details', validators=[DataRequired()])
    submit = SubmitField('Complete')

class CommentForm(FlaskForm):
    content = TextAreaField('Would you like to leave any comments?')
    submit = SubmitField('Comment')