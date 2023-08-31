from flask import Flask, render_template, request
import mysql.connector
import hashlib

app = Flask(__name__)

def connect():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="login"
        )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        connection = connect()
        cursor = connection.cursor()
        query = "SELECT * FROM login WHERE username='" + username + "' AND password='" + password + "'"
        cursor.execute(query)
       #query = "SELECT * FROM login WHERE username = %s AND password = %s"
        #cursor.execute(query, (username, password))
        result = cursor.fetchall()
        print(result)
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error in the database connection", err)
    if len(result) == 0:
          return render_template('register.html')
    else:
        return render_template('datas.html', users=result)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        connection2 = connect()
        cursor = connection2.cursor()
        sql = "INSERT INTO login (username,password,email) VALUES (%s, %s, %s)"
        values = (username, password, email)
        cursor.execute(sql, values)
        cursor.close()
        connection2.commit()
        connection2.close()

    except mysql.connector.Error as err:
        print("Error in the database connection", err)
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)

