from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    '''Establishes the app entry point.'''
    return render_template("home.html")

@app.route('/message')
def message():
    '''Sets up a message and selects the recipes.'''
    return render_template("message.html")

@app.route('/inboxSelection')
def inboxSelection():
    '''Shows the available recipes.'''
    return render_template("inboxSelection.html")

@app.route('/inboxes')
def prueba():
    '''Shows the available recipes.'''
    return render_template("inboxes.html")

if __name__ == "__main__":
    app.run()
