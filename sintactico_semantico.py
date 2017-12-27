import sys

import os

import time

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])

gramar = open("gramarSintactico.txt", "w")
gramar.write('''Axioma = S

NoTerminales = { S B T E E1 E2 M O P V V1 R}

Terminales = { var id write ( ) { } int chars cte-ent cadena function while return |= = + - ; == && , }

Producciones = {
S -> var T id ; S //// 1
S -> id B E ; S //// 2
S -> write ( E ) ; S //// 3
S -> while ( E1 ) { P } S //// 4
S -> if ( E1 ) { P } S //// 5
S -> function T id ( V ){ P R } S //// 6
T -> int | chars //// 7, 8
E -> cte-ent M | cadena M | id M //// 9, 10, 11
E1 -> E == E E2 //// 12
E2 -> && E1 | lambda //// 13, 14
M -> O E | lambda //// 15, 16
O -> + | - //// 17, 18
B -> = | |= //// 19, 20
V -> T id V1 //// 21
V1 -> , V | lambda //// 22, 23
R -> return E ; | lambda //// 24, 25
}''')
error = open("errores.txt", "w")
parse = open("parse.txt", "w")
simbolos = open("tablaDeSimbolos.txt", "w")
funtion = open("tablaDeSimbolosFuncion.txt", "w")


