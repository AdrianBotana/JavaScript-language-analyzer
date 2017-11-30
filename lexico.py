import sys
import re
from tablaSimbolos import tabla_simbolos

token_pattern = r"""
(?P<chars>"[a-zA-Z_ ][a-zA-Z0-9_ ]*")
|(?P<int>[0-9]+)
|(?P<iden>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<abrir_llave>[{])
|(?P<cerrar_llave>[}])
|(?P<abrir_par>[(])
|(?P<cerrar_par>[)])
|(?P<asig_or>[|])
|(?P<eol>\n)
|(?P<tab>\t)
|(?P<blanc>\s+)
|(?P<asig>[=])
|(?P<igual_cond>==)
|(?P<and_cond>&&)
|(?P<comment>//[a-zA-Z_ ][a-zA-Z0-9_ ]*)
|(?P<arit>[+])
|(?P<dec>--)
|(?P<arit1>[-])
|(?P<puntocoma>[;])
"""

token_re = re.compile(token_pattern, re.VERBOSE)
file_tokens = open("tokensLexico.txt", "w")
file_error = open("errorLexico.txt", "w")
tokens = list()


class TokenizerException(Exception): pass


def tokenize(text):
    pos = 0
    while True:
        m = token_re.match(text, pos)
        if not m: break
        pos = m.end()
        tokname = m.lastgroup
        tokvalue = m.group(tokname)
        yield tokname, tokvalue
    if pos != len(text):
        file_error.write('ERROR: se ha encontrado el token no valido %s en la posicion posicion %r de %r' % (
            text[pos], pos, len(text)))


def gen_tokens(file_name):
    tabla = tabla_simbolos()
    file_pointer = open(file_name)
    file = file_pointer.readlines()
    lines = ""
    for line in file:
        lines = lines + line
    for tok in tokenize(lines):
        if tok[0] == 'iden':
            try:
                index = tabla.index(tok[1])
                if index < 55:
                    file_tokens.write("<PR," + str(index) + ">\n")
                    tokens.append(("PR", tabla[index]))
                else:
                    file_tokens.write("<id," + str(index) + ">\n")
                    tokens.append(("id", tabla[index]))
            except ValueError:
                tabla.append(tok[1])
                index = tabla.index(tok[1])
                file_tokens.write("<id," + str(index) + ">\n")
                tokens.append(("id", tabla[index]))
        else:
            if tok[1] is not ' ':
                if tok[0] != 'eol':
                    tokens.append((tok[0],tok[1]))
            if tok[0] == 'eol' or tok[1] is ' ' or tok[1] is ';' or tok[1] is '=' or tok[1] is '+':
                file_tokens.write("<" + tok[0] + ">\n")
            else:
                file_tokens.write("<" + tok[0] + "," + tok[1] + ">\n")
    print "Fichero generado: tokensLexico.txt"
    return tokens, tabla
