"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12

"""
#Esta tabela foi reutilizda dos materiais fornecidos pelo professor Mario
class TabelaSimbolos:

    def __init__(self):
        self.tabela = dict()

    def existeIdent(self, nome):
        if nome in self.tabela:
            return True
        else:
            return False

    def declaraIdent(self, nome, valor):
        if not self.existeIdent(nome):
            self.tabela[nome] = valor
            return True
        else:
            return False

    def pegaValor(self, nome):
        return self.tabela[nome]

    def atribuiValor(self, nome, valor):
        self.tabela[nome] = valor

    def items(self):
        return self.tabela