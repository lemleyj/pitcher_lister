from flask import Flask, render_template, request, session, redirect, url_for, flash, get_flashed_messages
from flask_session import Session

from forms import *
import pandas as pd
from generate_chart import generate_chart

df = pd.read_csv('pitcher_stats.csv')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

all_stats = df.columns.tolist()
display_stats = ['Team','K/9','SIERA']
my_players = []
search_term = False

@app.route('/', methods=['GET','POST'])
def index():
    search_term = False
    form = SearchForm()
    flash('You can now use the "Customize" tab to tailor what stats are shown to you!', 'info')

    if form.validate_on_submit():
        search_term = form.search_term.data
        temp_df = df[df['Name'] == search_term].sort_values('Season')
        len_of_df = len(temp_df)
        img_filename = generate_chart(temp_df, search_term, y_axis="K/9") if len_of_df > 0 else False
        form.search_term.data = ''
        
        return render_template('search.html', img_filename=img_filename, len_of_df=len_of_df, tables=[temp_df.to_html(classes='data',header="true", table_id="table",index=False)], 
                                            titles=temp_df.columns.values, form=form, search_term=search_term, display_stats=display_stats, df=df)
    
    else: 
        return render_template('index.html', form=form, session=session)

@app.route('/list_of_pitchers', methods=['GET','POST'])
def list_of_pitchers(df=df):
    
    search_term = False
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        temp_df = df[df['Name'] == search_term].sort_values('Season')
        len_of_df = len(temp_df)
        img_filename = generate_chart(temp_df, search_term, y_axis="K/9") if len_of_df > 0 else False
        form.search_term.data = ''
        
        return render_template('search.html', img_filename=img_filename, len_of_df=len_of_df, tables=[temp_df.to_html(classes='data',header="true", table_id="table",index=False)], 
                                            titles=temp_df.columns.values, form=form, search_term=search_term, display_stats=display_stats, df=df)

    return render_template('list_of_pitchers.html', form=form, search_term=search_term, session=session, 
                                    display_stats=display_stats, df=df)

@app.route('/search', methods=['GET','POST'])
def search():
    
    search_term = False
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        temp_df = df[df['Name'] == search_term].sort_values('Season')
        len_of_df = len(temp_df)
        img_filename = generate_chart(temp_df, search_term, y_axis="K/9") if len_of_df > 0 else False
        form.search_term.data = ''
        
        return render_template('search.html', img_filename=img_filename, len_of_df=len_of_df, tables=[temp_df.to_html(classes='data',header="true", table_id="table",index=False)], 
                                            titles=temp_df.columns.values, form=form, search_term=search_term, display_stats=display_stats, df=df)
    
    return render_template('search.html', form=form, search_term=search_term, session=session, len_of_df=0)


@app.route('/customize', methods=['GET','POST'])
def customize(display_stats=display_stats, df=df):
    search_term = False
    stats_form = CustomStatsForm()
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        temp_df = df[df['Name'] == search_term].sort_values('Season')
        len_of_df = len(temp_df)
        img_filename = generate_chart(temp_df, search_term, y_axis="K/9") if len_of_df > 0 else False
        form.search_term.data = ''
        
        return render_template('search.html', img_filename=img_filename, len_of_df=len_of_df, tables=[temp_df.to_html(classes='data',header="true", table_id="table",index=False)], 
                                            titles=temp_df.columns.values, form=form, search_term=search_term, display_stats=display_stats, df=df)
    
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
            return render_template('list_of_pitchers.html', df=df, form=form, search_term=search_term, session=session, 
                                    display_stats=display_stats)

    return render_template('customize.html', form=form, stats_form=stats_form, search_term=search_term, 
                                session=session, display_stats=display_stats)

## TODO: Create player card for individual pitchers instead of using the search.html page
@app.route('/pitchers/<name>', methods=['GET','POST'])
def pitchers(name):
    return f"You searched for {name}"    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)