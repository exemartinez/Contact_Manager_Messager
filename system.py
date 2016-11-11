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
