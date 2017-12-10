import sys

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])
# print tokens

gramar = open("gramarSintactico.txt", "w")
gramar.write('''//// Decidimos implementar el comentario //, cadenas con "",  el + y -, operador relacional ==, 
//// operador logico && y operadores de asignacion = y |=

Axioma = P

NoTerminales = { P T T1 O M M1 C C1 A A1 Q R R1 Z B }

Terminales = { var id write ( ) { } int chars bool function while cte-ent coment cadena return |= = + - ; == && , }

Producciones = {
P -> var T id ; ////1
P -> id B T1 M ////2
P -> write ( T1 M1 ) ; ////3 
P -> while ( C ) { Z Q } ////4 
P -> function T id ( A ) { Z Q R } ////5
P -> comment ////6
B -> = ////7
B -> |= ////8
T -> int ////9 
T -> chars ////10 
T1 -> cte-ent ////11 
T1 -> cadena ////12 
T1 -> id ////13 
O -> + ////14 
O -> - ////15 
M -> O T1 M ////16 
M -> ; ////17
M1 -> O T1 M1 ////18 
M1 -> lambda ////19 
C -> T1 == T1 C1 ////20 
C1 -> && T1 == T1 C1 ////21 
C1 -> lambda ////22 
A -> T id A1 ////23 
A1 -> , T id A1 ////24 
A1 -> lambda ////25 
Q -> P Q ////26
Q -> lambda ////27
R -> return T1 ; ////28
R -> lambda ////29 
Z -> comment ////30
Z -> lambda ////31
A -> lambda ////32
}''')

'''Pruebas
Des 5 11 24 13 26 31 27 1 9 28 29 13 ////pruebo function
Des 4 21 13 13 23 31 27 1 9 28 ////pruebo while
Des 2 7 13 17 15 12 18 ////prueba asignar valores
Des 1 9 ////prueba a inicializar
Des 3 13 20 ////prueba write
Des 6 31 o 6 32 ////prueba comentarios

Repasar las pruebas
'''


