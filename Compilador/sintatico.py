"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12

 Linguagem Toy

    Gramatica::

    F* --> C Rf
    Rf --> C Rf | lambda
    C  --> A | R | P
    A --> ident = E ;
    R --> read ( ident ) ;
    P --> print ( ident ) ;

    E --> M Rs
    Rs --> + M Rs | lambda
    M --> Op Rm
    Rm --> * Op Rm | lambda
    Op --> ( E ) | num | ident

    Tokens::

    IDENT ATRIB READ PTOVIRG PRINT ADD MULT OPENPAR CLOSEPAR NUM ERROR FIMARQ

    Comentarios::

    iniciam com # ate o fim da linha

"""

from lexico import TipoToken as tt, Token, Lexico
from tabela import TabelaSimbolos
from semantico import Semantico

class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.deuErro = False

    def traduz(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.deuErro = False
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            # inicio reconhecimento do fonte
            self.tabsimb = TabelaSimbolos()
            self.semantico = Semantico()
            self.F()
            self.consome( tt.FIMARQ )
            # fim do reconhecimento do fonte

            self.lex.fechaArquivo()
            return not self.deuErro

    def tokenEsperadoEncontrado(self, token):
        (const, msg) = token
        if self.tokenAtual.const == const:
            return True
        else:
            return False

    def consome(self, token):
        if self.tokenEsperadoEncontrado(token):
            self.tokenAtual = self.lex.getToken()
        else:
            self.deuErro = True
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def salvaLexema(self):
        return self.tokenAtual.lexema

    def salvaLinha(self):
        return self.tokenAtual.linha

    def testaVarNaoDeclarada(self, var, linha):
        if self.deuErro:
            return
        if not self.tabsimb.existeIdent(var):
            self.deuErro = True
            msg = "Variavel " + var + " nao declarada."
            self.semantico.erroSemantico(msg, linha)
            quit()


    ##################################################################
    # Segue uma funcao para cada variavel da gramatica
    ##################################################################

    def F(self):
        self.C()
        self.Rf()

    def Rf(self):
        if self.tokenEsperadoEncontrado( tt.FIMARQ ):
            pass
        else:
            self.C()
            self.Rf()

    def C(self):
        if self.tokenEsperadoEncontrado( tt.READ ):
            self.R()
        elif self.tokenEsperadoEncontrado( tt.PRINT ):
            self.P()
        else:
            self.A()

    def A(self):
        var = self.salvaLexema()
        self.consome( tt.IDENT )
        self.consome( tt.ATRIB )
        valor = self.E()
        self.consome( tt.PTOVIRG )
        if not self.tabsimb.existeIdent(var):
            self.tabsimb.declaraIdent(var, valor)
        else:
            self.tabsimb.atribuiValor(var, valor)

    def R(self):
        self.consome( tt.READ )
        self.consome( tt.OPENPAR )
        var = self.salvaLexema()
        linha = self.salvaLinha()
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )

        valor = eval(input("Input: "))
        self.testaVarNaoDeclarada(var, linha)
        self.tabsimb.atribuiValor(var, valor)

    def P(self):
        self.consome( tt.PRINT )
        self.consome( tt.OPENPAR )
        var = self.salvaLexema()
        linha = self.salvaLinha()
        self.consome( tt.IDENT )
        self.consome( tt.CLOSEPAR )
        self.consome( tt.PTOVIRG )
        self.testaVarNaoDeclarada(var, linha)
        valor = self.tabsimb.pegaValor(var)
        print(valor)

    def E(self):
        valor1 = self.M()
        valor2 = self.Rs(valor1)
        return valor2

    def Rs(self, valor1):
        if self.tokenEsperadoEncontrado( tt.ADD ):
            self.consome( tt.ADD )
            valor2 = self.M()
            valor3 = valor1 + valor2
            return self.Rs(valor3)
        else:
            return valor1

    def M(self):
        valor1 = self.Op()
        valor2 = self.Rm(valor1)
        return valor2

    def Rm(self, valor1):
        if self.tokenEsperadoEncontrado( tt.MULT ):
            self.consome( tt.MULT )
            valor2 = self.Op()
            valor3 = valor1 * valor2
            return self.Rm(valor3)
        else:
            return valor1

    def Op(self):
        if self.tokenEsperadoEncontrado( tt.OPENPAR ):
            self.consome( tt.OPENPAR )
            valor = self.E()
            self.consome( tt.CLOSEPAR )
            return valor
        elif self.tokenEsperadoEncontrado( tt.NUM ):
            num = self.salvaLexema()
            self.consome( tt.NUM )
            return int(num)
        else:
            var = self.salvaLexema()
            linha = self.salvaLinha()
            self.consome(tt.IDENT)
            self.testaVarNaoDeclarada(var, linha)
            valor = self.tabsimb.pegaValor(var)
            return valor

if __name__== "__main__":

   nome = 'exemplo.toy'
   parser = Sintatico()
   parser.traduz(nome)
