from dao import DAO
from csv_reader import CSVManager
from entities import Contacto
from system import LogMngr

import sys

'''
This imports the CSV into the SQLite database.
'''
if __name__ == "__main__":

    log = LogMngr("import_database")

    if (len(sys.argv) > 1):
        log.info("Processing the CSV file exported from LinkedIn (c) 2016 -> " + str(sys.argv[1]))

        dao = DAO()
        csvMng = CSVManager()

        #iterates over the list of contacts and instroduces it into the database.
        dao.open_connection()

        log.info("Database connection online.")
        contactos = csvMng.getContactos(str(sys.argv[1]))

        #TODO: Classify the contact; analize its data and tag it or typify it.
        for conta in contactos:
            #TODO: perform updates, when the record already exists.
            result = dao.exec_new_single_contacto(conta) #inserts new data.

            if (result == dao.SQLITE_CONSTRAINT_UNIQUE):
                result = dao.exec_upd_single_contacto(conta) #updates the same record with new data.

        dao.close_connection()
        log.info("Database connection closed.")
