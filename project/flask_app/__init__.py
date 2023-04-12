from flask import Flask, render_template, redirect, request, session
import pickle
import psycopg2
import os
import pandas as pd
import numpy as np

base_dir = os.getcwd()
host = 'ziggy.db.elephantsql.com'
user = 'nxsyeowh'
password = 'TgTJdb-06koQQ569eLOr_u2gSqKnwVIC'
database = 'nxsyeowh'

con = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database)

with open('model.pkl', 'rb') as pickle_file:
    model=pickle.load(pickle_file)

app = Flask(__name__)
price = None
body = None
tannin = None
sweetness = None
acidity = None
features = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redwine')
def redwine():
    return render_template('index2.html')

@app.route('/send-features', methods=['POST'])
def submit_features():
    global price, body, tannin, sweetness, acidity
    # features = []
    # for feature in ['price', 'body', 'tannin', 'sweetness', 'acidity']:
    #     temp = request.form[feature]
    #     temp = int(temp)
    #     features.append(temp)
    price = request.form['price']
    price = int(price)

    body = request.form['body']
    body = int(body)

    tannin = request.form['tannin']
    tannin = int(tannin)

    sweetness = request.form['sweetness']
    sweetness = int(sweetness)

    acidity = request.form['acidity']
    acidity = int(acidity)
    
    return redirect('/redwine/predict')
    
    
@app.route('/redwine/predict')
def redwine_predict():
    global price, body, tannin, sweetness, acidity
    test = pd.DataFrame(columns=['price', 'body', 'tannin', 'sweetness', 'acidity'])
    test = test.append({'price': price, 'body' : body, 'tannin' : tannin, 'sweetness' : sweetness, 'acidity' : acidity}, ignore_index=True)
    test = test.astype('int')
    reco = np.exp(model.predict(test)[0])
    
    

    cur = con.cursor()    
    cur.execute(f"""SELECT w.name, w.score
            FROM wine w 
            ORDER BY ABS(w.score-{reco}) """)
    
    wine1 = cur.fetchone()
    wine_name1 = wine1[0]
    wine_score1 = wine1[1]
    wine2 = cur.fetchone()
    wine_name2 = wine2[0]
    wine_score2 = wine2[1]
    wine3 = cur.fetchone()
    wine_name3 = wine3[0]
    wine_score3 = wine3[1]
    
    cur.close()
    return render_template('index3.html', wine_name1 = wine_name1, wine_name2 = wine_name2, wine_name3 = wine_name3, wine_score1=wine_score1, wine_score2=wine_score2, wine_score3=wine_score3)

@app.route('/dashboard')
def dashboard():
    cur = con.cursor()    
    cur.execute(f"""select name
                    from wine
                    order by score desc, price asc 
                    limit 1""")
    
    best = cur.fetchone()[0]
    
    cur.close()

    cur = con.cursor()
    cur.execute("""select avg(score)
                from wine w 
                group by w.price """)
    data1 = [
        ("~5만원", cur.fetchone()[0]),
        ("5만원 ~ 10만원", cur.fetchone()[0]),
        ("10만원 ~ 15만원", cur.fetchone()[0]),
        ("15만원~", cur.fetchone()[0]),
    ]
    data1_labels = [row[0] for row in data1]
    data1_values = [row[1] for row in data1]

    cur.close()

    return render_template('dashboard.html', best = best, data1_labels=data1_labels, data1_values=data1_values)