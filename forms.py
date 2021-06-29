from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
from wtforms.fields.core import BooleanField, FloatField
from wtforms.validators import DataRequired, Email, Length

class AddAdmin(FlaskForm):
    """Form for one admin user to add another"""

    name = StringField('User name of prospective admin', validators=[DataRequired()])

class LocationForm(FlaskForm):
    """Form for adding/editing messages."""

    name = StringField('Name of Location', validators=[DataRequired()],  render_kw={"placeholder": "Eg: Indian Creek"})
    location = StringField('Brief description of how to get to location', render_kw={"placeholder": "Eg: An hour south of Moab, UT"})
    latitude = FloatField('Latitude', validators=[DataRequired()], render_kw={"placeholder": "Eg: 38.03535"})
    longitude = FloatField('Longitude', validators=[DataRequired()], render_kw={"placeholder": "Eg: -109.56968"})
    image_url = StringField('(Optional) Image URL', render_kw={"placeholder": "Eg: Indian Creek"})
    description = TextAreaField('Brief description of the area')
    env = RadioField('Climbing Environment', choices=[('sand','Sandstone'), ('alp','Alpine'), ('none', 'Neither')], validators=[DataRequired()])

class LocationEditForm(FlaskForm):
    """Form for adding/editing messages."""

    name = StringField('Name of Location', validators=[DataRequired()],  render_kw={"placeholder": "Eg: Indian Creek"})
    location = StringField('Brief description of how to get to location', render_kw={"placeholder": "Eg: An hour south of Moab, UT"})
    latitude = FloatField('Latitude', validators=[DataRequired()], render_kw={"placeholder": "Eg: 38.03535"})
    longitude = FloatField('Longitude', validators=[DataRequired()], render_kw={"placeholder": "Eg: -109.56968"})
    image_url = StringField('(Optional) Image URL', render_kw={"placeholder": "Eg: Indian Creek"})
    description = TextAreaField('Brief description of the area')
    env = RadioField('Climbing Environment', choices=[('sand','Sandstone'), ('alp','Alpine'), ('none', 'Neither')], validators=[DataRequired()])


class BackcastEditForm(FlaskForm):
    """Form for editing saved backcasts."""

    user_report = TextAreaField('User report')

class CustomBackcastForm(FlaskForm):
    """Form for creating custom backcasts."""

    latitude = FloatField('Latitude:', validators=[DataRequired()])
    longitude = FloatField('Longitude:', validators=[DataRequired()])
    env = RadioField('Climbing Environment', choices=[('sand','Sandstone'), ('alp','Alpine'), ('none', 'Neither')], validators=[DataRequired()])

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditUserProfileForm(FlaskForm):
    """Form for editing user profile."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    bio = StringField('(Optional) Bio')
    password = StringField('Optional for now Password')