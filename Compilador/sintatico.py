"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12


Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias.
    
Linguagem Monga

    program : { definition }

    definition : def-variable | def-function

    def-variable : VAR ID ':' type ';'

    type : ID

    def-function : FUNCTION ID '(' parameters ')' [':' type] block

    parameters : [ parameter { ',' parameter } ]

    parameter : ID ':' type

    block : '{' { def-variable } { statement } '}'

    statement : IF exp block [ ELSE block ]
            | WHILE exp block
            | var '=' exp ';'
            | RETURN [ exp ] ';'
            | call ';'
            | '@' exp ';'
            | block

    var : ID | exp '[' exp ']' | exp '.' ID

    <exp> -> <atrib>
    <atrib> -> <or> <restoAtrib>
    <restoAtrib> -> '=' <atrib> | lambda
    <or> -> <and> <restoOr>
    <restoOr> -> '||' <and> <restoOr> | lambda
    <and> -> <not> <restoAnd>
    <restoAnd> -> '&&' <not> <restoAnd> | lambda
    <not> -> '!' <not> | <rel>
    <rel> -> <add> <restoRel>
    <restoRel> -> '==' <add> | '!=' <add>
                | '<' <add> | '<=' <add> 
                | '>' <add> | '>=' <add> | lambda
    <add> -> <mult> <restoAdd>
    <restoAdd> -> '+' <mult> <restoAdd> 
                | '-' <mult> <restoAdd> | lambda
    <mult> -> <uno> <restoMult>
    <restoMult> -> '*' <uno> <restoMult>
                |  '/' <uno> <restoMult> 
                |  '%' <uno> <restoMult> | lambda
    <uno> -> '+' <uno> | '-' <uno> | <fator>
    <fator> -> 'NUMint' | 'NUMfloat' | '(' <atrib> ')'

    call : ID '(' explist ')'

    explist : [ exp { ',' exp } ]

