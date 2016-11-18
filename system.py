from dao import DAO
from csv_reader import CSVManager
from entities import Contacto

import sys
import logging
import locale
import chardet

'''
The encoding class definition
'''
class StringCoder():

    '''
    Decodes the data that comes from the CSV file and transforms it to UNICODE
    '''
    def encode(self, stringValue):
        #TODO: We need a better way to transform the data to unicode. Currently it just replaces the conflicting chars or leaves it as it is.
        coding = str(chardet.detect(stringValue)["encoding"])
        try:
            valor = unicode(stringValue, coding)
        except:
            valor = stringValue

        return valor

'''
The system management classes goes here.
'''
class LogMngr():

    logger = None

    '''
    Constructor initializes the base logging configuration.
    '''
    def __init__(self, logger_name):

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        #fh = logging.StreamHandler() #this is to print it in the common console.
        fh = logging.FileHandler('importing_database_data.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    '''
    Prints INFO kind of data.
    '''
    def info(self, valor):
        self.logger.info(valor)

    '''
    Prints ERRORS kind of data.
    '''
    def error(self, valor):
        self.logger.info(valor)

    '''
    Prints DEBUG kind of data.
    '''
    def debug(self, valor):
        self.logger.debug(valor)

class Importer():
'''
This class imports contacts into the SQLite database; it manages different data structures.
'''
    def import_Linkedin_Csv_Contacts(dataFile):
        '''Just loads the database with the CSV data obtained from linkedin. It serves their data structure.'''

        log = LogMngr("Importer.import_linkedin_csv_contacts")

        if (dataFile!=None):
            log.info("Processing the CSV file exported from LinkedIn (c) 2016 -> " + str(dataFile))

            dao = DAO()
            csvMng = CSVManager()

            #iterates over the list of contacts and instroduces it into the database.
            dao.open_connection()

            log.info("Database connection online.")
            contactos = csvMng.getContactos(str(dataFile))

            #TODO: Classify the contact; analize its data and tag it or typify it.
            for conta in contactos:
                #TODO: perform updates, when the record already exists.
                result = dao.exec_new_single_contacto(conta) #inserts new data.

                if (result == dao.SQLITE_CONSTRAINT_UNIQUE):
                    result = dao.exec_upd_single_contacto(conta) #updates the same record with new data.

            dao.close_connection()
            log.info("Database connection closed.")

            log = None

            return True

        else:
            log.error("Datafile name to import laking.")
            log = None

            return False
