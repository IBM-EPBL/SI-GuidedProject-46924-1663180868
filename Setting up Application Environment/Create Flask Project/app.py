from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return 'Hello %s!' % name



if __name__ == '__main__':
    app.run( debug=True )