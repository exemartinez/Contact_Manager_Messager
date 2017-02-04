from flask import Flask, render_template, jsonify, request, json, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from backend import ImportController, ContactosController, MessagingController, LogMngr, MailingManager

#Constants
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','csv','docx'])

#Flask Settings
app = Flask(__name__)
app.secret_key = '003-Gr4c10s0+50s$Gar0f4!' #special key for coding the session variables.
log = LogMngr("web services frontend")
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #it allows to upload a file of up to 64mb.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def index():
    '''Establishes the app entry point.'''

    return render_template("home.html")

@app.route('/logoff')
def clearsession():
    """Logs off the user from the app."""
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect('/home')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    '''Returns the uploaded file name'''
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
def allowed_file(filename):
    '''Defines which sort of files are allowed to be sent to the server'''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

@app.route('/api/v1.0/mailing/login_try', methods=['POST'])
def login_mail():
    '''This logs into the mailing server and takes the credentials for further usage.'''
    log.info("Login into the mail service...")

    post = request.get_json()

    user = post.get('user')
    password = post.get('pass')
    server = post.get('server')

    result = False

    try:

        log.info("User to login: " + user)
        mail = MailingManager()
        mail.setServer(server)

        result = mail.login(user, password)

        if(result):

            session['user']=user
            session['password']=password
            session['server']=server

            return jsonify({'resultado': 'User logged in!.'}), 200

        else:

            session.clear()
            return jsonify({'resultado': 'Bad user name or password.'}), 400

    except Exception as e:

        log.error("ERROR: " + str(e))
        session.clear()
        return jsonify({'resultado': 'Can\'t log in.'}), 500

    return jsonify({'resultado': 'User logged in!.'}), 200

@app.route('/api/v1.0/upload_controller', methods=['GET', 'POST'])
def upload_file():
    '''Manages the file after it is sent by a HTML input for uploading.'''
    log.info("Uploading the posted file...")

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            log.error("No file part")
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            log.error("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            log.info("Saving file to disk...")
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #TODO: Have to change the filename for unique name, so different users can upload files.
            except Exception as e:
                log.error("Internal Error:" + str(e))
                return jsonify({'resultado': 'Error trying to upload the file to the server.','code':500}), 500

            log.info("File uploaded successfully!")

            return jsonify({'resultado': str(url_for('uploaded_file', filename=filename)),'code':200}), 200
            #return redirect(url_for('uploaded_file',filename=filename)) #use this in case you want to show the file.

    return jsonify({'resultado': 'Wrong form method or signature.','code':500}), 500

@app.route('/api/v1.0/mailing/send', methods=['POST'])
def send_mail_to_contacts():
    '''Returns all the database contacts.'''

    #TODO: Have to TEST this method ASAP.
    mailctrl = MessagingController()
    log.info("Params: " + str(request.json))

    #TODO: This has to be reennacted as soon as I implement login for the mailing service.
    """
    if not request.json or not 'username' in request.json:
        return jsonify({'resultado': 'Bad parameters or JSON structure'}), 400
    """

    #parsing post parameters

    username=session['user']
    passw=session['password']
    mensaje = request.json['message']
    remitente=session['user']
    destinatarios = request.json['selectedItems'] #it comes as a list and is inmediatly transformed: access it by "destinatarios[x]"
    asunto = request.json['subject']
    attachment = request.json['fileName']

    log.info("The subject received was:" + request.json['subject'])

    resultado = mailctrl.send_Massive_Mails_to_Contacts(username, passw, mensaje,remitente, destinatarios, asunto, session['server'], attachment)

    if(resultado==0):
        return jsonify({'resultado': resultado}), 200
    else:
        return jsonify({'resultado': 'Error trying to send the mails to the given contacts'}), 501

@app.route('/api/v1.0/contactos/all', methods=['GET'])
def get_all_contacts():
    '''Returns all the database contacts.'''
    #TODO: Have to TEST this method ASAP.
    contactosctrl = ContactosController()

    contactosctrl.getContactosAll()
    resultado = contactosctrl.getJSONContactosSet()

    log.info(resultado);

    return resultado, 200


@app.route('/api/v1.0/contactos/load/linkedin', methods=['GET', 'POST'])
def post_load_linkedin_contacts():
    #TODO: Has to wrte the tests.
    '''Loads a all the database contacts.'''
    imp = ImportController()

    log.info("Importing file " + request.json['fileName'] + " into the database.");
    res = imp.import_Linkedin_Csv_Contacts(str("." + request.json['fileName']))

    if (res):
        return jsonify({'resultado': res}), 200
    else:
        return jsonify({'resultado': res}), 501

    return jsonify(resultado)

if __name__ == "__main__":
    app.run()
