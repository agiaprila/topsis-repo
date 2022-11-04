from topsis import topsis
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)

app.secret_key = "Rahasia Bos"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rate_umkm'

@app.route('/')
def home() :
    return render_template("home.html")

@app.route('/topsis', methods=['POST', 'GET'])
def topsis():
    cur = mysql.connection.cursor()
    cur.execute("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 FROM bawang")
    data = cur.fetchall()
    cur.close()
    evaluation_matrix = [list(data) for data in data]
    weights = [5,4,5,5,5,4,4,2,2,3]
    criterias = [1,1,0,1,1,1,0,1,0,0]
    decision = topsis(evaluation_matrix, weights, criterias)
    print(decision)
    return render_template('topsis.html')

@app.route('/data')
def data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bawang")
    data = cur.fetchall()
    cur.close()
    return render_template('data.html', data=data)


@app.route('/insert', methods = ['POST', 'GET'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        Nama = request.form['Nama']
        C1 = request.form['C1']
        C2 = request.form['C2']
        C3 = request.form['C3']
        C4 = request.form['C4']
        C5 = request.form['C5']
        C6 = request.form['C6']
        C7 = request.form['C7']
        C8 = request.form['C8']
        C9 = request.form['C9']
        C10 = request.form['C10']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bawang (Nama, C1, C2,C3,C4,C5,C6,C7,C8,C9,C10) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s)", (Nama, C1, C2,C3,C4,C5,C6,C7,C8,C9,C10))
        mysql.connection.commit()
        return redirect(url_for('data'))
    return render_template('insert.html')


@app.route('/delete/<int:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    sql= f"""delete from bawang where id={id_data}; """
    cur.execute(sql)
    mysql.connection.commit()
    return redirect(url_for('data'))



if __name__ == '__main__':
    app.run(debug=True)