class Syntactic(object):
    def __init__(self):
        self.tokens = tokens
        self.tablaSimbolos = tabla
        self.token = self.tokens.pop(0)
        self.tipo = "no"
        self.ret = "no"
        self.f = 1
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
                    parse.write("24 ")
                    self.token = self.tokens.pop(0)
                    self.tipo = self.ret
                    self.ret = "ret"
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
                                            parse.write("25 ")
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
                        error.write("ERROR SEMANTICO: variable ya declarada, no puede ser funcion \n")
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
                self.tipo = self.token[1].type
                self.token = self.tokens.pop(0)
                if self.token[1] == "|":
                    parse.write("20 ")
                    self.token = self.tokens.pop(0)
                    self.token = self.tokens.pop(0)
                elif self.token[1] == "=":
                    parse.write("19 ")
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
            return 0
        elif self.token[1] == "}":
            pass
        else:
            error.write("ERROR SINTACTICO: inicio de axioma desconocido \n")
            print "Error al analizar el fichero"
            print self.token
            exit(-1)

    def v(self, result):
        parse.write("21 ")
        if self.token[1].name == "int":
            parse.write("7 ")
            type = self.token[1].name
            self.token = self.tokens.pop(0)
            if self.token[0] == "id":
                entry = self.asignar_tipo(self.token[1], type, 1)
                self.tablaSimbolos.search_index(entry)
                result.append([self.token[1].name, type])
                self.token = self.tokens.pop(0)
                if self.token[1] == ",":
                    self.token = self.tokens.pop(0)
                    parse.write("22 ")
                    return self.v(result)
                elif self.token[1] == ")":
                    parse.write("23 ")
                    return result
                else:
                    error.write("ERROR SINTACTICO: simbolo incorrecto en los parametros \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            else:
                error.write("ERROR SINTACTICO: los parametros tienen que ser ids \n")
                print "Error al analizar el fichero"
                exit(-1)
        elif self.token[1].name == "chars":
            parse.write("8 ")
            type = self.token[1].name
            self.token = self.tokens.pop(0)
            if self.token[0] == "id":
                entry = self.asignar_tipo(self.token[1], type, 1)
                self.tablaSimbolos.search_index(entry)
                result.append([self.token[1].name, type])
                self.token = self.tokens.pop(0)
                if self.token[1] == ",":
                    self.token = self.tokens.pop(0)
                    parse.write("22 ")
                    return self.v(result)
                elif self.token[1] == ")":
                    parse.write("23 ")
                    return result
                else:
                    error.write("ERROR SINTACTICO: simbolo incorrecto en los parametros \n")
                    print "Error al analizar el fichero"
                    exit(-1)
            else:
                error.write("ERROR SINTACTICO: los parametros tienen que ser ids \n")
                print "Error al analizar el fichero"
                exit(-1)

        else:
            error.write("ERROR SINTACTICO: tipo no definido \n")
            print "Error al analizar el fichero"
            exit(-1)

    def e(self):
        if self.token[0] == "id":
            parse.write("11 ")
            if self.token[1].type == self.tipo:
                self.token = self.tokens.pop(0)
            else:
                if self.token[1].type == "no":
                    error.write("ERROR SEMANTICO: variable no declarada")
                    print "Error al analizar el fichero"
                    exit(-1)
                if self.ret != "ret":
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[1].type + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                    exit(-1)
                else:
                    error.write(
                        "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[1].type + " cuando se espera un "
                        + self.tipo + " en el return")
                    print "Error al analizar el fichero"
                    exit(-1)
        elif self.token[0] == 'int':
            parse.write("9 ")
            if self.token[0] == self.tipo:
                self.token = self.tokens.pop(0)
            else:
                if self.ret != "ret":
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[0] + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                    exit(-1)
                else:
                    error.write(
                        "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[0] + " cuando se espera un "
                        + self.tipo + " en el return")
                    print "Error al analizar el fichero"
                    exit(-1)
        elif self.token[0] == "chars":
            parse.write("10 ")
            if self.token[0] == self.tipo:
                self.token = self.tokens.pop(0)
            else:
                if self.ret != "ret":
                    error.write(
                        "ERROR SEMANTICO: no puedes asignar o comparar un tipo " + self.token[0] + " a un tipo " + self.tipo)
                    print "Error al analizar el fichero"
                else:
                    error.write(
                        "ERROR SEMANTICO: no puedes devolver un tipo " + self.token[0] + " cuando se espera un "
                        + self.tipo + " en el return")
                    print "Error al analizar el fichero"
                    exit(-1)
                exit(-1)
        if self.token[1] == "+":
            parse.write("15 ")
            parse.write("17 ")
            self.token = self.tokens.pop(0)
            return self.e()
        elif self.token[1] == "-":
            parse.write("15 ")
            parse.write("18 ")
            self.token = self.tokens.pop(0)
            return self.e()
        else:
            parse.write("16 ")
        # intentar tratar el caso de error para otros operadores

    def e1(self):
        parse.write("12 ")
        if self.token[1] == ")":
            error.write("ERROR SINTACTICO: falta condicion para analizar")
            print "Error al analizar el fichero"
            exit(-1)
        self.e_aux()
        if self.token[1] == "=":
            self.token = self.tokens.pop(0)
            if self.token[1] == "=":
                self.token = self.tokens.pop(0)
                if self.token[1] == ")" or self.token[1] == "&&":
                    error.write("ERROR SINTACTICO: falta segundo operando de la comparacion \n")
                    print "Error al analizar el fichero"
                    exit(-1)
                self.e()
                if self.token[1] == "&&":
                    parse.write("13 ")
                    self.token = self.tokens.pop(0)
                    return self.e1()
                parse.write("14 ")
            else:
                error.write("ERROR SINTACTICO: operador de comparacion desconocido. \n")
                print "Error al analizar el fichero"
                exit(-1)
        else:
            if self.token[1] != ")":
                error.write("ERROR SINTACTICO: operador de comparacion desconocido. \n")
                print "Error al analizar el fichero"
                exit(-1)

    def e_aux(self):
        if self.token[0] == "id":
            parse.write("11 ")
            if self.token[1].type != "no":
                self.tipo = self.token[1].type
                self.token = self.tokens.pop(0)
                return self.e()
            else:
                error.write("ERROR SEMANTICO: variable no declarada \n")
                print "Error al analizar el fichero"
                exit(-1)
        elif self.token[0] == "int":
            parse.write("9 ")
            self.tipo = self.token[0]
            self.token = self.tokens.pop(0)
            return self.e()
        elif self.token[0] == "chars":
            parse.write("10 ")
            self.tipo = self.token[0]
            self.token = self.tokens.pop(0)
            return self.e()
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
            parse.write("7 ")
            self.tipo = "int"
            self.token = self.tokens.pop(0)
        elif self.token[1].name == "chars":
            parse.write("8 ")
            self.tipo = "chars"
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
        else:
            desp = 16
        if art != 1:
            tab.write("* LEXEMA : '" + lexema + "' \n \t")
            tab.write("ATRIBUTOS : \n \t")
            tab.write("+ tipo : '" + tipo + "'\n \t")
            tab.write("+ desplazamiento : '" + str(desp) + "'\n \t")
            tab.write("---------- ----------- \n")
        else:
            tab.write("* LEXEMA : '" + lexema + "' (parametro)\n \t")
            tab.write("ATRIBUTOS : \n \t")
            tab.write("+ tipo : '" + tipo + "'\n \t")
            tab.write("+ desplazamiento : '" + str(desp) + "'\n \t")
            tab.write("---------- ----------- \n")


def main():
    print "Fichero generado: gramarSintactico.txt"
    print "Fichero generado: parse.txt"
    print "Fichero generado: tablaDeSimbolos.txt"
    Syntactic().s()
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
