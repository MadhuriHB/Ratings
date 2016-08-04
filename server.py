"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """ Show list of users """
    """ Grabs all the users from the db """
    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/movies")
def movie_list():
    """ Show list of movies """
    """ Grabs all the users from the db """
    movies = Movie.query.all()
    return render_template("movie_list.html", movies=movies)




@app.route("/register", methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route("/processed", methods=["POST"])
def processed_registration():
    print "I made it to registration"
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
   
    new_user = User(email = email, password=password, age=age, zipcode=zipcode)
    print "new_user", new_user

    db.session.add(new_user)
    db.session.commit()
    flash("User added")
    #print "User added"
    return render_template("homepage.html")


@app.route("/signin", methods=["GET"])
def show_signin_form():
    return render_template("sign-in.html")


@app.route("/signin", methods=["POST"])
def signin_process():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session["user_id"] = user.user_id
        flash("Logged in!")
    else:
        flash("If you aren't already registered, please register and then sign-in.")

    
    return render_template("homepage.html")

@app.route("/logout")
def logout_process():
   
    del session["user_id"]

    flash("You are now logged out.")
    
    return render_template("homepage.html")

 
@app.route("/user/<int:user_id>")
def show_user_details(user_id):
    movie_dict = {}
    
    my_user = User.query.get(user_id)
    
    ratings = my_user.ratings
    
    for rating in ratings:
       
        movie = rating.movie
        score = rating.score
        movie_dict[movie] = score


    print movie_list
    return render_template("user_details.html", user=my_user, ratings=ratings)

    





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
