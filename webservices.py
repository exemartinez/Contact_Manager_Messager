from flask import Flask, render_template, jsonify, request, json, redirect, url_for
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename
from backend import ImportController, ContactosController, MessagingController, LogMngr

#Constants
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','csv','docx'])

#Flask Settings
app = Flask(__name__)
log = LogMngr("web services frontend")
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #it allows to upload a file of up to 64mb.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def index():
    '''Establishes the app entry point.'''
    return render_template("home.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    '''Returns the uploaded file name'''
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
def allowed_file(filename):
    '''Defines which sort of files are allowed to be sent to the server'''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload_controller', methods=['GET', 'POST'])
def upload_file():
    '''Manages the file after it is sent by a HTML input for uploading.'''
    log.info("Uploading the posted file...")

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            log.error("No file part")
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            log.error("No selected file")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            log.info("Saving file to disk...")
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except Exception as e:
                log.error("Internal Error:" + str(e))
                return jsonify({'resultado': 'Error trying to upload the file to the server.'}), 500

            log.info("File uploaded successfully!")

            return jsonify({'resultado': str(url_for('uploaded_file', filename=filename))}), 200
            #return redirect(url_for('uploaded_file',filename=filename)) #use this in case you want to show the file.

    return jsonify({'resultado': 'Wrong form method or signature.'}), 500

@app.route('/upload')
def upload():
    '''renders a file uploader page.'''
    return render_template("uploads.html")

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
    #TODO: Have to TEST this method ASAP.
    mailctrl = MessagingController()

    if not request.json or not 'username' in request.json:
        return jsonify({'resultado': 'Bad parameters or JSON structure'}), 400

    #parsing post parameters
    username = request.json['username']
    passw = request.json['passw']
    mensaje = request.json['mensaje']
    remitente = request.json['remitente']
    destinatarios = request.json['destinatarios'] #it comes as a list and is inmediatly transformed: access it by "destinatarios[x]"
    asunto = request.json['asunto']

    log.info("The subject received was:" + request.json['asunto'])

    resultado = mailctrl.send_Massive_Mails_to_Contacts(username, passw, mensaje,remitente, destinatarios, asunto)

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
