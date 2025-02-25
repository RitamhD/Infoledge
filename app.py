from flask import Flask, render_template, url_for, redirect, request, session
import mysql.connector


app = Flask(__name__, template_folder='view')

@app.route('/')
def landing_page():
    return render_template('landing_page.html')



if __name__=='__main__':
    app.run(debug=True)