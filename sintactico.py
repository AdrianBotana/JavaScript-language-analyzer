import sys

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])
print tokens


class Syntactic(object):
    def __init__(self):
        self.tokens = tokens
        self.tablaSimbolos = tabla
        self.file_error = open("errorSintactico.txt", "w")
        self.token = self.tokens.pop(0)
        self.tipos = list()

    def axioma(self):
        if self.token[1] is 'var':  # Estado 1
            self.token = self.tokens.pop(0)
            if self.token[1] is 'int':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'id':
                    index = tabla.index(self.token[1])
                    self.tipos.append([index, 'int'])
                    self.token = self.tokens.pop(0)
                    if self.token[1] is ';':
                        self.token = self.tokens.pop(0)
                        return self.axioma()
                    else:
                        self.file_error.write("ERROR: en P falta punto y coma\n")
                else:
                    self.file_error.write("ERROR: en P falta id\n")
            elif self.token[1] is 'chars':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'id':
                    index = tabla.index(self.token[1])
                    self.tipos.append([index, 'chars'])
                    self.token = self.tokens.pop(0)
                    if self.token[1] is ';':
                        self.token = self.tokens.pop(0)
                        return self.axioma()
                    else:
                        self.file_error.write("ERROR: en P falta punto y coma\n")
                else:
                    self.file_error.write("ERROR: en P falta id\n")
            else:
                self.file_error.write("ERROR: en T tipo no definido\n")
        elif self.tokens[1] is 'while':
            print self.token
        elif self.tokens[1] is 'function':
            print self.token
        elif self.tokens[1] is 'write':
            print self.token
        elif self.token[0] is 'id':
            index = tabla.index(self.token[1])
            self.token = self.tokens.pop(0)
            if self.token[1] is '=':
                self.token = self.tokens.pop(0)
                aux = self.T1(index)
                if aux is None:
                    self.file_error.write("ERROR: en T1 mal tipo\n")
                if self.token[1] is ';':
                    self.token = self.tokens.pop(0)
                    return self.axioma()
                else:
                    self.M(aux, index)
            else:
                self.file_error.write("ERROR: en P mal operador\n")
        else:
            self.file_error.write("ERROR: en P palabra no valida\n")

    def M(self, aux, index):
        if self.token[1] is '+':
            self.token = self.tokens.pop(0)
            self.T1(index)
        elif self.token[1] is '-':
            self.token = self.tokens.pop(0)
            self.T1(index)
            if self.token[1] is ';':
                return self.axioma()
            else:
                return self.M(aux, index)
        elif self.token[1] is ';':
            self.token = self.tokens.pop(0)
            return self.axioma()
        else:
            self.file_error.write("ERROR: en M operando no aceptado")

    def T1(self, index):
        if self.token[0] == 'int':
            self.token = self.tokens.pop(0)
            aux = self.comprobar_tipos(index, 'int')
            if aux is not 'int':
                print aux
            else:
                return aux
        elif self.token[0] == 'chars':
            self.token = self.tokens.pop(0)
            aux = self.comprobar_tipos(index, 'chars')
            if aux is not 'chars':
                print aux
            else:
                return aux
        elif self.token[0] == 'id':
            index1 = tabla.index(self.token[1])
            aux = self.comprobar_ids(index, index1)
            if aux is not 'chars':
                if aux is not 'int':
                    print aux
                else:
                    self.token = self.tokens.pop(0)
                    return aux
            else:
                self.token = self.tokens.pop(0)
                return aux

    def comprobar_ids(self, index, index1):
        try:
            if self.tipos.count([index, 'int']) is 0:
                if self.tipos.count([index1, 'int']) is not 0:
                    return "ERROR: el id " + self.tablaSimbolos[index] + " es tipo chars y el id " + self.tablaSimbolos[
                        index1] + " es tipo int"
                else:
                    return 'int'
            else:
                if self.tipos.count([index1, 'int']) is 0:
                    return "ERROR: el id " + self.tablaSimbolos[index] + " es tipo int y el id " + self.tablaSimbolos[
                        index1] + " es tipo chars"
                else:
                    return 'chars'
        except IndexError:
            pass

    def comprobar_tipos(self, index, tipo):
        try:
            aux = [index, tipo]
            self.tipos.index(aux)
            return tipo
        except:
            return "ERROR: el id " + self.tablaSimbolos[index] + " no es tipo " + tipo


def main():
    print "Fichero generado: erroresSintactico.txt"
    print "Fichero generado: sintacticGramar.txt"
    Syntactic().axioma()


if __name__ == '__main__':
    main()
