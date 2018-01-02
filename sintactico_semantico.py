import sys
import os

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])

gramar = open("gramarSintactico.txt", "w")
gramar.write('''Axioma = S

NoTerminales = { S B T E E1 E2 E3 F M O P V V1 R L L1}

Terminales = { var id write ( ) { } int chars bool cte-ent cadena function while return |= = + - ; == && , }

Producciones = {
S1 -> S S1 | eof
S -> var T id ; 
S -> id B E ; 
S -> write ( E ) ; 
S -> while ( E1 ) { P } 
S -> if ( E1 ) { P } 
S -> function T id ( V ){ P R }
T -> int | chars | bool 
E -> cte-ent M | cadena M | id F M
E1 -> E E3 //// 14
E3 -> == E E2 | lambda 
E2 -> && E1 | lambda 
F -> ( L ) | lambda 
M -> O E | lambda 
O -> + | - 
B -> = | |= 
V -> T id V1 
V1 -> , V | lambda 
R -> return E ; | lambda 
L -> E L1 | lambda 
L1 ->, L | lambda 
P -> S P | lambda 
}''')
error = open("errores.txt", "w")
parse = open("parse.txt", "w")
simbolos = open("tablaDeSimbolos.txt", "w")
funtion = open("tablaDeSimbolosFuncion.txt", "w")


class Conts:
    tabla = 0
    fun = 0


