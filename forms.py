from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

avatars = [('https://img2.pngio.com/default-image-png-picture-710225-default-image-png-default-png-376_356.png', 'Default'),
('https://cdn.pixabay.com/photo/2020/10/08/19/32/snowman-5638857__480.png', 'Angry Snowman'),
('https://cdn.pixabay.com/photo/2016/03/31/20/27/avatar-1295773__480.png', 'Dog'),
('https://cdn.pixabay.com/photo/2016/12/13/16/17/dancer-1904467__480.png', 'Dancing Afro Dude'),
('https://cdn.pixabay.com/photo/2016/03/31/21/40/angry-1296580__480.png', 'King of Fish'),
('https://cdn.pixabay.com/photo/2013/07/12/15/34/character-150095__480.png', 'Gasping'),
('https://cdn.pixabay.com/photo/2016/03/31/19/56/avatar-1295399__480.png', 'Penguin'),
('https://cdn.pixabay.com/photo/2017/02/01/11/19/cartoon-chips-2029737__480.png', 'French Fries'),
('https://cdn.pixabay.com/photo/2012/04/12/20/24/skull-30511__480.png', 'Top Hat Skull'),
('https://cdn.pixabay.com/photo/2020/01/14/10/55/cartoon-4764726__480.png', "Vibin'n Pineapple")]


ratings = [('1',1), ('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7), ('8',8), ('9',9), ('10',10)]

movie_genres = [('None', 'Any'), ('35', 'Comedy'), ('18', 'Drama'), 
('10751', 'Family'), ('9648', 'Mystery')]

tv_genres = [('None', 'Any'), ('10759', 'Action & Adventure'), ('35', 'Comedy'), ('18', 'Drama'), 
('10751', 'Family'), ('9648', 'Mystery'), ('10764', 'Reality')]


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username Max 25 characters*', validators=[DataRequired(), Length(max=25)])
    email = StringField('Email*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=6)])
    avatar = SelectField('Select an Avatar', choices=avatars)


class EditUserForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username Max 25 characters*', validators=[DataRequired(), Length(max=25)])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=6)])
    avatar = SelectField('Select an Avatar', choices=avatars)


class DeleteUserForm(FlaskForm):
    """Form to ensure the user wants to delete their profile."""

    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class ReviewForm(FlaskForm):
    """Form for adding/editing reviews."""

    name = TextAreaField('Name of show or movie', validators=[DataRequired(), Length(max=35)])
    text = TextAreaField('Your thoughts? 240 characters max', validators=[DataRequired(), Length(max=240)])
    rating = SelectField('How would you rate it?', choices=ratings)

class CommentForm(FlaskForm):
    """Form for adding/editing comments."""

    comment = TextAreaField('comment', validators=[DataRequired()])


class EditReviewForm(FlaskForm):
    """Form for adding/editing reviews."""

    name = TextAreaField('Name of show or movie', validators=[DataRequired(), Length(max=35)])
    text = TextAreaField('Your thoughts', validators=[DataRequired(), Length(max=240)])
    rating = SelectField('How would you rate it?', choices=ratings)
    password = PasswordField('Password', validators=[Length(min=6)])


class DeleteReviewForm(FlaskForm):
    """Form to ensure user wants to delete their review."""

    password = PasswordField('Password', validators=[Length(min=6)])


class SessionTvForm(FlaskForm):
    """Form for TV session inputs"""

    genre = SelectField('Select a genre', choices=tv_genres)


class SessionMovieForm(FlaskForm):
    """Form for movie session inputs"""

    genre = SelectField('Select a genre', choices=movie_genres)