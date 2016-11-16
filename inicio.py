from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    '''Establishes the app entry point.'''
    return render_template("home.html")

@app.route('/message')
def message():
    '''Sets up a message and selects the recipes.'''
    return render_template("message.html")


#**************
# REST backend
#**************
@app.route('/api/v1.0/contacts/all', methods=['GET'])
def get_all_contacts():
    '''Returns all the database contacts.'''
    #TODO: Have to implement this method ASAP.
    resultado = "Completar con la funcionalidad adecuada!"
    return jsonify({'resultado': { \
    'resulta': resultado \
    }}),200
    #return jsonify(resultado)

@app.route('/api/v1.0/contacts/load/linkedin/<string:dataFile>', methods=['GET'])
def post_load_linkedin_contacts(dataFile):
    '''Loads a all the database contacts.'''
    #TODO: Have to implement this method ASAP.
    resultado = "Completar con la funcionalidad de carga del archivo desde linkedin!" + dataFile
    return jsonify({'resultado': { \
    'resulta': resultado \
    }}), 200
    #return jsonify(resultado)

if __name__ == "__main__":
    app.run()