class Syntactic(object):
    def __init__(self):
        self.tokens = tokens
        self.tablaSimbolos = tabla
        self.token = self.tokens.pop(0)
        self.tipo = "no"
        self.ret = "no"
        self.f = 1
        self.fun = list()
        parse.write("Des ")
        simbolos.write("TABLA DE SIMBOLOS #1: \n \n")

    def s(self):
        self.tipo = "no"
        if self.token[0] == "PR":
            if self.token[1].name == "var":
                parse.write("1 ")
                self.token = self.tokens.pop(0)
                self.t()
                if self.token[1] == ";":
                    error.write("ERROR SINTACTICO: falta id para asignarle un tipo")
                    print "Error al analizar el fichero"
                    exit(-1)
                self.asignar_tipo(self.token[1], self.tipo)
                nombre = self.token[1].name
                self.token = self.tokens.pop(0)
                if self.token[1] == ";":
                    self.token = self.tokens.pop(0)
                    if self.ret == "no":
                        self.escribe_tabla(nombre, self.tipo)
                    else:
                        self.escribe_tabla(nombre, self.tipo, 0, funtion)
                    return self.s()
                else:
                    error.write("ERROR SINTACTICO: falta punto y coma en la declaracion de variables \n")
                    print "Error al analizar el fichero"
                    exit(-1)

            elif self.token[1].name == "write":
                parse.write("3 ")
                self.token = self.tokens.pop(0)
                if self.token[1] == "(":
                    self.token = self.tokens.pop(0)
                    if self.token[1] == ")":
                        error.write("ERROR SINTACTICO: falta contenido a escribir en el write \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                    self.e_aux()
                    if self.token[1] == ")":
                        self.token = self.tokens.pop(0)
                        if self.token[1] == ";":
                            self.token = self.tokens.pop(0)
                            return self.s()
                        else:
                            error.write("ERROR SINTACTICO: falta punto y coma en el write \n")
                            print "Error al analizar el fichero"
                            exit(-1)
                    else:
                        error.write("ERROR SINTACTICO: falta cerrar parentesis en el write \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    error.write("ERROR SINTACTICO: falta abrir parentesis en el write \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            elif self.token[1].name == "while":
                parse.write("4 ")
                self.token = self.tokens.pop(0)
                if self.token[1] == "(":
                    self.token = self.tokens.pop(0)
                    self.e1()
                    if self.token[1] == ")":
                        self.token = self.tokens.pop(0)
                        if self.token[1] == "{":
                            self.token = self.tokens.pop(0)
                            self.s()
                            if self.token[1] == "}":
                                self.token = self.tokens.pop(0)
                                return self.s()
                            else:
                                error.write("ERROR SINTACTICO: falta cerrar corchete en el while \n")
                                print "Error al analizar el fichero"
                                exit(-1)
                        else:
                            error.write("ERROR SINTACTICO: falta abrir corchete en el while \n")
                            print "Error al analizar el fichero"
                            exit(-1)
                    else:
                        error.write("ERROR SINTACTICO: falta cerrar parentesis en el while \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    error.write("ERROR SINTACTICO: falta abrir parentesis en el while \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            elif self.token[1].name == "if":
                parse.write("5 ")
                self.token = self.tokens.pop(0)
                if self.token[1] == "(":
                    self.token = self.tokens.pop(0)
                    self.e1()
                    if self.token[1] == ")":
                        self.token = self.tokens.pop(0)
                        if self.token[1] == "{":
                            self.token = self.tokens.pop(0)
                            self.s()
                            if self.token[1] == "}":
                                self.token = self.tokens.pop(0)
                                return self.s()
                            else:
                                error.write("ERROR SINTACTICO: falta cerrar corchete en el if \n")
                                print "Error al analizar el fichero"
                                exit(-1)
                        else:
                            error.write("ERROR SINTACTICO: falta abrir corchete en el if \n")
                            print "Error al analizar el fichero"
                            exit(-1)
                    else:
                        error.write("ERROR SINTACTICO: falta cerrar parentesis en el if \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    error.write("ERROR SINTACTICO: falta abrir parentesis en el if \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            elif self.token[1].name == "return":
                if self.ret != "no":
                    self.token = self.tokens.pop(0)
                    self.tipo = self.ret
                    self.ret = "ret"
                    parse.write("30 ")
                    self.e()
                    self.ret = self.tipo
                    if self.token[1] == ";":
                        self.token = self.tokens.pop(0)
                    else:
                        error.write("ERROR SINTACTICO: falta punto y coma tras el return \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    error.write("ERROR SEMANTICO: no puedes usar return si no se esta en una funcion \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            elif self.token[1].name == "function":
                parse.write("6 ")
                self.f = self.f + 1
                self.token = self.tokens.pop(0)
                self.t()
                if self.token[0] == "id":
                    if self.token[1].type == "no":
                        fun = self.token[1]
                        simbolos.write("* LEXEMA : '" + fun.name + "' (funcion) \n \t")
                        fun.type = self.tipo
                        simbolos.write("ATRIBUTOS : \n \t")
                        simbolos.write("+ tipo : '" + fun.type + "' \n \t")
                        self.ret = fun.type
                        self.token = self.tokens.pop(0)
                        if self.token[1] == "(":
                            self.token = self.tokens.pop(0)
                            if self.token[1] != ")":
                                ini = list()
                                result = self.v(ini)
                                self.asignar_tipo(fun, fun.type, result)
                                simbolos.write("+ parametros : " + str(result.__len__()) + "\n \t")
                                for x in result:
                                    simbolos.write("+ tipoparametro : '" + x[1] + "' \n \t")
                                simbolos.write("---------- ----------- \n")
                            else:
                                ini = list()
                                ini.append("empty")
                                self.asignar_tipo(fun, fun.type, ini)
                                result = None
                                simbolos.write("+ parametros : 0 \n \t")
                                simbolos.write("---------- ----------- \n")
                            funtion.write("TABLA DE FUNCION " + fun.name + " #" + str(self.f) + " : \n \n")
                            if result is not None:
                                for x in result:
                                    self.escribe_tabla(x[0], x[1], 1, funtion)
                            if self.token[1] == ")":
                                self.token = self.tokens.pop(0)
                                if self.token[1] == "{":
                                    self.token = self.tokens.pop(0)
                                    self.s()
                                    if self.token[1] == "}":
                                        if self.ret == "no":
                                            parse.write("31 ")  # COMPROBAR
                                        self.token = self.tokens.pop(0)
                                        self.ret = "no"
                                        funtion.write("\n")
                                        return self.s()
                                    else:
                                        error.write("ERROR SINTACTICO: falta cerrar corchete en el function \n")
                                        print "Error al analizar el fichero"
                                        exit(-1)
                                else:
                                    error.write("ERROR SINTACTICO: falta abrir corchete en el function \n")
                                    print "Error al analizar el fichero"
                                    exit(-1)
                            else:
                                error.write("ERROR SINTACTICO: falta cerrar parentesis en function \n")
                                print "Error al analizar el fichero"
                                exit(-1)
                        else:
                            error.write("ERROR SINTACTICO: falta abrir parentesis en function \n")
                            print "Error al analizar el fichero"
                            exit(-1)
                    else:
                        error.write("ERROR SEMANTICO: variable o funcion ya declarada, "
                                    "no puede pasar a ser una funcion \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    error.write("ERROR SINTACTICO: se necesita id para la funcion \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            else:
                error.write("ERROR SINTACTICO: palabra reservada no conocida: " + self.token[1].name + "\n")
                print "Error al analizar el fichero"
                exit(-1)
        elif self.token[0] == "id":
            parse.write("2 ")
            if self.token[1].type != "no":
                if self.token[1].argum != 0 and self.token[1].argum != 1:
                    # Llamada de funcion
                    self.llamar_fun()
                    if self.token[1] == ";":
                        self.token = self.tokens.pop(0)
                        return self.s()
                    else:
                        error.write("ERROR SINTACTICO: falta punto y coma en la llamada a funcion \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                else:
                    self.tipo = self.token[1].type
                    self.token = self.tokens.pop(0)
                    if self.token[1] == "|":
                        parse.write("26 ")
                        self.token = self.tokens.pop(0)
                        if self.token[1] != "=":
                            error.write("ERROR SINTACTICO: operador de asignacion no aceptado \n")
                            print "Error al analizar el fichero"
                            exit(-1)
                        self.token = self.tokens.pop(0)
                    elif self.token[1] == "=":
                        parse.write("25 ")
                        self.token = self.tokens.pop(0)
                    else:
                        error.write("ERROR SINTACTICO: operador de asignacion no aceptado \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                    if self.token[1] == ";":
                        error.write("ERROR SINTACTICO: falta segundo operando en la asignacion \n")
                        print "Error al analizar el fichero"
                        exit(-1)
                    self.e()
                    if self.token[1] == ";":
                        self.token = self.tokens.pop(0)
                        return self.s()
                    else:
                        error.write("ERROR SINTACTICO: falta punto y coma en la asignacion \n")
                        print "Error al analizar el fichero"
                        exit(-1)
            else:
                error.write("ERROR SEMANTICO: variable no declarada \n")
                print "Error al analizar el fichero"
                exit(-1)
        elif self.token[0] == "fin":
            parse.write("7 ")
        elif self.token[1] == "}":
            pass
        else:
            error.write("ERROR SINTACTICO: inicio de axioma desconocido \n")
            print "Error al analizar el fichero"
            print self.token
            exit(-1)

    def v(self, result):
        parse.write("27 ")
        if self.token[1].name == "int":
            parse.write("8 ")
        elif self.token[1].name == "chars":
            parse.write("9 ")
        elif self.token[1].name == "bool":
            parse.write("10 ")
        else:
            error.write("ERROR SINTACTICO: tipo no definido \n")
            print "Error al analizar el fichero"
            exit(-1)
        type = self.token[1].name
        self.token = self.tokens.pop(0)
        if self.token[0] == "id":
            entry = self.asignar_tipo(self.token[1], type, 1)
            self.tablaSimbolos.search_index(entry)
            result.append([self.token[1].name, type])
            self.token = self.tokens.pop(0)
            if self.token[1] == ",":
                parse.write("28 ")
                self.token = self.tokens.pop(0)
                return self.v(result)
            elif self.token[1] == ")":
                parse.write("29 ")
                return result
            else:
                error.write("ERROR SINTACTICO: simbolo incorrecto en los parametros \n")
                print "Error al analizar el fichero"
                exit(-1)
        else:
            error.write("ERROR SINTACTICO: los parametros tienen que ser ids \n")
            print "Error al analizar el fichero"
            exit(-1)

    def e(self, fu="nose"):
        if self.token[0] == "id":
            parse.write("13 ")
            if self.token[1].argum != 0 and self.token[1].argum != 1:
                # Llamada de funcion
                parse.write("19 ")
                re = self.llamar_fun()
                if fu != "nose":
                    error.write(
                        "ERROR SEMANTICO: se espera un parametro tipo " + self.tipo + ", no un tipo " + re
                        + " en la funcion " + fu)
                    print "Error al analizar el fichero"
                    exit(-1)
                if re != self.tipo:
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + re + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                    exit(-1)
            else:
                parse.write("20 ")
                if self.token[1].type == self.tipo:
                    self.token = self.tokens.pop(0)
                else:
                    if self.token[1].type == "no":
                        error.write("ERROR SEMANTICO: variable no declarada")
                        print "Error al analizar el fichero"
                        exit(-1)
                    if fu != "nose":
                        error.write(
                            "ERROR SEMANTICO: se espera un parametro tipo " + self.tipo + ", no un tipo " +
                            self.token[1].type + " en la funcion " + fu)
                        print "Error al analizar el fichero"
                        exit(-1)
                    if self.ret != "ret":
                        error.write(
                            "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[
                                1].type + " a un tipo " + self.tipo)
                        print "Error al analizar el fichero"
                        exit(-1)
                    else:
                        error.write(
                            "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[
                                1].type + " cuando se espera un "
                            + self.tipo + " en el return")
                        print "Error al analizar el fichero"
                        exit(-1)
        elif self.token[0] == 'int':
            parse.write("11 ")
            if self.token[0] == self.tipo:
                self.token = self.tokens.pop(0)
            else:
                if fu != "nose":
                    error.write(
                        "ERROR SEMANTICO: se espera un parametro tipo " + self.tipo + ", no un tipo " + self.token[0]
                        + " en la funcion " + fu)
                    print "Error al analizar el fichero"
                    exit(-1)
                if self.ret != "ret":
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[
                            0] + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                    exit(-1)
                else:
                    error.write(
                        "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[0] + " cuando se espera un "
                        + self.tipo + " en el return")
                    print "Error al analizar el fichero"
                    exit(-1)
        elif self.token[0] == "chars":
            parse.write("12 ")
            if self.token[0] == self.tipo:
                self.token = self.tokens.pop(0)
            else:
                if fu != "nose":
                    error.write(
                        "ERROR SEMANTICO: se espera un parametro tipo " + self.tipo + ", no un tipo " + self.token[0]
                        + " en la funcion " + fu)
                    print "Error al analizar el fichero"
                    exit(-1)
                if self.ret != "ret":
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[
                            0] + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                    exit(-1)
                else:
                    error.write(
                        "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[0] + " cuando se espera un "
                        + self.tipo + " en el return")
                    print "Error al analizar el fichero"
                    exit(-1)
        if self.token[1] == "+":
            parse.write("21 ")
            parse.write("23 ")
            if self.tipo == "bool":
                self.token = self.tokens.pop(0)
                error.write(
                    "ERROR SEMANTICO: no puedes concatenar un tipo " + self.token[
                        0] + " con un tipo " + self.tipo)
                print "Error al analizar el fichero"
                exit(-1)
            self.token = self.tokens.pop(0)
            return self.e()
        elif self.token[1] == "-":
            parse.write("21 ")
            parse.write("24 ")
            if self.tipo == "bool":
                error.write(
                    "ERROR SEMANTICO: no puedes concatenar un tipo " + self.token[
                        0] + " con un tipo " + self.tipo)
                print "Error al analizar el fichero"
                exit(-1)
            self.token = self.tokens.pop(0)
            return self.e()
        else:
            parse.write("22 ")

    def e1(self):
        parse.write("14 ")
        if self.token[1] == ")":
            error.write("ERROR SINTACTICO: falta condicion para analizar")
            print "Error al analizar el fichero"
            exit(-1)
        self.e_aux()
        if self.tipo == "bool":
            if self.token[1] == ")":
                parse.write("16 ")
        if self.token[1] == "=":
            parse.write("15 ")
            self.token = self.tokens.pop(0)
            if self.token[1] == "=":
                self.token = self.tokens.pop(0)
                if self.token[1] == ")" or self.token[1] == "&&":
                    error.write("ERROR SINTACTICO: falta segundo operando de la comparacion \n")
                    print "Error al analizar el fichero"
                    exit(-1)
                self.e()
                if self.token[1] == "&&":
                    parse.write("17 ")
                    self.token = self.tokens.pop(0)
                    return self.e1()
                parse.write("18 ")
            else:
                error.write("ERROR SINTACTICO: operador de comparacion desconocido. \n")
                print "Error al analizar el fichero"
                exit(-1)
        else:
            if self.token[1] != ")":
                error.write("ERROR SINTACTICO: operador de comparacion desconocido. \n")
                print "Error al analizar el fichero"
                exit(-1)
            parse.write("16 ")

    def e_aux(self):
        if self.token[0] == "id":
            parse.write("13 ")
            if self.token[1].argum != 0 and self.token[1].argum != 1:
                parse.write("19 ")
                # Llamada de funcion
                self.tipo = self.llamar_fun()
                return self.e()
            else:
                parse.write("20 ")
                if self.token[1].type != "no":
                    self.tipo = self.token[1].type
                    self.token = self.tokens.pop(0)
                    if self.tipo != "bool":
                        return self.e()
                else:
                    error.write("ERROR SEMANTICO: variable no declarada \n")
                    print "Error al analizar el fichero"
                    exit(-1)
        elif self.token[0] == "int":
            parse.write("11 ")
            self.tipo = self.token[0]
            self.token = self.tokens.pop(0)
            return self.e()
        elif self.token[0] == "chars":
            parse.write("12 ")
            self.tipo = self.token[0]
            self.token = self.tokens.pop(0)
            return self.e()
        elif self.token[0] == "bool":
            self.tipo = self.token[0]
            self.token = self.tokens.pop(0)
            print "no se que pasa"
        else:
            error.write("ERROR SINTACTICO: tipo no conocido \n")
            print "Error al analizar el fichero"
            exit(-1)

    def t(self):
        if self.token[0] != "PR":
            error.write("ERROR SINTACTICO: falta tipo o esta mal definido \n")
            print "Error al analizar el fichero"
            exit(-1)
        if self.token[1].name == "int":
            parse.write("8 ")
            self.tipo = "int"
            self.token = self.tokens.pop(0)
        elif self.token[1].name == "chars":
            parse.write("9 ")
            self.tipo = "chars"
            self.token = self.tokens.pop(0)
        elif self.token[1].name == "bool":
            parse.write("10 ")
            self.tipo = "bool"
            self.token = self.tokens.pop(0)
        else:
            error.write("ERROR SINTACTICO: tipo no conocido \n")
            print "Error al analizar el fichero"
            exit(-1)

    def asignar_tipo(self, entry, tipo, argum=0):
        self.tablaSimbolos.erase(entry)
        entry.type = tipo
        entry.argum = argum
        if tipo == "int":
            entry.desp = 2
        else:
            entry.desp = 16
        self.tablaSimbolos.insert(entry)
        return entry

    def escribe_tabla(self, lexema, tipo, art=0, tab=simbolos):
        if tipo == "int":
            desp = 2
        elif tipo == "chars":
            desp = 16
        else:
            desp = 1
        if tab.name == "tablaDeSimbolos.txt":
            aux = Conts.tabla
        else:
            aux = Conts.fun
        if art != 1:
            tab.write("* LEXEMA : '" + lexema + "' \n \t")
            tab.write("ATRIBUTOS : \n \t")
            tab.write("+ tipo : '" + tipo + "'\n \t")
            if aux == 0:
                tab.write("+ desplazamiento : '" + str(aux) + "'\n \t")
            else:
                tab.write("+ desplazamiento : '-" + str(aux) + "'\n \t")
            tab.write("---------- ----------- \n")
        else:
            tab.write("* LEXEMA : '" + lexema + "' (parametro)\n \t")
            tab.write("ATRIBUTOS : \n \t")
            tab.write("+ tipo : '" + tipo + "'\n \t")
            tab.write("+ desplazamiento : '-" + str(aux) + "'\n \t")
            tab.write("---------- ----------- \n")
        if tab.name == "tablaDeSimbolos.txt":
            Conts.tabla = Conts.tabla + desp
        else:
            Conts.fun = Conts.fun + desp

    def llamar_fun(self):
        arg = self.token[1].argum
        ret = self.token[1].type
        name = self.token[1].name
        if self.tipo != "no":
            if self.tipo != ret:
                error.write("ERROR SEMANTICO: no se puede asignar un tipo " + ret + " a un tipo " + self.tipo + "\n")
                print "Error al analizar el fichero"
                exit(-1)
        aux = self.tipo
        self.token = self.tokens.pop(0)
        if self.token[1] == "(":
            self.token = self.tokens.pop(0)
            if arg[0] != "empty":
                parse.write("32 ")
                if self.token[1] == ")":
                    error.write("ERROR SINTACTICO: falta parametros en la llamada a funcion " + name + "\n")
                    print "Error al analizar el fichero"
                    exit(-1)
                while arg.__len__() > 0:
                    self.tipo = arg.pop(0)[1]
                    if self.token[1] == ")":
                        error.write("ERROR SINTACTICO: falta parametros en la llamada a funcion " + name + "\n")
                        print "Error al analizar el fichero"
                        exit(-1)
                    self.e(name)
                    if arg.__len__() > 0:
                        if self.token[1] == ",":
                            self.token = self.tokens.pop(0)
                            parse.write("34 ")
                        else:
                            error.write("ERROR SINTACTICO: falta coma entre parametros de llamada en funcion " + name)
                            print "Error al analizar el fichero"
                            exit(-1)
                parse.write("35 ")
            else:
                arg.pop(0)
                parse.write("33 ")
            if self.token[1] == ",":
                error.write("ERROR SINTACTICO: sobran parametros en la llamada a funcion" + name + "\n")
                print "Error al analizar el fichero"
                exit(-1)
            if self.token[1] == ")":
                if arg.__len__() > 0:
                    error.write("ERROR SINTACTICO: falta parametros en la llamada a funcion " + name + "\n")
                    print "Error al analizar el fichero"
                    exit(-1)
                self.token = self.tokens.pop(0)
                self.tipo = aux
                return ret
            else:
                error.write("ERROR SINTACTICO: falta cerrar parentesis en la llamada a funcion " + name + "\n")
                print "Error al analizar el fichero"
                exit(-1)
        else:
            error.write("ERROR SINTACTICO: falta abrir parentesis en la llamada a funcion " + name + "\n")
            print "Error al analizar el fichero"
            exit(-1)
        return ret


def main():
    print "Fichero generado: gramarSintactico.txt"
    print "Fichero generado: parse.txt"
    print "Fichero generado: tablaDeSimbolos.txt"
    s = Syntactic()
    s.s()
    funtion.close()
    fun = open("tablaDeSimbolosFuncion.txt", "r")
    cont = fun.read()
    if cont == '':
        os.remove("tablaDeSimbolosFuncion.txt")
    else:
        print "Fichero generado: tablaDeSimbolosFuncion.txt"
    print "Fichero analizado correctamente"


if __name__ == '__main__':
    main()
