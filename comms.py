import smtplib
from system import LogMngr

class MailingManager:

    server = smtplib.SMTP('smtp.gmail.com:587') #TODO Replace this for a parameter extracted from a configuration file or some other thing.

    #System controllers: logs and others
    log = LogMngr("mailing_manager")

    def login(self, username, password):
        '''This allows the entire app to login'''
        try:
            #This is an example of Google Mail:
            self.server.ehlo()
            self.server.starttls()
            self.server.login(username,password)

            self.log.info( "Usuario " + username + " conectado.")

        except:
            self.log.error("""Error: el usuario, password o servidor son erroneos.""")

    def sendMail(self, mensaje, remitente, destinatario, asunto):
        '''Sends a mail to a given account.'''
        #Message basic and standard template.
        msg = "\r\n".join([
          "From: " + remitente,
          "To: " + destinatario,
          "Subject: " + asunto,
          "",
          mensaje
          ])

        try:

            self.server.sendmail(remitente, destinatario, msg)

            log.info( "Correo enviado a " + destinatario + ".")

        except:
            log.error("""Error: el mensaje no pudo enviarse.
            Compruebe que sendmail se encuentra instalado en su sistema""")

    def logOout(self):
        '''Logs out from the user mail account'''
        self.server.quit()
