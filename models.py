from datetime import date

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
today = date.today()

class Likes(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    review_id = db.Column(
        db.Integer,
        db.ForeignKey('reviews.id', ondelete='cascade')
    )

class Review_Likes(db.Model):
    """Mapping user likes to reviews."""

    __tablename__ = 'review_likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    review_id = db.Column(
        db.Integer,
        db.ForeignKey('reviews.id', ondelete='cascade')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

class Comment(db.Model):
    """Mapping user comments to reviews."""

    __tablename__ = 'comments' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    comment = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=today.strftime("%B/%d/%Y")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    user = db.relationship('User')

    review_id = db.Column(
        db.Integer,
        db.ForeignKey('reviews.id', ondelete='cascade')
    )

    reviews = db.relationship('Review')

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    avatar = db.Column(
        db.Text,
        default="https://img2.pngio.com/default-image-png-picture-710225-default-image-png-default-png-376_356.png",
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    reviews = db.relationship('Review')

    likes = db.relationship(
        'Review',
        secondary="likes"
    )

    comments = db.relationship(
        'Review',
        secondary="comments"
    )

    review_likes = db.relationship(
        'Review',
        secondary="review_likes"
    )

    temp = db.Column(
        db.Text
    )

    def __repr__(self):
        return f'<User #{self.id}: {self.username}, {self.email}>'


    @classmethod
    def signup(cls, username, email, password, avatar):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            avatar=avatar
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Review(db.Model):
    """A review."""

    __tablename__ = 'reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(35),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    text = db.Column(
        db.String(240),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=today.strftime("%B/%d/%Y")
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    user = db.relationship('User')

    comments = db.relationship('Comment')

    likes = db.relationship(
        'User',
        secondary="review_likes"
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
