import sys

from lexico import gen_tokens

tokens, tabla = gen_tokens(sys.argv[1])


class Syntactic(object):
    def __init__(self):
        self.tokens = tokens
        self.tablaSimbolos = tabla
        self.file_error = open("errorSintactico.txt", "w")
        self.token = self.tokens.pop(0)

    def axioma(self):
        if self.token[1] is 'var':
            self.token = self.tokens.pop(0)
            if self.token[1] is 'int' or self.token[1] is 'chars' or self.token[1] is 'bool':
                self.token = self.tokens.pop(0)
            else:
                print "porque" + str(self.token)
                self.file_error.write("ERROR: en T tipo no valido")
            if self.token[0] is 'id':
                self.token = self.tokens.pop(0)
                if self.token[0] is 'puntocoma':
                    self.token = self.tokens.pop(0)
        elif self.tokens[1] is 'while':
            print self.token
        elif self.tokens[1] is 'function':
            print self.token
        elif self.tokens[1] is 'write':
            print self.token
        elif self.token[0] is 'id':
            print self.token
        else:
            self.file_error.write("ERROR: en P terminal no valido")


def main():
    Syntactic().axioma()
    print tokens


if __name__ == '__main__':
    main()
