import sys

import lexico


class Syntactic(object):
    def __init__(self, file_name):
        self.tokens = lexico.tokens_list(file_name)
        self.tablaSimbolos = lexico.lexico(file_name)
        self.file_error = open("errorSintactico.txt", "w")
        self.token = self.tokens.pop(0)

    def show_tokens(self):
        while self.tokens.__len__() > 0:
            print self.tokens.pop(0)
    #TODO: Casos de errores de la mayoria de los no terminales

    def P(self):
        print self.token[0] + "P"
        if self.token[0] == 'palabra reservada':
            aux = self.comprobar_tabla(self.token[1])
            if aux == 'function':  #Estado 1
                self.F()
                self.Z()
                self.P()
            elif aux == 'var' or aux == 'if' or aux == 'write' or aux == 'do' or aux == 'prompt' or aux == 'id' or aux == 'return':  # Estado 2
                self.B()
                self.Z()
                self.P()
            else:
                self.file_error.write("ERROR: en P en palabra reservada\n")
        if self.token[0] == 'coment/*':  # Estado 3
            self.Z()
            self.P()
        elif self.token[0] == 'salto linea':  # Estado 76
            self.token = self.tokens.pop(0)
            self.P()
        elif self.token[0] == 'eof':
            print "El programa ha terminado"  # Estado 4
        elif self.token[0] =='id':
            self.file_error.write("ERROR: en P id mal declarado\n")
        else:
            self.file_error.write("ERROR: en P")

    def Z(self):
        print self.token[0] +"Z"
        if self.token[0] == 'coment/*':  # Estado 5
            self.C1()
            if self.token[0] == 'salto linea':
                self.token = self.tokens.pop(0)
                if self.token[0] == 'coment/*':  # Estado 6
                    self.Z()
            else:
                self.file_error.write("ERROR: en Z no salto linea tras comentario \n")
        else:
            self.file_error.write("ERROR: en Z no coment/* \n")

    def Z1(self):
        if self.token[0] == 'coment/*':
            self.Z()

    def C1(self):
        print self.token[0] + "C1"
        if self.token[0] == 'coment/*':  # Estado 7, 8
            self.token = self.tokens.pop(0)

    def F(self):  # Estado 9
        print self.token[0] + "F"
        if self.comprobar_tabla(self.token[1]) is not 'function':
            self.file_error.write("ERROR: en F no function \n")
        self.token = self.tokens.pop(0)
        if self.token[0] is 'palabra reservada':
            self.T1()
            if self.comprobar_tabla(self.token[1]) is not None:
                self.token = self.tokens.pop(0)
                if self.token[0] == 'abre-par':
                    self.token = self.tokens.pop(0)
                    self.A()
                    if self.token[0] == 'cierr-par':
                        self.token = self.tokens.pop(0)
                        self.Z1()
                        if self.token[0] == 'abre-llave':
                            self.token = self.tokens.pop(0)
                            self.Z()
                            self.S1()
                            if self.token[0] == 'cierr-llave':
                                self.token = self.tokens.pop(0)

    def T1(self):  # Estado 10,11
        print self.token[0] + "T1"
        aux = self.comprobar_tabla(self.token[1])
        if aux is 'int' or aux is 'chars' or aux is 'bool':
            self.T()

    def T(self):  # Estado 12, 13, 14
        print self.token[0] + "T"
        aux = self.comprobar_tabla(self.token[1])
        if aux is 'int' or aux is 'chars' or aux is 'bool':
            self.token = self.tokens.pop(0)
        else:
            self.file_error.write("ERROR: en T no tipo \n")

    def A(self):  # Estado 15, 16
        print self.token[0] + "A"
        self.T()
        if self.comprobar_tabla(self.token[1]) is not None:
            self.token = self.tokens.pop(0)
            if self.token[0] is not 'cierr-par':
                self.A1()

    def A1(self):  # Estado 17, 18
        print self.token[0] + "A1"
        if self.token[0] is 'coma':
            self.token = self.tokens.pop(0)
            self.T()
            if self.comprobar_tabla(self.token[1]) is not None:
                self.token = self.tokens.pop(0)
                if self.token[0] is not 'cierr-par':
                    self.A1()

    def S1(self):  # Estado 19, 20
        print self.token[0] + "S1"
        aux = self.comprobar_tabla(self.token[1])
        if aux == 'var' or aux == 'if' or aux == 'write' or aux == 'prompt' or aux == 'id' or aux == 'return':
            self.B()
            self.Z()
            self.S1()

    def M(self):  # Estado 21, 22
        print self.token[0]
        if self.token[0] is 'puntoComa':
            self.token = self.tokens.pop(0)
            self.S()
            self.M()

    def B(self):  # Estado 23, 24, 25, 26
        print self.token[0] + "B"
        aux = self.comprobar_tabla(self.token[1])
        print aux
        if aux is 'var':
            self.token = self.tokens.pop(0)
            self.T()
            if self.comprobar_tabla(self.token[1]) is not None:
                self.token = self.tokens.pop(0)
                self.V()
                self.V1()
        elif aux is 'if':
            self.token = self.tokens.pop(0)
            if self.comprobar_tabla(self.token[1]) is 'abre-par':
                self.token = self.tokens.pop(0)
                self.Q()
                if self.comprobar_tabla(self.token[1]) is 'cierr-par':
                    self.token = self.tokens.pop(0)
                    self.S()
        elif aux is 'do':
            self.token = self.tokens.pop(0)
            self.Z1()
            if self.token[0] is 'abre-llave':
                self.token = self.tokens.pop(0)
                self.Z()
                self.S1()
                if self.token[0] is 'cierr-llave':
                    self.token = self.tokens.pop(0)
                    if self.token[0] is 'palabra reservada':
                        if self.comprobar_tabla(self.token[1]) is 'while':
                            self.token = self.tokens.pop(0)
                            if self.token[0] is 'abre-par':
                                self.token = self.tokens.pop(0)
                                self.Q()
                                if self.token[0] is 'cierr-par':
                                    self.token = self.tokens.pop(0)
        else:
            self.token = self.tokens.pop(0)
            self.S()
            self.M()

    def S(self):  # Estado 27,28,29,30,31,32
        if self.token[0] is 'palabra reservada':
            if self.comprobar_tabla(self.token[1]) is 'write':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'abre-par':
                    self.token = self.tokens.pop(0)
                    self.W()
                    if self.token[0] is 'cierr-par':
                        self.token = self.tokens.pop(0)
            if self.comprobar_tabla(self.token[1]) is 'prompt':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'abre-par':
                    self.token = self.tokens.pop(0)
                    if self.token[0] is 'id':
                        self.token = self.tokens.pop(0)
                        if self.token[0] is 'cierr-par':
                            self.token = self.tokens.pop(0)
        if self.comprobar_tabla(self.token[1]) is 'return':
                self.token = self.tokens.pop(0)
                self.Y()
        else:
            if self.token[0] is 'id':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'op-asign':
                    self.token = self.tokens.pop(0)
                    self.Q()
                elif self.token[0] is 'or-logic':
                    self.token = self.tokens.pop(0)
                    self.Q()
                elif self.token[0] is 'abre-par':
                    self.token = self.tokens.pop(0)
                    self.W()
                    if self.token[0] is 'cierr-par':
                        self.token = self.tokens.pop(0)
                else:
                    self.file_error.write("ERROR: en S no operador \n")
            else:
                self.file_error.write("ERROR: en S no id \n")

    def Q(self):
        self.token = self.tokens.pop(0)

    def comprobar_tabla(self, lexema):
        result = None
        try:
            result = self.tablaSimbolos[lexema]
        except IndexError:
            self.file_error.write("ERROR: id no definido \n")
        return result


def main():
    syntactic = Syntactic(sys.argv[1])
    syntactic.P()


if __name__ == '__main__':
    main()
