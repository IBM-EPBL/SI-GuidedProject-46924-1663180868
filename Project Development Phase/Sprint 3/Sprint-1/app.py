from flask import Flask,render_template,request,url_for,flash,redirect,session


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/login")
def login():
	return render_template('login.html')
@app.route("/signin")
def signin():
	return render_template('signin.html')
    
if __name__ == '__main__':
    app.run(debug=True)
