from system import StringCoder


class Contacto():
    '''
    The entity of "Contactos" in the database; one instance = one row.
    '''

    nombre = ""
    apellido = ""
    email = ""
    compania = ""
    posicion = ""
    tipo = ""

    scoder = StringCoder()

    #setters y getters.
    def getNombre(self):
        return self.nombre
    def setNombre(self, valor):
        self.nombre = self.scoder.encode(str(valor))

    def getApellido(self):
        return self.apellido
    def setApellido(self, valor):
        self.apellido = self.scoder.encode(str(valor))

    def getEmail(self):
        return self.email
    def setEmail(self, valor):
        self.email = self.scoder.encode(str(valor))

    def getCompania(self):
        return self.compania
    def setCompania(self, valor):
        self.compania = self.scoder.encode(str(valor))

    def getPosicion(self):
        return self.posicion
    def setPosicion(self, valor):
        self.posicion = self.scoder.encode(str(valor))

    def getTipo(self):
        return self.tipo
    def setTipo(self, valor):
        self.tipo = self.scoder.encode(str(valor))
