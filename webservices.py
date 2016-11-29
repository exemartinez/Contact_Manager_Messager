from flask import Flask, render_template, jsonify
from system import Importer

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
@app.route('/api/v1.0/contactos/all', methods=['GET'])
def get_all_contacts():
    '''Returns all the database contacts.'''
    #TODO: Have to TEST this method ASAP.
    contactosctrl = ContactosController()
    
    resultado = contactosctrl.getContactosAll()
    
    return jsonify({'resultado': resultado}}), 200

@app.route('/api/v1.0/contactos/load/linkedin/<string:dataFile>', methods=['GET'])
def post_load_linkedin_contacts(dataFile):
    #TODO: Has to wrte the tests.
    '''Loads a all the database contacts.'''
    imp = ImportController()

    res = imp.import_Linkedin_Csv_Contacts(str(dataFile))

    if (res):
        return jsonify({'resultado': res}), 200

    else:
        return jsonify({'resultado': res}), 501

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()
