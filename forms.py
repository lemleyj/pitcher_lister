from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, widgets, SelectMultipleField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
  search_term = StringField('Search for a pitcher: ', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})


# class CustomStatsForm(FlaskForm):
#   list_of_stats = SelectField(u'Choose your stats: ', 
#                           choices=[('Team','Team'),('W','W'),('L','L'),('K/9','K/9'),('SIERA','SIERA')	
#                                   ]
#                               )
#   submit = SubmitField('Submit',
#                        render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CustomStatsForm(FlaskForm):
    # list_of_stats = ['Team','W','L','K/9','SIERA']
    list_of_stats = ['Season', 'Team', 'W', 'L', 'SV', 'G', 'GS', 'IP', 'K/9', 'BB/9', 'HR/9',
                         'BABIP','LOB', 'GB', 'HR_FB', 'ERA', 'xERA', 'FIP', 'xFIP', 'WAR']
    # create a list of value/description tuples
    stats_tuples = [(x, x) for x in list_of_stats]
    example = MultiCheckboxField('Label', choices=stats_tuples)
    submit = SubmitField('Submit',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})

class AddPitcherForm(FlaskForm):
    list_of_stats = ['Team','W','L','K/9','SIERA']
    # create a list of value/description tuples
    stats_tuples = [(x, x) for x in list_of_stats]
    example = MultiCheckboxField('Label', choices=stats_tuples)
    submit = SubmitField('Submit',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})