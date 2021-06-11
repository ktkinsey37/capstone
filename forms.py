from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.core import BooleanField, FloatField
from wtforms.validators import DataRequired, Email, Length


class SpecialLocationForm(FlaskForm):
    """Form for adding/editing messages."""

    name = StringField('Name of Location', validators=[DataRequired()],  render_kw={"placeholder": "Indian Creek"})
    location = StringField('Brief description of how to get to location', render_kw={"placeholder": "An hour south of Moab, UT"})
    latitude = FloatField('Latitude, eg: 35.145645', validators=[DataRequired()])
    longitude = FloatField('Longitude, eg: 35.145645', validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')
    description = TextAreaField('Brief description of the area', validators=[DataRequired()])
    is_desert = BooleanField('Is this a Sandstone location?')
    is_snowy = BooleanField('Is this an alpine location?')


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