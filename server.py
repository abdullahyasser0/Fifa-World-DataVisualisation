from flask import Flask, jsonify, render_template,request
import sqlite3 as sql
import pandas as pd
from sqlalchemy import create_engine
from sqlite3 import Error

def create_connection (db_file):
    conn = None
    try:
        conn = sql.connect (db_file)
    except Error as e:
        print(e)
    return conn

db_url = 'sqlite:///Fifa.db'
engine = create_engine(db_url, echo=True)
df = pd.read_sql( 'select * from Fifa_Data', engine)
# print (df_2)

# con = sql.connect("Fifa.db")
# df = pd.read_sql_query ("select * from Fifa_Data ",con)

df["index"] = df["index"].sort_values()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secoundPage')
def secoundPage():
    return render_template('secoundpage.html')

@app.route('/get-pieChart')
def get_datachart():
    category = df["Preferred Foot"].value_counts().index
    values = df["Preferred Foot"].value_counts().values
    data = [{"category": c, "value": int(v)} for c, v in zip(category, values)]
    #print(data)
    return jsonify(data)

@app.route('/get-BarChart')
def get_datachar1t():
    dfn = pd.read_sql_query ("SELECT Nationality, COUNT(*) AS Counter FROM Fifa_Data where Overall>80 GROUP BY Nationality; ",engine)
    dfn=dfn.sort_values(by='Counter',ascending=False)
    category = dfn["Nationality"]
    values = dfn["Counter"]
    data = [{"country": c, "value": int(v)} for c, v in zip(category, values)]
    return jsonify(data[:10])

@app.route('/get-wordMap')
def get_datachart3():
    category = df["cCode"].value_counts().index
    values = df["cCode"].value_counts().values
    data = [{"id": c,"name":c, "value": int(v)} for c, v in zip(category, values)]
    print(len(data))
    return jsonify(data)

@app.route('/get-coolCol',methods =["POST"])
def get_datachart4():
    country= request.form.get("country")
    df4 = pd.read_sql_query (f"SELECT Position, Overall FROM Fifa_Data where Nationality like'%{country}' ",engine)
    df1=df4.groupby(['Position'])["Overall"].mean()
    category = df1.index 
    values = df1.values
    data = [{"country": c, "value": int(v)} for c, v in zip(category, values)]
    return jsonify(data)

@app.route('/get-person',methods =["POST"])
def get_datachart6():
    name = request.form.get("fname")
    print(name)
    dfn = pd.read_sql_query (f"SELECT HeadingAccuracy,Jumping,Reactions,Acceleration,Finishing  FROM Fifa_Data where Name like'%{name}'",engine)
    category = dfn.columns.tolist()
    data = []
    for i,c in enumerate(category):
        item = {
            "value": int(dfn[c]),
            "category": c,
        }
        data.append(item)
    return jsonify(data)


@app.route('/get-coolPie',methods =["POST"])
def get_datachart5():
    name = request.form.get("fname")
    print(name)
    dfn = pd.read_sql_query (f"SELECT SprintSpeed,Ballcontrol,ShortPassing,Dribbling,Curve  FROM Fifa_Data where Name like'%{name}'",engine)
    category = dfn.columns.tolist()
    data = []
    for i,c in enumerate(category):
        item = {
            "category": c,
            "value": int(dfn[c]),
            "full": 100,  
            "columnSettings": {
                "fill": "chart.get('colors').getIndex(3)"
            }
        }
        data.append(item)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

