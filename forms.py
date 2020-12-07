from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

avatars = [('https://p.kindpng.com/picc/s/78-786085_robot-01-icon-robot-free-icon-hd-png.png', 'Robot'),
('https://p.kindpng.com/picc/s/78-786416_flat-design-png-avatar-transparent-png.png', 'Dancer with Afro'),
('https://p.kindpng.com/picc/s/78-786705_king-of-fish-avatar-clip-arts-wajah-gambar.png', 'King of Fish'),
('https://p.kindpng.com/picc/s/78-787370_avatar-icon-storybook-unicorn-transparent-icon-unicorn-hd.png', 'Unicorn'),
('https://p.kindpng.com/picc/s/78-787300_grim-reaper-icon-roblox-tower-warfare-hd-png.png', 'Skull'),
('https://p.kindpng.com/picc/s/78-787178_picture-freeuse-computer-icons-emoticon-avatar-clip-silent.png', 'Mouth Taped Shut'),
('https://p.kindpng.com/picc/s/295-2955682_findings-festival-edm-avatar-hd-png-download.png', 'Colorful Mouse'),
('https://p.kindpng.com/picc/s/280-2800820_avatar-beak-beginner-black-cute-emotion-face-linux.png', 'Penguin'),
('https://p.kindpng.com/picc/s/146-1468523_bear-profile-icon-png-download-transparent-png.png', 'Bear'),
('https://p.kindpng.com/picc/s/30-301598_cartoon-santa-hat-free-clip-art-on-santa.png', 'Holiday Bunny'),
('https://img2.pngio.com/default-image-png-picture-710225-default-image-png-default-png-376_356.png', 'Default')]


ratings = [('1',1), ('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7), ('8',8), ('9',9), ('10',10)]

movie_genres = [('None', 'Any'), ('35', 'Comedy'), ('18', 'Drama'), 
('10751', 'Family'), ('9648', 'Mystery')]

tv_genres = [('None', 'Any'), ('10759', 'Action & Adventure'), ('35', 'Comedy'), ('18', 'Drama'), 
('10751', 'Family'), ('9648', 'Mystery'), ('10764', 'Reality')]


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username Max 25 characters*', validators=[DataRequired(), Length(max=25)])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[Length(min=6)])
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