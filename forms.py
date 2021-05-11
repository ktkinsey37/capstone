from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SpecialLocationForm(FlaskForm):
    """Form for adding/editing messages."""

    name = TextAreaField('text', validators=[DataRequired()])
    location = 
    coordinates = 
    image_url = 
    description = 
    is_desert = 
    is_snowy = 


# class UserAddForm(FlaskForm):
#     """Form for adding users."""

#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[Length(min=6)])
#     image_url = StringField('(Optional) Image URL')


# class LoginForm(FlaskForm):
#     """Login form."""

#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[Length(min=6)])

# class EditUserProfileForm(FlaskForm):
#     """Form for editing user profile."""

#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     image_url = StringField('(Optional) Image URL')
#     header_image_url = StringField('(Optional) Header Image URL')
#     bio = StringField('(Optional) Bio')
#     password = StringField('Optional for now Password')