class Syntactic(object):
    def __init__(self):
        self.tokens = tokens
        self.tablaSimbolos = tabla
        self.semantico = open("errorSemantico.txt", "w")
        self.file_error = open("errorSintactico.txt", "w")
        self.parse = open("parseSintactico.txt", "w")
        self.parse.write("Des ")
        self.token = self.tokens.pop(0)
        self.tipos = list()
        self.fun = list()

    def axioma(self):
        if self.token[0] is 'fin':
            print "Analizado el fichero completo"
            return 0
        elif self.token[1] is 'var':  # Estado 1
            self.parse.write("1 ")
            self.token = self.tokens.pop(0)
            if self.token[1] is 'int':
                self.parse.write("9 ")
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
                        return -1
                else:
                    self.file_error.write("ERROR: en P falta id\n")
                    return -1
            elif self.token[1] is 'chars':
                self.parse.write("10 ")
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
                        return -1
                else:
                    self.file_error.write("ERROR: en P falta id\n")
                    return -1
            else:
                self.file_error.write("ERROR: en T tipo no definido\n")
                return -1
        elif self.token[1] == 'while':
            self.parse.write("4 ")
            self.token = self.tokens.pop(0)
            if self.token[1] == '(':
                self.token = self.tokens.pop(0)
                self.parse.write("20 ")
                aux = self.T()
                if aux is None:
                    return -1
                if self.token[1] == '=':
                    self.token = self.tokens.pop(0)
                    if self.token[1] == '=':
                        self.token = self.tokens.pop(0)
                        aux2 = self.T()
                        if aux2 is None:
                            return -1
                        if aux == aux2:
                            a = self.C1()
                            if a == -1:
                                return -1
                            if self.token[1] == ')':
                                self.token = self.tokens.pop(0)
                                if self.token[1] == '{':
                                    self.token = self.tokens.pop(0)
                                    if self.token[0] == 'comment':
                                        self.parse.write("6 ")
                                        self.parse.write("30 ")
                                        self.token = self.tokens.pop(0)
                                    elif self.token[0] == 'blanc':
                                        self.token = self.tokens.pop(0)
                                    else:
                                        self.parse.write("31 ")
                                    try:
                                        self.Q()
                                    except RuntimeError:  # Cosa que hay que arreglar
                                        self.file_error.close()
                                        file_error = open("errorSintactico.txt", "w")
                                        file_error.write("ERROR: fallo dentro del while")
                                        return -1
                                    return self.axioma()
                                else:
                                    self.file_error.write("ERROR: en P abrir corchete")
                                    return -1
                            else:
                                self.file_error.write("ERROR: en P falta cerrar parentesis")
                                return -1
                        else:
                            self.semantico.write("ERROR: no puedes comparar un tipo " + aux + " con un tipo " + aux2)
                            return -1
                    else:
                        self.file_error.write("ERROR: en C mal operacion de comparacion\n")
                        return -1
                else:
                    self.file_error.write("ERROR: en C falta operacion de comparacion\n")
                    return -1
            else:
                self.file_error.write("ERROR: en P falta parentesis en el while\n")
                return -1
        elif self.token[1] is 'function':
            self.parse.write("5 ")
            self.token = self.tokens.pop(0)
            ret = ""
            if self.token[1] == 'int':
                ret = 'int'
                self.parse.write("9 ")
            elif self.token[1] == 'chars':
                ret = 'chars'
                self.parse.write("10 ")
            else:
                self.file_error.write("ERROR: en P tipo de funcion no existe\n")
                return -1
            self.token = self.tokens.pop(0)
            if self.token[0] == 'id':
                name = self.token[1]
                self.fun.append([self.token[1], ret])
            else:
                self.file_error.write("ERROR: en P falta id en function\n")
                return -1
            self.token = self.tokens.pop(0)
            if self.token[1] == '(':
                self.token = self.tokens.pop(0)
                self.A()
                if self.token[1] == ')':
                    self.token = self.tokens.pop(0)
                    if self.token[1] == '{':
                        self.token = self.tokens.pop(0)
                        if self.token[0] == 'comment':
                            self.parse.write("6 ")
                            self.parse.write("30 ")
                            self.token = self.tokens.pop(0)
                        elif self.token[0] == 'blanc':
                            self.token = self.tokens.pop(0)
                        else:
                            self.parse.write("31 ")
                        try:
                            self.Q()
                            if self.token[1] == 'return':
                                self.parse.write("28 ")
                                self.token = self.tokens.pop(0)
                                val = self.T()
                                aux = self.fun.pop()
                                if aux[1] != val or aux[0] != name:
                                    self.file_error.write(
                                        "ERROR: en R no se puede devolver un tipo diferente a la funcion\n")
                                    return -1
                                if self.token[1] == ';':
                                    self.token = self.tokens.pop(0)
                                else:
                                    self.file_error.write("ERROR: en R falta punto y coma\n")
                                    return -1
                                if self.token[0] == 'blanc':
                                    self.token = self.tokens.pop(0)
                                if self.token[1] == '}':
                                    self.token = self.tokens.pop(0)
                                    return self.axioma()
                                else:
                                    self.file_error.write("ERROR: en P cerrar corchete")
                                    return -1
                            else:
                                self.parse.write("29 ")
                                return self.axioma()
                        except RuntimeError:  # Cosa que hay que arreglar
                            self.file_error.close()
                            file_error = open("errorSintactico.txt", "w")
                            file_error.write("ERROR: fallo dentro del function")
                            return -1
                    else:
                        self.file_error.write("ERROR: en P abrir corchete")
                        return -1
                else:
                    self.file_error.write("ERROR: en A mal formado\n")
                    return -1
            else:
                self.file_error.write("ERROR: en P falta abre parentesis en function\n")
                return -1
        elif self.token[1] is 'write':
            self.parse.write("3 ")
            self.token = self.tokens.pop(0)
            if self.token[1] is '(':
                self.token = self.tokens.pop(0)
                tipo = self.T()
                if self.token[1] is ')':
                    self.token = self.tokens.pop(0)
                else:
                    a = self.M1(tipo)
                    if a == -1:
                        return -1
                    self.token = self.tokens.pop(0)
                if self.token[1] is ';':
                    self.parse.write("19 ")
                    self.token = self.tokens.pop(0)
                    return self.axioma()
                else:
                    self.file_error.write("ERROR: en P falta punto y coma\n")
                    return -1
            else:
                self.file_error.write("ERROR: en P falta abre parentesis en write\n")
                return -1
        elif self.token[0] == 'blanc':
            self.token = self.tokens.pop(0)
        elif self.token[1] == '}':
            pass
        elif self.token[0] == 'comment':
            self.parse.write("6 ")
            self.parse.write("30 ")
            self.token = self.tokens.pop(0)
            return self.axioma()
        elif self.token[0] is 'id':
            self.parse.write("2 ")
            index = tabla.index(self.token[1])
            a = self.comprobar_declarado(index)
            if a is not None:
                self.semantico.write(a + "\n")
                return -1
            self.token = self.tokens.pop(0)
            if self.token[1] is '=':
                self.parse.write("7 ")
                self.token = self.tokens.pop(0)
                aux = self.T1(index)
                self.M(aux, index)
            elif self.token[1] is '|':
                self.token = self.tokens.pop(0)
                if self.token[1] is '=':
                    self.parse.write("8 ")
                    self.token = self.tokens.pop(0)
                    aux = self.T1(index)
                    self.M(aux, index)
                else:
                    self.file_error.write("ERROR: en B mal operador\n")
                    return -1
            else:
                self.file_error.write("ERROR: en B mal operador\n")
                return -1
        else:
            self.file_error.write("ERROR: en P palabra no valida\n")
            return -1

    def A(self):
        if self.token[1] == ',':
            self.parse.write("24 ")
            self.token = self.tokens.pop(0)
            return self.A()
        elif self.token[1] != ')':
            self.parse.write("23 ")
            self.token = self.tokens.pop(0)
            if self.token[1] == 'int':
                var = 'int'
                self.token = self.tokens.pop(0)
                if self.token[0] == 'id':
                    self.tipos.append([self.token[1], var])
            elif self.token[1] == 'chars':
                var = 'chars'
                self.token = self.tokens.pop(0)
                if self.token[0] == 'id':
                    self.tipos.append([self.token[1], var])
            else:
                self.file_error.write("ERROR: en A tipo de parametro no existe\n")
            self.token = self.tokens.pop(0)
            return self.A()
        else:
            self.parse.write("25 ")

    def Q(self):
        if self.token[1] == '}':
            self.parse.write("27 ")
            self.token = self.tokens.pop(0)
        elif self.token[1] == 'return':
            pass
        else:
            self.parse.write("26 ")
            self.axioma()
            self.Q()

    def C1(self):
        if self.token[1] != ')':
            self.parse.write("21 ")
            if self.token[1] == '&&':
                self.token = self.tokens.pop(0)
                aux = self.T()
                if aux is None:
                    return -1
                if self.token[1] == '=':
                    self.token = self.tokens.pop(0)
                    if self.token[1] == '=':
                        self.token = self.tokens.pop(0)
                        aux2 = self.T()
                        if aux2 is None:
                            return -1
                        if aux == aux2:
                            return self.C1()
                        else:
                            self.semantico.write("ERROR: no puedes comparar un tipo " + aux + " con un tipo " + aux2)
                            return -1
                    else:
                        self.file_error.write("ERROR: en C mal operacion de comparacion\n")
                        return -1
                else:
                    self.file_error.write("ERROR: en C mal operacion de comparacion\n")
                    return -1
            else:
                self.file_error.write("ERROR: en C falta operacion de comparacion\n")
                return -1
        else:
            self.parse.write("22 ")

    def M(self, aux, index):
        if self.token[1] is '+':
            self.parse.write("16 ")
            self.parse.write("14 ")
            self.token = self.tokens.pop(0)
            self.T1(index)
        elif self.token[1] is '-':
            self.parse.write("16 ")
            self.parse.write("15 ")
            self.token = self.tokens.pop(0)
            self.T1(index)
            if self.token[1] is ';':
                return self.axioma()
            else:
                return self.M(aux, index)
        else:
            if self.token[1] is ';':
                self.parse.write("17 ")
                self.token = self.tokens.pop(0)
                return self.axioma()
            else:
                self.file_error.write("ERROR: en M falta punto y coma")
        self.file_error.write("ERROR: en O operador no aceptado")

    def T1(self, index):
        if self.token[0] == 'int':
            self.parse.write("11 ")
            self.token = self.tokens.pop(0)
            aux = self.comprobar_tipos(index, 'int')
            if aux is not 'chars':
                if aux is not 'int':
                    self.semantico.write(aux + "\n")
                else:
                    return aux
            else:
                return aux
        elif self.token[0] == 'chars':
            self.parse.write("12 ")
            self.token = self.tokens.pop(0)
            aux = self.comprobar_tipos(index, 'chars')
            if aux is not 'chars':
                if aux is not 'int':
                    self.semantico.write(aux + "\n")
                else:
                    return aux
            else:
                return aux
        elif self.token[0] == 'id':
            self.parse.write("13 ")
            index1 = tabla.index(self.token[1])
            a = self.comprobar_declarado(index1)
            if a is not None:
                self.semantico.write(a + "\n")
            aux = self.comprobar_ids(index, index1)
            if aux is not 'chars':
                if aux is not 'int':
                    self.semantico.write(aux + "\n")
                else:
                    self.token = self.tokens.pop(0)
                    return aux
            else:
                self.token = self.tokens.pop(0)
                return aux
        else:
            if self.token[1] == '+':
                self.file_error.write("ERROR: en O mal operando\n")
            else:
                self.file_error.write("ERROR: en T1 mal tipo\n")

    def T(self):
        if self.token[0] == 'int':
            self.parse.write("11 ")
            self.token = self.tokens.pop(0)
            return 'int'
        elif self.token[0] == 'chars':
            self.parse.write("12 ")
            self.token = self.tokens.pop(0)
            return 'chars'
        elif self.token[0] == 'id':
            self.parse.write("13 ")
            index = tabla.index(self.token[1])
            a = self.comprobar_declarado(index)
            if a is not None:
                self.semantico.write(a + "\n")
                return None
            if self.comprobar_tipos(index, 'int') is 'int':
                self.token = self.tokens.pop(0)
                return 'int'
            else:
                self.token = self.tokens.pop(0)
                return 'chars'
        else:
            if self.token[1] == '+':
                self.file_error.write("ERROR: en O mal operando\n")
            else:
                self.file_error.write("ERROR: en T1 mal tipo\n")

    def M1(self, aux):
        if self.token[1] is '+':
            self.parse.write("18 ")
            self.parse.write("14 ")
            self.token = self.tokens.pop(0)
            tipo = self.T()
            if tipo is None:
                return -1
            if tipo != aux:
                self.semantico.write("ERROR: no se puede concatenar un tipo " + aux + " con un tipo " + tipo + "\n")
        elif self.token[1] is '-':
            self.parse.write("18 ")
            self.parse.write("15 ")
            self.token = self.tokens.pop(0)
            tipo = self.T()
            if tipo is None:
                return -1
            if tipo != aux:
                self.semantico.write("ERROR: no se puede concatenar un tipo " + aux + " con un tipo " + tipo + "\n")
            if self.token[1] is not ')':
                return self.M1(aux)
        else:
            self.file_error.write("ERROR: en O operador no aceptado\n")
            return -1

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
        except ValueError:
            return "ERROR: el id " + self.tablaSimbolos[index] + " no es tipo " + tipo

    def comprobar_declarado(self, id):
        if self.tipos.count([id, 'int']) is 0:
            if self.tipos.count([id, 'chars']) is 0:
                return "ERROR: variable no ceclarada"


def main():
    print "Fichero generado: gramarSintactico.txt"
    print "Fichero generado: erroresSintactico.txt"
    print "Fichero generado: parseSemantico.txt"
    print "Fichero generado: errorSemantico.txt"
    Syntactic().axioma()


if __name__ == '__main__':
    main()
