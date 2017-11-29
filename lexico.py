import os
import sys


class LexAnalizer(object):
    # TODO: gestionar casos de error, pueden faltar algunos

    def __init__(self, fileName):
        self.filePointer = open(fileName)
        self.char = ""
        self.fileName = ""
        self.tablaSimbolos = tabla_simbolos()
        self.file_error = open("errorLexico.txt", "w")

    def pedirToken(self):
        if self.char == "":
            self.char = self.filePointer.read(1)

        while self.char == ' ':  # Compruebo si se leen espacios en blanco
            self.char = self.filePointer.read(1)
            return "blanco",

        if self.char.isalpha():  # Estado: comprueba identificadores y palabras clave
            token = self.char

            while True:
                self.char = self.filePointer.read(1)

                if self.char.isalnum() or self.char == "_":
                    token += self.char

                else:
                    if token in self.tablaSimbolos:
                        index = self.tablaSimbolos.index(token)
                        if index < 55:
                            return "palabra reservada", index
                        else:
                            return "id", index

                    else:
                        self.tablaSimbolos.append(token)
                        return "id", self.tablaSimbolos.index(token)

        if self.char.isdigit():  # Estado: comprueba constantes enteras
            num = 0
            while self.char.isdigit():
                if num is 0:
                    num = self.char
                else:
                    num = num + self.char
                self.char = self.filePointer.read(1)
            else:
                return "cte-ent", num

        if self.char == '"':  # Estado: comprueba strings
            string = self.char
            aux = True

            while aux:
                self.char = self.filePointer.read(1)

                if (self.char != '\n' and self.char != '"') or self.char == '':
                    # DONE: Comprobar si puntero esta al final del fichero
                    string += str(self.char)

                else:
                    if self.char == '"':
                        self.char = self.filePointer.read(1)
                        return "string", string + "\""

                    else:
                        aux = False
                        self.file_error.write("ERROR: String mal definido \n")

        if self.char == '-':  # Estado: comprueba post-decremento -> --
            self.char = self.filePointer.read(1)

            if self.char == '-':
                self.char = self.filePointer.read(1)
                return "post-dec",
            else:
                self.char = self.filePointer.read(1)
                return "op-arit", 2

        if self.char == '|':  # Estado: comprueba asignacion con o logico -> --
            self.char = self.filePointer.read(1)

            if self.char == '=':
                return "or-logic",
            else:
                self.file_error.write("ERROR: Asignacion OR logico mal formada \n")

        if self.char == '/':  # Estado: compruebo comentarios //...
            self.char = self.filePointer.read(1)

            if self.char == '/':
                while self.char != '\n':
                    self.char = self.filePointer.read(1)
                else:
                    return "coment//",
            elif self.char == '*':  # Estado: compruebo comentarios /*...*/
                self.char = self.filePointer.read(1)
                while self.char != '*':
                    self.char = self.filePointer.read(1)
                self.char = self.filePointer.read(1)
                if self.char != '/':
                    self.file_error.write("ERROR: Comentario /* mal formado \n")
                else:
                    self.char = self.filePointer.read(1)
                    return "coment/*",
            elif self.char != ' ':
                return "op-arit", 4

        if self.char == '=':  # Estado: compruebo si se trata de asignacion o de comparacion
            self.char = self.filePointer.read(1)

            if self.char == '=':
                self.char = self.filePointer.read(1)
                return "op-rel",
            else:
                self.char = self.filePointer.read(1)
                return "op-asign",

        if self.char == '&':  # Estado: compruebo si se trata del operador logico &&
            self.char = self.filePointer.read(1)

            if self.char == '&':
                return "op-log",
            else:
                self.file_error.write("ERROR: AND logico mal formado")

        if self.char == '+':  # Estado: compruebo si se trata de un operador de suma
            self.char = self.filePointer.read(1)
            return "op-arit", 1

        if self.char == '*':  # Estado: compruebo si se trata de un operador de suma
            self.char = self.filePointer.read(1)
            return "op-arit", 3

        if self.char == '!':  # Estado: compruebo si se trata de un operador de esclamacion
            self.char = self.filePointer.read(1)
            return "op-arit", 5

        if self.char == '(':  # Estado: compruebo si se trata de un abre-parentesis
            self.char = self.filePointer.read(1)
            return "abre-par",

        if self.char == ')':  # Estado: compruebo si se trata de un cierra-parentesis
            self.char = self.filePointer.read(1)
            return "cierr-par",

        if self.char == '{':  # Estado: compruebo si se trata de un abre-llaves
            self.char = self.filePointer.read(1)
            return "abre-llave",

        if self.char == '}':  # Estado: compruebo si se trata de un cierra-llaves
            self.char = self.filePointer.read(1)
            return "cierr-llave",

        if self.char == ';':  # Estado: compruebo si se trata de un punto y coma
            self.char = self.filePointer.read(1)
            return "puntoComa",

        if self.char == ',':  # Estado: compruebo si se trata de una coma
            self.char = self.filePointer.read(1)
            return "coma",

        if self.char == '\n':  # Estado: compruebo si se trata de un salto de linea
            self.char = self.filePointer.read(1)
            return "salto linea",

        if self.char == '\t':  # Estado: compruebo si se trata de una tabulacion
            self.char = self.filePointer.read(1)
            return "tab",

        if self.char == '.':  # Estado: compruebo si se trata de una llamada a funcion
            self.char = self.filePointer.read(1)
            return "punto",

        return "eof",


