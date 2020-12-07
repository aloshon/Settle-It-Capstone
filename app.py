import os

from flask import Flask, render_template, request, flash, redirect, session, g, make_response
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, ReviewForm, CommentForm, EditReviewForm, DeleteReviewForm, SessionTvForm, SessionMovieForm
from models import db, connect_db, User, Review, Comment
import string

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///settle_it'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# generate a random secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                avatar=form.avatar.data or User.avatar.default.arg
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Successfully logged out!", 'success')
    return redirect("/login")

##############################################################################
# General routes:

@app.route('/')
def start_page():
    """Render start page"""
    if g.user:
        user = User.query.get_or_404(g.user.id)

        return render_template('home.html', user=user)

    return redirect('/signup')

@app.route('/search/reviews')
def get_searched_reviews():
    """Page with the list of users based on the query"""

    search = request.args.get('q')

    if not search:
        reviews = Review.query.order_by(Review.timestamp.desc()).limit(100).all()
    else:
        reviews = Review.query.filter(Review.title.ilike(f"%{search}%")).order_by(Review.timestamp.desc()).all()

    return render_template('reviews/list_reviews.html', reviews=reviews, search=search)

##############################################################################
# User routes:

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    # snagging reviews in order from the database;
    reviews = (Review
                .query
                .filter(Review.user_id == user_id)
                .order_by(Review.timestamp.desc())
                .all())
    
    return render_template('users/user_details.html', user=user, reviews=reviews)

@app.route('/users/edit', methods=["GET", "POST"])
def profile():
    """Edit profile for the current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserAddForm(obj=g.user)
    user_id = g.user.id

    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.avatar = form.avatar.data
        if User.authenticate(form.username.data, form.password.data) != g.user:
            flash("Incorrect password", "danger")
            return redirect("/")

        db.session.add(g.user)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")
    return render_template("users/edit_user.html", form=form, user_id=user_id)

@app.route('/users/likes/<int:user_id>')
def list_liked_reviews(user_id):
    """Generate page that lists all the reviews the user has liked."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('users/user_likes.html', user=user, likes=user.likes)

@app.route('/users/delete', methods=["GET", "POST"])
def delete_user():
    """Delete a user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = DeleteUserForm()

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data) != g.user:
            flash("Incorrect password", "danger")
            return redirect("/")
        
        do_logout()

        db.session.delete(g.user)
        db.session.commit()

        return redirect("/signup")

    return render_template("users/user_delete.html", form=form)

##############################################################################
# Review routes:

@app.route('/reviews/add', methods=["GET", "POST"])
def add_review():
    """If GET: Generate page with form to write a review about a movie.
    If POST: Add review to database and redirect to 
    """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            title=string.capwords(form.name.data),
            rating=form.rating.data,
            text=form.text.data)
        g.user.reviews.append(review)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('reviews/add_review.html', form=form)

@app.route('/reviews/<int:review_id>', methods=["GET"])
def show_review_details(review_id):
    """Show a specific review."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = Review.query.get(review_id)
    return render_template('reviews/review_details.html', review=review)

@app.route('/reviews/add_like/<int:review_id>', methods=["POST"])
def like_message(review_id):
    """Add like to review"""

    if not g.user:
        flash("Must be logged in to add a like!", "danger")
        return redirect("/")

    liked_review = Review.query.get_or_404(review_id)
    if liked_review in g.user.likes:
        g.user.likes.remove(liked_review)
        liked_review.likes.remove(g.user)
        db.session.commit()

    else: 
        g.user.likes.append(liked_review)
        liked_review.likes.append(g.user)
        db.session.commit()

    return '', 204

@app.route('/reviews/<int:review_id>/edit', methods=["GET", "POST"])
def edit_review(review_id):
    """GET generates form for updating review. POST updates it."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = Review.query.get_or_404(review_id)
    form = EditReviewForm(obj=review)
    if g.user.id != review.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data) != g.user:
            flash("Incorrect password", "danger")
            return redirect("/")
        review.title = string.capwords(form.name.data)
        review.text = form.text.data
        review.rating = form.rating.data

        db.session.add(review)
        db.session.commit()

        return redirect(f"/reviews/{review_id}")
    return render_template("reviews/edit_review.html", form=form, review=review)

@app.route('/reviews/<int:review_id>/delete', methods=["GET", "POST"])
def remove_review(review_id):
    """Delete a review."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = Review.query.get(review_id)
    form = DeleteReviewForm()
    if review.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data) != g.user:
            flash("Incorrect password", "danger")
            return redirect("/")

        db.session.delete(review)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template("reviews/delete_review.html", form=form)

##############################################################################
# Comment routes:

@app.route('/users/add_comment/<int:review_id>', methods=["GET", "POST"])
def create_comment(review_id):
    """
    If GET then return form for making a comment. 
    If POST then send comment to database and redirect to review details
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    review = Review.query.get_or_404(review_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data,
                            user_id=g.user.id)
        review.comments.append(comment)
        db.session.commit()

        return redirect(f"/reviews/{review_id}")
    
    
    return render_template('add_comment.html', form=form, review=review)

@app.route('/comments/<int:comment_id>/delete', methods=["POST"])
def delete_comment(comment_id):
    """Delete comment"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(comment)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")

##############################################################################
# Session routes:

@app.route('/session/tv/form', methods=["GET", "POST"])
def session_tv_form():
    """GET generates tv form. POST sends inputs to the session."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SessionTvForm()

    if form.validate_on_submit():

        return redirect("/instructions")

    return render_template("session/session_form.html", form=form)

@app.route('/session/movie/form', methods=["GET", "POST"])
def session_movie_form():
    """GET generates movie form. POST sends inputs to the session."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SessionMovieForm()

    if form.validate_on_submit():

        return redirect("/instructions")

    return render_template("session/session_form.html", form=form)

@app.route('/instructions')
def explain_session():
    """Explain how the session works."""
    if not g.user:

        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("session/session_explanation.html")

@app.route('/settle/it')
def start_session():
    """Start settle it session"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("session/session.html")

@app.route('/session/end')
def display_settled_title():
    """Get title that was settled on and display it"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("session/session_end.html")

@app.route('/session/stopped')
def session_too_long():
    """Notify the user that they have browsed hundreds of titles and suggest trying something new"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("session/session_stopped.html")