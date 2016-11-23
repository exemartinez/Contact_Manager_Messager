from entities import Contacto
from system import LogMngr

import logging
#import unicodecsv as csv
import csv

class CSVManager():



    logger = logging.getLogger()

    '''
    Just reads the passed as parameter filename and prints its contents out of the box. - This is just for checking the file structure and show it to the user, purposes.
    '''
    def read_csv_print(self, file_name):
        with open(file_name, 'rb') as f: #watch it: this file HAS to be a CSV file...
            reader = csv.reader(f)
            try:
                for row in reader:
                    print row[1] + " " + row[3] + " e-mail: " + row[5] + " compania: " + row[29] + " posicion (job title): " + row[31]
            except (IndexError):
                print "Minor Error: Index out of bounds (end of file unexpectedly reached)."

    '''
    returns a set with all the data extracted from the CSV; this set is an object suitable for the database.
    '''
    def getContactos(self, file_name):

        contactos = set()

        with open(file_name , 'rb') as f:
            reader = csv.reader(f)
            try:
                for row in reader:

                    if (row[1] == "First Name"):
                        continue

                    conta = Contacto()

                    conta.setNombre(row[1])
                    conta.setApellido(row[3])
                    conta.setEmail(row[5])
                    conta.setCompania(row[29])
                    conta.setPosicion(row[31])

                    contactos.add(conta)

            except (IndexError):
                self.logger.error("Minor Error: Index out of bounds (end of file unexpectedly reached).")

        return contactos
