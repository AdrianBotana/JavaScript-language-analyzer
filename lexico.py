import sys
import re
from tabla_de_simbolos import TablaDeSimbolos, Entry

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
    tabla = TablaDeSimbolos()
    file_pointer = open(file_name)
    file = file_pointer.readlines()
    lines = ""
    for line in file:
        lines = lines + line
    for tok in tokenize(lines):
        if tok[0] == 'iden':
            index = tabla.search_index(Entry(name=tok[1], type="PR"))
            if index != -1:
                file_tokens.write("<PR," + str(index) + ">\n")
                tokens.append(("PR", tabla[index]))
            else:
                index = tabla.search_index(Entry(name=tok[1], type="id"))
                if index != -1:
                    file_tokens.write("<id," + str(index) + ">\n")
                    tokens.append(("id", tabla[index]))
                else:
                    tabla.insert(Entry(name=tok[1], type="id"))
                    index = tabla.search_index(Entry(name=tok[1], type="id"))
                    file_tokens.write("<id," + str(index) + ">\n")
                    tokens.append(("id", tabla[index]))
        else:
            if tok[1] is not ' ':
                if tok[0] != 'eol':
                    tokens.append((tok[0], tok[1]))
            if tok[0] == 'eol' or tok[1] is ' ' or tok[1] is ';' or tok[1] is '=' or tok[1] is '+':
                file_tokens.write("<" + tok[0] + ">\n")
            else:
                file_tokens.write("<" + tok[0] + "," + tok[1] + ">\n")
    print "Fichero generado: tokensLexico.txt"
    print "Fichero generado: errorLexico.txt"
    tokens.append(('fin', 'se acabo'))
    return tokens, tabla


def main():
    gen_tokens(sys.argv[1])


if __name__ == '__main__':
    main()
