"""Flask app for adopt app."""

from flask import Flask, render_template
from models import Pet

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)


# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():

    db.drop_all()
    db.create_all()

    p1 = Pet(name="Spots",species="dog", age='young', photo_url='https://tse3.mm.bing.net/th?id=OIP.qCtOqxrCFWQmBnwwEkJyxQHaHa&pid=Api')
    db.session.add(p1)
    db.session.commit()

    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)