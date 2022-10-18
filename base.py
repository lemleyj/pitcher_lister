from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages
from flask_session import Session

from forms import *
import pandas as pd

df = pd.read_csv('pitcher_stats.csv')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

players = {
            "Justin Verlander":{
                            'Team':"Houston Astros",
                            'W':'15',
                            'L':'1',
                            'K/9':"9.5",
                            'SIERA':'2.1'
                                },
            "Yu Darvish":{
                            'Team':"San Diego Padres",
                            'W':'13',
                            'L':'4',
                            'K/9':"9.0",
                            'SIERA':'3.4'
                                },
            "Shoehei Ohtani":{
                            'Team':"Los Angeles Angels",
                            'W':'6',
                            'L':'0',
                            'K/9':"15.0",
                            'SIERA':'1.1'
                                },
                        }

all_stats =  ['Team','W','L','K/9','SIERA']
display_stats = ['Team','K/9','SIERA']
my_players = []
search_term = False

# session['all_stats'] =  ['Team','W','L','K/9','SIERA']
# session['display_stats'] = ['Team','K/9','SIERA']
# session['my_players'] = []
# session['search_term'] = False

@app.route('/', methods=['GET','POST'])
def index():
    search_term = False
    form = SearchForm()
    flash('You can now use the "Customize" tab to tailor what stats are shown to you!', 'info')

    if form.validate_on_submit():
        search_term = form.search_term.data
        form.search_term.data = ''
        return render_template('search.html', form=form, search_term=search_term, players=players, display_stats=display_stats)
    
    else: 
        return render_template('index.html', form=form, session=session)

@app.route('/list_of_pitchers', methods=['GET','POST'])
def list_of_pitchers():
    
    search_term = False
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        form.search_term.data = ''
        return render_template('search.html', form=form, search_term=search_term, players=players, display_stats=display_stats)

    return render_template('list_of_pitchers.html', form=form, search_term=search_term, session=session, 
                                    players=players, display_stats=display_stats)

@app.route('/search', methods=['GET','POST'])
def search():
    
    search_term = False
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        form.search_term.data = ''
        return render_template('search.html', form=form, search_term=search_term, players=players, display_stats=display_stats)
    
    return render_template('search.html', form=form, search_term=search_term, session=session)


@app.route('/customize', methods=['GET','POST'])
def customize(display_stats=display_stats):
    search_term = False
    stats_form = CustomStatsForm()
    form = SearchForm()


    if form.validate_on_submit():
        search_term = form.search_term.data
        form.search_term.data = ''
        return render_template('search.html', form=form, search_term=search_term, players=players, display_stats=display_stats)

    if stats_form.validate_on_submit():            
        if len(stats_form.example.data) < 2:
            flash('You did not select enough stats. Please select at least 2 to display', 'warning')
            return render_template('customize.html', form=form, stats_form=stats_form, search_term=search_term, 
                                session=session, display_stats=display_stats)
        else:
            flash('If you wish to revert back to default, simply click the "List of Pitchers" tab at the top and it will reset', 'secondary')
            if len(stats_form.example.data) >= 5:
                flash('You have selected all the stats which could lead to being overwhelmed!! Use the "Customize" tab to lower the amount of stats displayed', 'danger')
            display_stats = stats_form.example.data
            stats_form.example.data = ''
            return render_template('list_of_pitchers.html', form=form, search_term=search_term, session=session, 
                                    players=players, display_stats=display_stats)

    return render_template('customize.html', form=form, stats_form=stats_form, search_term=search_term, 
                                session=session, display_stats=display_stats)

# @app.route('/my_team', methods=['GET','POST'])
# def my_team():
#     search_term = False
#     stats_form = CustomStatsForm()
#     form = SearchForm()

#     if form.validate_on_submit():
#         search_term = form.search_term.data
#         form.search_term.data = ''
#         return render_template('search.html', form=form, search_term=search_term, players=players, display_stats=display_stats)

#     return render_template('my_team.html', form=form, stats_form=stats_form, search_term=search_term, 
#                                     session=session, my_players=my_players, len=len, players=players)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)