def escribir_token_en_fichero(token):
    file = open("token.txt", "a")
    if token[0] == "coment//" or token[0] == "blanco" or token[0] == "tab":
        pass
    elif len(token) == 1:
        file.write("<" + str(token[0]) + ">\n")
    else:
        file.write("<" + str(token[0]) + "," + str(token[1]) + ">\n")


def tokens_list(file_name):
    analyzer = LexAnalizer(file_name)
    token = analyzer.pedirToken()
    tokens = list()

    while token[0] is not "eof":
        if token[0] != 'coment//' and token[0] != 'blanco' and token[0] != 'tab':
            tokens.append(token)
        token = analyzer.pedirToken()
    tokens.append(token)
    return tokens


def tabla_simbolos():
    tabla = list()
    tabla.append("abstract")
    tabla.append("boolean")
    tabla.append("break")
    tabla.append("byte")
    tabla.append("case")
    tabla.append("catch")
    tabla.append("chars")
    tabla.append("class")
    tabla.append("const")
    tabla.append("continue")
    tabla.append("default")
    tabla.append("do")
    tabla.append("double")
    tabla.append("else")
    tabla.append("extends")
    tabla.append("false")
    tabla.append("final")
    tabla.append("finally")
    tabla.append("float")
    tabla.append("for")
    tabla.append("function")
    tabla.append("goto")
    tabla.append("if")
    tabla.append("implements")
    tabla.append("import")
    tabla.append("in")
    tabla.append("instanceof")
    tabla.append("int")
    tabla.append("interface")
    tabla.append("long")
    tabla.append("native")
    tabla.append("new")
    tabla.append("null")
    tabla.append("package")
    tabla.append("private")
    tabla.append("prompt")
    tabla.append("protected")
    tabla.append("public")
    tabla.append("return")
    tabla.append("short")
    tabla.append("static")
    tabla.append("super")
    tabla.append("switch")
    tabla.append("synchronized")
    tabla.append("this")
    tabla.append("throw")
    tabla.append("throws")
    tabla.append("transient")
    tabla.append("true")
    tabla.append("try")
    tabla.append("var")
    tabla.append("void")
    tabla.append("while")
    tabla.append("whith")
    tabla.append("write")
    return tabla


def lexico(file_name):
    analyzer = LexAnalizer(file_name)
    os.remove(os.path.dirname(os.path.realpath(__file__)) + os.sep + "token.txt")
    token = analyzer.pedirToken()

    while token[0] is not "eof":
        escribir_token_en_fichero(token)
        token = analyzer.pedirToken()

    print "Fichero generado: token.txt"
    return analyzer.tablaSimbolos


def main():
    analyzer = LexAnalizer(sys.argv[1])
    os.remove(os.path.dirname(os.path.realpath(__file__)) + os.sep + "token.txt")
    token = analyzer.pedirToken()

    while token[0] is not "eof":
        escribir_token_en_fichero(token)
        token = analyzer.pedirToken()

    print "Fichero generado: token.txt"


if __name__ == '__main__':
    main()
