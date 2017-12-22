class Entry(object):

    def __init__(self, name="no", type="no", argum=0, desp=0):
        self.name = name
        self.type = type
        self.argum = argum
        self.desp = desp


class TablaDeSimbolos(object):
    tabla = list()
    #TODO: Arreglar toda la tabla de simbolos
    tabla.append(Entry(name="chars", type="PR"))
    tabla.append(Entry("function", "PR"))
    tabla.append(Entry(name="int", type="PR"))
    tabla.append(Entry("return", "PR"))
    tabla.append(Entry("var", "PR"))
    tabla.append(Entry("while", "PR"))
    tabla.append(Entry("write", "PR"))
    tabla.append(Entry(name="if", type="PR"))

    def __getitem__(self, item):
        return self.tabla.__getitem__(item)

    def insert(self, content):
        self.tabla.append(content)

    def search_index(self, content):
        aux = [element for element in self.tabla if element.name == content.name]

        if not aux:
            return -1
        else:
            return self.tabla.index(aux[0])

    def erase(self, content):
        self.tabla.pop(self.tabla.index(content))
