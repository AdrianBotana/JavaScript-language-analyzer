class Entry(object):

    def __init__(self, name="no", type="no", argum=0, desp=0):
        self.name = name
        self.type = type
        self.argum = argum
        self.desp = desp


class TablaDeSimbolos(object):
    tabla = list()
    tabla.append(Entry(name="chars", type="PR", desp=16))
    tabla.append(Entry(name="function", type="PR", desp=16))
    tabla.append(Entry(name="int", type="PR", desp=16))
    tabla.append(Entry(name="return", type="PR", desp=16))
    tabla.append(Entry(name="var", type="PR", desp=16))
    tabla.append(Entry(name="while", type="PR", desp=16))
    tabla.append(Entry(name="write", type="PR", desp=16))
    tabla.append(Entry(name="if", type="PR", desp=16))
    tabla.append(Entry(name="bool", type="PR", desp=16))

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