"""

from lexico import TipoToken as tt, Token, Lexico
from tabela import TabelaSimbolos
from semantico import Semantico

class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.deuErro = False
        self.modoPanico = False
        self.tokensDeSincronismo = [tt.PTEVIRG, tt.FIMARQ]

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
            self.program()
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
    
    def program(self):
        print('program')
        prog = True
        while not self.tokenEsperadoEncontrado(tt.FIMARQ):
            prog = self.definition()
            
            if prog == False:
                break
    
    def definition(self):
        print('definition')
        if self.tokenEsperadoEncontrado(tt.VAR):
            self.def_variable()
        elif self.tokenEsperadoEncontrado(tt.FUNCTION):
            self.def_function()
        else:
            return False
    
    def def_variable(self):
        print('def_variable')
        self.consome(tt.VAR)
        id = self.consome(tt.ID)
        self.consome(tt.DOISPTS)
        tipo = self.type()
        self.consome(tt.PTEVIRG)
        
    def def_function(self):
        print('def_function')
        self.consome(tt.FUNCTION)
        self.consome(tt.ID2)
        self.consome(tt.OPENPAR)
        self.parameters()
        self.consome(tt.CLOSEPAR)
        if self.tokenEsperadoEncontrado(tt.DOISPTS):
            self.consome(tt.DOISPTS)
            self.type()
        self.block()
        
    def parameters(self):
        print('parameters')
        if self.tokenEsperadoEncontrado(tt.ID) or not self.tokenEsperadoEncontrado(tt.CLOSEPAR):
            self.parameter()
            while self.tokenEsperadoEncontrado(tt.VIRG):
                self.consome(tt.VIRG)
                self.paramter()
    
    def parameter(self):
        print('parameter')
        self.consome(tt.ID)
        self.consome(tt.DOISPTS)
        self.type()
        
    def type(self):
        print('type')
        if self.tokenEsperadoEncontrado(tt.INT):
            return self.consome(tt.INT)
        if self.tokenEsperadoEncontrado(tt.FLOAT):
            return self.consome(tt.FLOAT)
        else:
            return self.consome(tt.ID)
        
    def block(self):
        print('block')
        self.consome(tt.OPENCHA)
        while self.tokenEsperadoEncontrado(tt.VAR):
            self.def_variable()
        while (self.tokenEsperadoEncontrado(tt.IF)) or (self.tokenEsperadoEncontrado(tt.WHILE)) or (self.tokenEsperadoEncontrado(tt.ID)) or (self.tokenEsperadoEncontrado(tt.RETURN)) or (self.tokenEsperadoEncontrado(tt.PRINT)) or (self.tokenEsperadoEncontrado(tt.OPENCHA))or (self.tokenEsperadoEncontrado(tt.ID2)):
            self.statement()
        self.consome(tt.CLOSECHA)
    
    def statement(self):
        print('statement')
        if self.tokenEsperadoEncontrado(tt.IF):
            self.consome(tt.IF)
            self.exp()
            self.block()
            if self.tokenEsperadoEncontrado(tt.ELSE):
                self.consome(tt.ELSE)
                self.block()
        
        if self.tokenEsperadoEncontrado(tt.WHILE):
            self.consome(tt.WHILE)
            self.exp()
            self.block()
            
        if self.tokenEsperadoEncontrado(tt.ID):
            self.var()
            self.consome(tt.ATRIB)
            self.exp()
            self.consome(tt.PTEVIRG)
            
        if self.tokenEsperadoEncontrado(tt.RETURN):
            self.consome(tt.RETURN)
            if not self.tokenEsperadoEncontrado(tt.PTEVIRG):
                self.exp()
            self.consome(tt.PTEVIRG)
        if self.tokenEsperadoEncontrado(tt.ID2):
            self.consome(tt.ID2)
            self.call()
            self.consome(tt.PTEVIRG)
        if self.tokenEsperadoEncontrado(tt.PRINT):
            self.consome(tt.PRINT)
            self.exp()
            self.consome(tt.PTEVIRG)
        if self.tokenEsperadoEncontrado(tt.OPENCHA):
            self.block()
    
    def var(self):
        print('var')
        if self.tokenEsperadoEncontrado(tt.INT) or self.tokenEsperadoEncontrado(tt.ADD) or self.tokenEsperadoEncontrado(tt.SUB) or self.tokenEsperadoEncontrado(tt.NOT):
            self.exp()
            if self.tokenEsperadoEncontrado(tt.OPENCOL):
                print('Colchete encontrado')
                self.consome(tt.OPENCOL)
                self.exp()
                self.consome(tt.CLOSECOL)
            elif self.tokenESperadoEncontrado(tt.PT):
                self.consome(tt.PT)
                self.consome(tt.ID)
        else:
            self.consome(tt.ID)
    def exp(self):
        print('exp')
        return self.atrib()
        
    def atrib(self):
        print('atrib')
        self.Or()
        self.restoAtrib()
    
    def restoAtrib(self):
        print('restoAtrib')
        if self.tokenEsperadoEncontrado(tt.ATRIB):
            self.consome(tt.ATRIB)
            self.atrib()
        else:
            pass
    
    def Or(self):
        print('Or')
        self.And()
        self.restoOr()
    
    def restoOr(self):
        print('restoOr')
        if self.tokenEsperadoEncontrado(tt.OR):
            self.consome(tt.OR)
            self.And()
            self.restoOr()
        else:
            pass

    def And(self):
        print('And')
        self.Not()
        self.restoAnd()

    def restoAnd(self):
        print('restoAnd')
        if self.tokenEsperadoEncontrado(tt.AND):
            self.consome(tt.AND)
            self.Not()
            self.restoAnd()
        else:
            pass

    def Not(self):
        print('Not')
        if self.tokenEsperadoEncontrado(tt.NOT):
            self.consome(tt.NOT)
            self.Not()
        else:
            self.rel()

    def rel(self):
        print('rel')
        self.add()
        self.restoRel()

    def restoRel(self):
        print('restoRel')
        if self.tokenEsperadoEncontrado(tt.COMPARIG):
           self.consome(tt.COMPARIG)
           self.add()
        if self.tokenEsperadoEncontrado(tt.COMPARDIF):
           self.consome(tt.COMPARDIF)
           self.add()
        if self.tokenEsperadoEncontrado(tt.MENOR):
           self.consome(tt.MENOR)
           self.add()
        if self.tokenEsperadoEncontrado(tt.MENORIG):
           self.consome(tt.MENORIG)
           self.add()
        if self.tokenEsperadoEncontrado(tt.MAIOR):
           self.consome(tt.MAIOR)
           self.add()
        if self.tokenEsperadoEncontrado(tt.MAIORIG):
           self.consome(tt.MAIORIG)
           self.add()
        else:
           pass
       
    def add(self):
        print('add')
        self.mult()
        self.restoAdd()
        
    def restoAdd(self):
        print('restoAdd')
        if self.tokenEsperadoEncontrado(tt.ADD):
           self.consome(tt.ADD)
           self.mult()
           self.restoAdd()
        if self.tokenEsperadoEncontrado(tt.SUB):
            self.consome(tt.SUB)
            self.mult()
            self.restoAdd()
        else:
           pass
       
    def mult(self):
        print('mult')
        self.uno()
        self.restoMult()
        
    def restoMult(self):
        print('restoMult')
        if self.tokenEsperadoEncontrado(tt.MULT):
           self.consome(tt.MULT)
           self.uno()
           self.restoMult()
        if self.tokenEsperadoEncontrado(tt.DIV):
           self.consome(tt.DIV)
           self.uno()
           self.restoMult()
        if self.tokenEsperadoEncontrado(tt.MOD):
           self.consome(tt.MOD)
           self.uno()
           self.restoMult()
        else:
           pass
       
    def uno(self):
        print('uno')
        if self.tokenEsperadoEncontrado(tt.ADD):
           self.consome(tt.ADD)
           self.uno()
        if self.tokenEsperadoEncontrado(tt.SUB):
           self.consome(tt.SUB)
           self.uno()
        else:
           self.fator()
           
    def fator(self):
        print('fator')
        if self.tokenEsperadoEncontrado(tt.INT):
            self.consome(tt.INT)
        if self.tokenEsperadoEncontrado(tt.FLOAT):
            self.consome(tt.FLOAT)
        elif self.tokenEsperadoEncontrado(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.atrib()
            self.consome(tt.CLOSEPAR)
        
            
    def call(self):
        print('call')
        self.consome(tt.OPENPAR)
        self.explist()
        self.consome(tt.CLOSEPAR)
    
    def explist(self):
        print('explist')
        self.exp()
        while self.tokenEsperadoEncontrado(tt.VIRG):
            self.consome(tt.VIRG)
            self.exp()