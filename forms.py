from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField, SelectField, widgets, SelectMultipleField
from wtforms.validators import DataRequired,Email,EqualTo

class SearchForm(FlaskForm):
  search_term = StringField('Search for a pitcher: ', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ul", prefix_label=True)
    option_widget = widgets.CheckboxInput()


class CustomStatsForm(FlaskForm):
    list_of_stats = ['W', 'L', 'SV', 'G', 'GS', 'IP', 'K/9', 'BB/9', 'HR/9',
                         'BABIP','LOB', 'GB', 'HR_FB', 'ERA', 'xERA', 'FIP', 'xFIP', 'WAR']
    # create a list of value/description tuples
    stats_tuples = [(x, x) for x in list_of_stats]
    form = MultiCheckboxField('Label', choices=stats_tuples)
    submit = SubmitField('Submit',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})

# class AddPitcherForm(FlaskForm):
#     list_of_stats = ['Team','W','L','K/9','SIERA']
#     # create a list of value/description tuples
#     stats_tuples = [(x, x) for x in list_of_stats]
#     form = MultiCheckboxField('Label', choices=stats_tuples)
#     submit = SubmitField('Submit',
#                        render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Update')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')