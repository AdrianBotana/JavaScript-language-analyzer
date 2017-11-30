class ContenidoTabla(object):
    # Los objetos de esta clase seran los que se inserten en la tabla de simbolos
    # Cada atributo representa las columnas de la tabla de simbolos

    def __init__(self, argum, lexema="", tipo="", despl=-1):
        self.lexema = lexema
        self.tipo = tipo
        self.despl = despl
        self.argum = argum


class TablaSimbolos(object):
    # La tabla de simbolos es un array de objetos, cada objeto representa las columnas mientras que los indices
    # del array se corresponden a los indices de las filas de la tabla de simbolos

    tabla = list()
    prueba = ContenidoTabla(lexema="hola", tipo="", argum=[])

    # DONE: Introducir palabras clave por defecto en la tabla mediante tabla.append()

    tabla.append(ContenidoTabla(lexema="abstract", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="boolean", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="break", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="byte", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="case", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="catch", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="char", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="class", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="const", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="continue", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="default", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="do", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="double", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="else", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="extends", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="false", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="final", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="finally", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="float", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="for", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="function", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="goto", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="if", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="implements", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="import", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="in", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="instanceof", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="int", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="interface", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="long", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="native", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="new", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="null", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="package", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="private", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="prompt", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="protected", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="public", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="return", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="short", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="static", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="super", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="switch", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="synchronized", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="this", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="throw", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="throws", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="transient", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="true", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="try", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="var", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="void", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="while", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="whith", tipo="palabra reservada", argum=[]))
    tabla.append(ContenidoTabla(lexema="write", tipo="palabra reservada", argum=[]))

    def __getitem__(self, item):
        return self.tabla.__getitem__(item)

    def insertarTS(self, content):
        self.tabla.append(content)

    def buscarTS(self, content):
        aux = [element for element in self.tabla if element.lexema == content.lexema]

        if not aux:
            return -1
        else:
            return self.tabla.index(aux[0])

    def borrarTS(self, content):
        self.tabla.pop(self.tabla.index(content))