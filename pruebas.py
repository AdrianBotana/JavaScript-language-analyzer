import sys
import re
from tablaSimbolos import tabla_simbolos

token_pattern = r"""
(?P<iden>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<entero>[0-9]+)
|(?P<cadena>"[a-zA-Z_][a-zA-Z0-9_]*")
|(?P<punto>\.)
|(?P<open_variable>[$][{])
|(?P<abrir_llave>[{])
|(?P<cerrar_llave>[}])
|(?P<abrir_par>[(])
|(?P<cerrar_par>[)])
|(?P<salto_linea>\n)
|(?P<tabulacion>\t)
|(?P<blanco>\s+)
|(?P<asig>[=])
|(?P<igual_cond>==)
|(?P<and_cond>&&)
|(?P<comentario>//[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<aritmetico>[+])
|(?P<aritmetico1>[-])
|(?P<aritmetico2>--)
|(?P<puntocoma>[;])
"""

token_re = re.compile(token_pattern, re.VERBOSE)


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
        raise TokenizerException('Analizador paro en posicion %r de %r' % (
            pos, len(text)))


def main():
    tabla = tabla_simbolos()
    file_pointer = open(sys.argv[1])
    file = file_pointer.readlines()
    lines = ""
    for line in file:
            lines = lines + line
    print lines
    for tok in tokenize(lines):
        if tok[0] == 'iden':
            try:
                index = tabla.index(tok[1])
            except ValueError:
                tabla.append(tok[1])
        print tok


if __name__ == '__main__':
    main()