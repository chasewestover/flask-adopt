"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash
from models import Pet

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

from forms import AddPetForm, EditPetForm

import requests

from pet_finder import get_random_pet, update_auth_token_string




app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

auth_token = None


# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

#when re-running the server empty the db and create one pet
db.drop_all()
db.create_all()
p1 = Pet(name="Spots", species="dog", age='young', photo_url='https://tse3.mm.bing.net/th?id=OIP.qCtOqxrCFWQmBnwwEkJyxQHaHa&pid=Api')
db.session.add(p1)
db.session.commit()


@app.before_first_request
def refresh_credentials():
    """Just once, get token and store it globally."""
    global auth_token
    auth_token = update_auth_token_string()


@app.route("/")
def show_homepage():
    """Display the homepage, and show all the pets. """

    pets = Pet.query.all()
    global auth_token
    random_pet = get_random_pet(auth_token)

    return render_template("homepage.html", pets=pets, random_pet = random_pet)


@app.route("/add", methods=["GET", "POST"])
def show_pet_form():
    """ render the add pet form """
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data or None
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, age=age, photo_url=photo_url, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Pet {name} added!")
        return redirect("/")

    return render_template("add_pet_form.html", form = form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_pet_details(pet_id):
    """ render pet page"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data or None
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect("/")

    return render_template("pet_detail.html", pet=pet, form=form)

