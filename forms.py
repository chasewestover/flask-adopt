"""Forms for adopt app."""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, Email, URL, Optional, AnyOf

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), AnyOf(['cat','dog', 'porcupine'])])
    age = SelectField('Age',
        choices=[('baby', 'Baby'), ('young', 'Young'), ('adult', 'Adult'), ('senior', 'Senior')])
    photo_url = StringField("Photo URL:",
        validators=[Optional(),URL()])
    notes = StringField("Notes")

class EditPetForm(FlaskForm):
    """Form for editing pets."""

    photo_url = StringField("Photo URL:",
        validators=[Optional(), URL()])
    notes = StringField("Notes")
    available = BooleanField()