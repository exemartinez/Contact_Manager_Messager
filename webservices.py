from flask import Flask, render_template, jsonify, request
from backend import ImportController, ContactosController, MessagingController, LogMngr

app = Flask(__name__)
log = LogMngr("web services frontend")

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

@app.route('/api/v1.0/mailing/send', methods=['POST'])
def send_mail_to_contacts():
    '''Returns all the database contacts.'''
    #below, curl for testing...(it didn't work yet; gives away a bad request error)
    #curl -i -H "Content-Type: application/json" -X POST -d '{"username":"yz","passw":"xyz","mensaje":"Buen test!","remitente":"Un remitente","destinatarios":"set de destinatarios","asunto":"mail de pruebas"}' http://127.0.0.1:5000/api/v1.0/mailing/send
    #TODO: Have to TEST this method ASAP.
    mailctrl = MessagingController()

    #TODO has to add the unjsonify of the destinatarios parameter.

    if not request.json or not 'username' in request.json:
        return jsonify({'resultado': 'Bad parameters or JSON structure'}), 400

    #parsing post parameters
    username = request.json['username']
    passw = request.json['passw']
    mensaje = request.json['mensaje']
    remitente = request.json['remitente']
    destinatarios = request.json['destinatarios']
    asunto = request.json['asunto']

    log.info("The values received were:" + request.json['username'])

    resultado = mailctrl.send_Massive_Mails_to_Contacts(username, passw, mensaje,remitente, unjsonify(destinatarios), asunto)

    if(resultado==0):
        return jsonify({'resultado': resultado}), 200
    else:
        return jsonify({'resultado': 'Error trying to send the mails to the given contacts'}), 501

@app.route('/api/v1.0/contactos/all', methods=['GET'])
def get_all_contacts():
    '''Returns all the database contacts.'''
    #TODO: Have to TEST this method ASAP.
    contactosctrl = ContactosController()

    resultado = contactosctrl.getContactosAll()

    return jsonify({'resultado': resultado}), 200

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
