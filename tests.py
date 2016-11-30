import sys
import unittest
import csv
import chardet
from backend import StringCoder, ImportController, LogMngr, Contacto, DAO, CSVManager, ContactosController


class importTest(unittest.TestCase):

    log = LogMngr("Testing")

    dao = None
    csvMng = None

    #The filename to be tested - usually a linkedin contacts export cvs file.
    filename = "./linkedin_connections_export_microsoft_outlook_dummy.csv"

    '''
    Test if inserting in the database of a new contact works ok.
    '''
    def test_database_contacto_insert(self):

        self.dao = DAO()
        self.csvMng = CSVManager()

        #iterates over the list of contacts and introduces it into the database.
        self.dao.open_connection()

        conta = Contacto()

        #dummy data for testing purposes
        conta.setNombre("John")
        conta.setApellido("Doe")
        conta.setCompania("ACME")
        conta.setPosicion("CEO")
        conta.setEmail("johndoe@gmail.com")
        conta.setTipo("dummy_erase_this_now")

        result = self.dao.exec_new_single_contacto(conta)

        self.assertEqual(result, 0)

        #deletes the inserted data.
        if (not self.dao.exec_delete_tipo_contacto(conta.getTipo())):
            print("Database remains corrupted - erase records with tipo=" +conta.setTipo())

        self.dao.close_connection()


    def test_import_linkedin_file_representation(self):
        '''
        It tests if the file string encoding is appropriate to be imported into the database.
        '''

        scoder = StringCoder()
        x = 0
        with open(self.filename, 'rb') as f: #watch it: this file HAS to be a CSV file...
            reader = csv.reader(f)
            try:
                for row in reader:
                    x+=1
                    assert type(row[1]) is str
                    self.log.info("String representation: " + \
                        str(chardet.detect(row[1])["encoding"]))

                    self.log.info("Values: Nombre -  " + scoder.encode(row[1]) + \
                        " Apellido: " + scoder.encode(row[3]) + " e-mail: " + scoder.encode(row[5]) + \
                        " compania: " + scoder.encode(row[29]) + " posicion (job title): " + scoder.encode(row[31]))
            except:
                self.log.info("Error: The configured csv file is in a type of string encoding that cannot be decoded.")


            self.assertEqual(x > 0, True)

    def test_REST_linkedin_datafile(self):
        ''' Test the REST WS for data import. '''

        scoder = StringCoder()
        imp = ImportController()
        result = imp.import_Linkedin_Csv_Contacts(self.filename)

        self.assertEqual(result, True)
        
    def test_get_all_contactos_REST(self):
        ''' Test the REST WS for all the contacts retrieval to the frontend. '''
        contactos = ContactosController()
        result = contactos.getContactosAll()
        
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
