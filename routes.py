from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", help="Postgres pwd")
args = parser.parse_args()
pwd = args.password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://pgadmin:' + str(pwd) + '@localhost/learningflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
  return render_template('index.html')


@app.route("/about")
def about():
  return render_template('about.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
      return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      return 'Success!'

  elif request.method == "GET":
    return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
      return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home", methods=["GET", "POST"])
def home():
    print(session)

    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('home.html', form=form)
        else:
            # get the address
            address = form.address.data

            # query for places around it
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            # return those results
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

    elif request.method == 'GET':
        return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)

