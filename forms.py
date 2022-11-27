from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets, SelectMultipleField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
  search_term = StringField('Search for a pitcher: ', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ul", prefix_label=True)
    option_widget = widgets.CheckboxInput()


class CustomStatsForm(FlaskForm):
    list_of_stats = ['W', 'L', 'SV', 'G', 'GS', 'IP', 'K/9', 'BB/9', 'HR/9',
                         'BABIP','LOB', 'GB', 'HR_FB', 'ERA','FIP', 'xFIP', 'WAR']
    stats_tuples = [(x, x) for x in list_of_stats]
    form = MultiCheckboxField('Label', choices=stats_tuples)
    submit = SubmitField('Submit',
                       render_kw={'class': 'btn btn-outline-success my-2 my-sm-0'})
