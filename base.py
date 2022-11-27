from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages

from forms import *
import pandas as pd
from generate_chart import generate_chart
import pickle
# import os

df = pd.read_csv('./pitcher_stats.csv').sort_values('Season').round(3)
temp_df = df.drop_duplicates(['Name','playerid'], keep='last')
id_name_dict = dict(zip(temp_df['playerid'],temp_df['Name'])) 
name_id_dict = dict(zip(temp_df['Name'],temp_df['playerid'])) 
last_team_dict = dict(zip(temp_df['playerid'],temp_df['Team'])) 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'

all_stats = df.columns.tolist()
try:
    with open('display_stats.pickle', 'rb') as f:
        display_stats = pickle.load(f)
except:
    display_stats = ['K/9','xFIP']
    with open('display_stats.pickle', 'wb') as f:
        pickle.dump(display_stats, f)

# my_players = []
# search_term = False

@app.route('/', methods=['GET','POST'])
def index():
    search_term = False
    form = SearchForm()
    flash('You can now use the "Customize" tab to tailor what stats are shown to you!', 'info')

    if form.validate_on_submit():
        search_term = form.search_term.data
        pitcher_id = name_id_dict[search_term]
        form.search_term.data = ''
        if pitcher_id is not None:
            return redirect(url_for(f'pitchers', pitcher_id=pitcher_id))

    else: 
        return render_template('index.html', form=form, session=session)

@app.route('/list_of_pitchers', methods=['GET','POST'])
def list_of_pitchers(df=df):
    
    search_term = False
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        pitcher_id = name_id_dict[search_term]
        form.search_term.data = ''
        if pitcher_id is not None:
            return redirect(url_for(f'pitchers', pitcher_id=pitcher_id))

    return render_template('list_of_pitchers.html', form=form, search_term=search_term, session=session, 
                                    display_stats=display_stats, df=df, name_id_dict=name_id_dict, last_team_dict=last_team_dict)


@app.route('/customize', methods=['GET','POST'])
# @login_required
def customize(display_stats=display_stats, df=df):
    search_term = False
    stats_form = CustomStatsForm()
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        pitcher_id = name_id_dict[search_term]
        form.search_term.data = ''
        if pitcher_id is not None:
            return redirect(url_for(f'pitchers', pitcher_id=pitcher_id))
    
    if stats_form.validate_on_submit():            
        if len(stats_form.form.data) <= 2:
            flash('You did not select enough stats. Please select at least 2 to display', 'warning')
        else:
            if len(stats_form.form.data) >= 5:
                flash('You have selected a lot of stats which could lead to being overwhelmed!! Use the "Customize" tab to lower the amount of stats displayed', 'danger')
            display_stats = stats_form.form.data
            with open('display_stats.pickle', 'wb') as f:
                pickle.dump(display_stats, f)
            
            stats_form.form.data = ''
            return render_template('list_of_pitchers.html', df=df, form=form, search_term=search_term, session=session, 
                                    display_stats=display_stats, name_id_dict=name_id_dict, last_team_dict=last_team_dict)

    return render_template('customize.html', form=form, stats_form=stats_form, search_term=search_term, 
                                session=session, display_stats=display_stats)


@app.route('/pitchers/<pitcher_id>', methods=['GET','POST'])
def pitchers(pitcher_id, id_name_dict=id_name_dict):
    search_term = False
    form = SearchForm()
    with open('display_stats.pickle', 'rb') as f:
        display_stats = pickle.load(f)

    if form.validate_on_submit():
        search_term = form.search_term.data
        pitcher_id = name_id_dict[search_term]
        form.search_term.data = ''
        if pitcher_id is not None:
            return redirect(url_for(f'pitchers', pitcher_id=pitcher_id))
    
    if type(pitcher_id) != 'int':
        pitcher_id = int(pitcher_id)
    pitcher_name = id_name_dict[pitcher_id]
    last_team = last_team_dict[pitcher_id]

    if pitcher_id in id_name_dict.keys():
        temp_df = df[df['playerid'] == pitcher_id].sort_values('Season').reset_index()
        table_records = temp_df.to_dict('records')
        len_of_df = len(temp_df)
        img_filename = generate_chart(temp_df, pitcher_name, y_axis="K/9") if len_of_df > 0 else False
        print(img_filename)
        return render_template('pitcher_card.html', form=form, search_term=search_term, 
                                session=session, display_stats=display_stats, img_filename=img_filename,
                                last_team=last_team, pitcher_name=pitcher_name, table_records=table_records)
    else:
        return render_template('404.html', form=form), 404

@app.errorhandler(404)
def page_not_found(e):
    form = SearchForm()
    return render_template('404.html', form=form), 404

if __name__ == "__main__":
    app.run(debug=True)