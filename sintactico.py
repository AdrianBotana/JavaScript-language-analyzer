import sys

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])
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
P -> Z ////6
B -> = ////7
B -> |= ////8
T -> int ////9 
T -> chars ////10 
T -> bool ////11 
T1 -> cte-ent ////12 
T1 -> cadena ////13 
T1 -> id ////14 
O -> + ////15 
O -> - ////16 
M -> O T1 M ////17 
M -> ; ////18
M1 -> O T1 M1 ////19 
M1 -> lambda ////20 
C -> T1 == T1 C1 ////21 
C1 -> && T1 == T1 C1 ////22 
C1 -> lambda ////23 
A -> T1 id A1 ////24 
A1 -> , T1 id A1 ////25 
A1 -> lambda ////26 
Q -> P Q ////27
Q -> lambda ////28
R -> return T1 ; ////29
R -> lambda ////30
Z -> coment ////31
Z -> lambda ////32 
}''')


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

    def axioma(self):
        if self.token[1] is 'var':  # Estado 1
            self.parse.write("1 ")
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
                        return -1
                else:
                    self.file_error.write("ERROR: en P falta id\n")
                    return -1
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
                        return -1
                else:
                    self.file_error.write("ERROR: en P falta id\n")
                    return -1
            else:
                self.file_error.write("ERROR: en T tipo no definido\n")
                return -1
        elif self.tokens[1] is 'while':
            print self.token
        elif self.tokens[1] is 'function':
            print self.token
        elif self.tokens[1] is 'write':
            print self.token
        elif self.token[0] is 'id':
            index = tabla.index(self.token[1])
            a = self.comprobar_declarado(index)
            if a is not None:
                self.semantico.write(a + "\n")
                return -1
            self.token = self.tokens.pop(0)
            if self.token[1] is '=':
                self.token = self.tokens.pop(0)
                aux = self.T1(index)
                if aux is 'int':
                    if aux is 'chars':
                        self.M(aux, index)
            elif self.token[1] is '|':
                self.token = self.tokens.pop(0)
                if self.token[1] is '=':
                    self.token = self.tokens.pop(0)
                    aux = self.T1(index)
                    if aux is 'int':
                        if aux is 'chars':
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
        else:
            if self.token[1] is ';':
                self.token = self.tokens.pop(0)
                return self.axioma()
            else:
                self.file_error.write("ERROR: en M falta punto y coma")
                return -1
        self.file_error.write("ERROR: en M operador no aceptado")

    def T1(self, index):
        if self.token[0] == 'int':
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
            self.file_error.write("ERROR: en T1 mal tipo\n")

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
        except IndexError:
            return "ERROR: el id " + self.tablaSimbolos[index] + " no es tipo " + tipo

    def comprobar_declarado(self, index):
        if self.tipos.count([index, 'int']) is 0:
            if self.tipos.count([index, 'chars']) is 0:
                return "ERROR: variable no ceclarada"


def main():
    print "Fichero generado: erroresSintactico.txt"
    print "Fichero generado: gramarSintactico.txt"
    print "Fichero generado: parseSintactico.txt"
    Syntactic().axioma()


if __name__ == '__main__':
    main()
