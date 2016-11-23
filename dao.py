from system_messenger import LogMngr

import logging
import locale
import sqlite3 as sqlite
#from pysqlite2 import dbapi2 as sqlite

class DAO (object):

    SQLITE_CONSTRAINT_UNIQUE = 2067
    SQLITE_CONSTRAINT = 19
    SQLITE_ERROR = 1
    SQLITE_OK = 0

    log = LogMngr("database_transactions")

    '''
    Updates a contact with new data into the database
    '''
    def exec_upd_single_contacto(self, contacto):

        try:

            result = self.cursor.execute("update contactos set nombre = ?, apellido = ?, email = ?, compania = ?, posicion = ?, tipo = ? where email = ?", (contacto.getNombre(), contacto.getApellido(), contacto.getEmail(), contacto.getCompania(), contacto.getPosicion(), contacto.getTipo(), contacto.getEmail()))
            self.connection.commit()

        except sqlite.IntegrityError as er:
            self.log.error("Database Error: " + str(er.args))
            if (str(er.message)[:6]=="UNIQUE"):
                return self.SQLITE_CONSTRAINT_UNIQUE #Unique constraint failed.
            else:
                return self.SQLITE_CONSTRAINT

        except sqlite.Error as er:
            self.log.error("Database Error: " + er.message)
            self.log.error("The database insert failed with contacto: " + contacto.getNombre() + " " + contacto.getApellido())
            self.connection.rollback()
            return self.SQLITE_ERROR #SQLite error or missing database

        return self.SQLITE_OK #sqlite OK! yey!

    '''
    Inserts a new contact into the database
    '''
    def exec_new_single_contacto(self, contacto):

        try:

            result = self.cursor.execute("insert into contactos (nombre, apellido, email, compania, posicion, tipo) values (?, ?, ?, ?, ?, ?)", (contacto.getNombre(), contacto.getApellido(), contacto.getEmail(), contacto.getCompania(), contacto.getPosicion(), contacto.getTipo(),))
            self.connection.commit()

        except sqlite.IntegrityError as er:
            self.log.error("Database Error: " + str(er.args))
            if (str(er.message)[:6]=="UNIQUE"):
                return self.SQLITE_CONSTRAINT_UNIQUE #Unique constraint failed.
            else:
                return self.SQLITE_CONSTRAINT

        except sqlite.Error as er:
            self.log.error("Database Error: " + er.message)
            self.log.error("The database insert failed with contacto: " + contacto.getNombre() + " " + contacto.getApellido())
            self.connection.rollback()
            return 1 #SQLite error or missing database

        return 0 #sqlite OK! yey!

    def exec_delete_tipo_contacto(self, tipo):
        '''
        Deletes all the contacto's records with the given tipo.
        '''
        try:

            self.cursor.execute("delete from contactos where tipo=?", (str(tipo),))
            self.connection.commit()

        except:
            self.log.error("The database deletion by TIPO failed with TIPO: " + str(tipo))
            self.connection.rollback()
            return False

        return True

    def exec_get_contacto_exists_byCompania(self, compania):
        '''
        Returns one, single sub categoria by its URL
        '''
        self.cursor.execute("select * from contactos where compania=?", (compania,))
        return self.cursor.fetchone()

    def exec_get_contactos_exists_byEmail(self, email):
        '''
        Returns one, single contacto by its URL
        '''
        self.cursor.execute("select * from contactos where email=?", (email,))
        result = self.cursor.fetchone()

        self.log.debug("search ---- " + str(result))
        return result

    def exec_get_all_contactos(self):
        '''
        Returns every categoria that is in place (full scan)
        '''
        self.log.debug("Fetching...")
        self.cursor.execute("select id, nombre, apellido, email, compania, posicion, tipo from contactos")

        return self.cursor.fetchall()

    def open_connection(self):
        '''
        Sets the due connections to the data stores.
        '''

        self.log.debug("Initiating database")
        # Initializes the connection to SQLite (and creates the due tables)
        self.connection = sqlite.connect('./contactos.db')
        self.connection.text_factory = str

        self.cursor = self.connection.cursor()

        #Creates the database TABLES, if there is NONE
        self.cursor.execute('CREATE TABLE IF NOT EXISTS contactos ' \
                    '(id INTEGER PRIMARY KEY, nombre varchar(40), apellido varchar(40), email varchar(140) UNIQUE, compania varchar(140), posicion varchar(140), tipo varchar(40))')

        self.log.debug("Database, READY to throw operations at her.")

    def close_connection(self):
        '''
        Closes the database connection to avoid issues related to the connectivity.
        '''
        self.log.debug("Database offline.")
        self.cursor.close()
