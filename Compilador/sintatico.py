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

#Alguns comandos foram reutilizados do exemplo fornecido com a linguagem TOY e foi adaptado para a linguagem MONGA
class Sintatico:

    def __init__(self): #foram colocados var1 e var2 para armazenar os dados na tabela e o modoPanico não foi possível de se implementar
        self.var1 = None
        self.valor = None
        self.var2 = None
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
            teste = self.tabsimb.items() #esta funcao serve para mostrar a tabela que esta sendo exportada para o arquivo.txt
            print(teste)
            # fim do reconhecimento do fonte

            self.lex.fechaArquivo()
            return not self.deuErro
        
    def tabela(self):
        texto = str(self.tabsimb.items())
        return texto
        
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

    def testaVarNaoDeclarada(self, var, linha): #funcao aproveitada
        if self.deuErro:
            return
        if not self.tabsimb.existeIdent(var):
            self.deuErro = True
            msg = "Variavel " + var + " nao declarada."
            self.semantico.erroSemantico(msg, linha)
            quit()
            
    def verificaInt(self, var, linha): #funcao feita para verificar se os valores em IF e WHILE e o retorno de operacoes logicas serem sempre int, caso não, ele retorna um erro semantico
        if self.deuErro:
            return
        if var is not int:
            self.deuErro = True
            msg = "Variavel " + var + " nao possui valor int."
            self.semantico.erroSemantico(msg, linha)
            quit()

    ##################################################################
    # Segue uma funcao para cada variavel da gramatica
    ##################################################################
    
    def program(self):
        prog = True
        while not self.tokenEsperadoEncontrado(tt.FIMARQ):
            prog = self.definition()
            
            if prog == False:
                break
    
    def definition(self):
        if self.tokenEsperadoEncontrado(tt.VAR):
            self.def_variable()
        elif self.tokenEsperadoEncontrado(tt.FUNCTION):
            self.def_function()
    
    def def_variable(self):
        self.consome(tt.VAR)
        var = self.salvaLexema()
        self.consome(tt.ID)
        self.consome(tt.DOISPTS)
        valor = self.type()
        self.consome(tt.PTEVIRG)
        if not self.tabsimb.existeIdent(var):
            self.tabsimb.declaraIdent(var, valor)
        else:
            pass
        
    def def_function(self):
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
        if self.tokenEsperadoEncontrado(tt.ID) or not self.tokenEsperadoEncontrado(tt.CLOSEPAR):
            self.parameter()
            while self.tokenEsperadoEncontrado(tt.VIRG):
                self.consome(tt.VIRG)
                self.paramter()
    
    def parameter(self):
        self.consome(tt.ID)
        self.salvaLexema()
        self.consome(tt.DOISPTS)
        self.type()
        
    def type(self):
        if self.tokenEsperadoEncontrado(tt.INT):
            valor = self.consome(tt.INT)
            return valor
        if self.tokenEsperadoEncontrado(tt.FLOAT):
            valor = self.consome(tt.FLOAT)
            return valor
        else:
            self.consome(tt.ID)
            return id
        
    def block(self):
        self.consome(tt.OPENCHA)
        while self.tokenEsperadoEncontrado(tt.VAR):
            self.def_variable()
        while (self.tokenEsperadoEncontrado(tt.IF)) or (self.tokenEsperadoEncontrado(tt.WHILE)) or (self.tokenEsperadoEncontrado(tt.ID)) or (self.tokenEsperadoEncontrado(tt.RETURN)) or (self.tokenEsperadoEncontrado(tt.PRINT)) or (self.tokenEsperadoEncontrado(tt.OPENCHA))or (self.tokenEsperadoEncontrado(tt.ID2)):
            self.statement()
        self.consome(tt.CLOSECHA)
    
    def statement(self):
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
        if self.tokenEsperadoEncontrado(tt.INT) or self.tokenEsperadoEncontrado(tt.ADD) or self.tokenEsperadoEncontrado(tt.SUB) or self.tokenEsperadoEncontrado(tt.NOT):
            self.exp()
            if self.tokenEsperadoEncontrado(tt.OPENCOL):
                self.consome(tt.OPENCOL)
                self.exp()
                self.consome(tt.CLOSECOL)
            elif self.tokenESperadoEncontrado(tt.PT):
                self.consome(tt.PT)
                self.consome(tt.ID)
        else:
            var = self.salvaLexema()
            linha = self.salvaLinha()
            self.consome(tt.ID)
            self.testaVarNaoDeclarada(var, linha)
            self.var1 = var
            return var
                
    def exp(self):
        return self.atrib()
        
    def atrib(self):
        self.Or()
        self.restoAtrib()
    
    def restoAtrib(self):
        if self.tokenEsperadoEncontrado(tt.ATRIB):
            self.consome(tt.ATRIB)
            self.atrib()
        else:
            pass
    
    def Or(self):
        self.And()
        self.restoOr()
    
    def restoOr(self):
        if self.tokenEsperadoEncontrado(tt.OR):
            self.consome(tt.OR)
            self.And()
            self.restoOr()
        else:
            pass

    def And(self):
        self.Not()
        self.restoAnd()

    def restoAnd(self):
        if self.tokenEsperadoEncontrado(tt.AND):
            self.consome(tt.AND)
            self.Not()
            self.restoAnd()
        else:
            pass

    def Not(self):
        if self.tokenEsperadoEncontrado(tt.NOT):
            self.consome(tt.NOT)
            self.var2 = self.salvaLexema()
            a1 = int(self.var2)
            self.Not()
            a1 =  -a1
            self.tabsimb.atribuiValor(self.var1, a1)
        else:
            self.rel()

    def rel(self):
        self.add()
        self.restoRel()

    def restoRel(self):
        if self.tokenEsperadoEncontrado(tt.COMPARIG):
           self.consome(tt.COMPARIG)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 == a2):
               return 1
           else:
               return 0
        if self.tokenEsperadoEncontrado(tt.COMPARDIF):
           self.consome(tt.COMPARDIF)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 != a2):
               return 1
           else:
               return 0
        if self.tokenEsperadoEncontrado(tt.MENOR):
           self.consome(tt.MENOR)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 < a2):
               return 1
           else:
               return 0
        if self.tokenEsperadoEncontrado(tt.MENORIG):
           self.consome(tt.MENORIG)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 <= a2):
               return 1
           else:
               return 0
        if self.tokenEsperadoEncontrado(tt.MAIOR):
           self.consome(tt.MAIOR)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 > a2):
               return 1
           else:
               return 0
        if self.tokenEsperadoEncontrado(tt.MAIORIG):
           self.consome(tt.MAIORIG)
           self.var2 = self.salvaLexema()
           linha = self.salvaLinha()
           a1 = int(self.valor)
           self.verificaInt(a1, linha)
           self.add()
           linha = self.salvaLinha()
           a2 = int(self.var2)
           self.verificaInt(a2, linha)
           if(a1 >= a2):
               return 1
           else:
               return 0
        else:
           pass
       
    def add(self):
        self.mult()
        self.restoAdd()
        
    def restoAdd(self):
        if self.tokenEsperadoEncontrado(tt.ADD):
           self.consome(tt.ADD)
           self.var2 = self.salvaLexema()
           a1 = int(self.valor)
           self.mult()
           self.restoAdd()
           a2 = int(self.var2)
           total = a1 + a2
           self.tabsimb.atribuiValor(self.var1, total)
        if self.tokenEsperadoEncontrado(tt.SUB):
            self.consome(tt.SUB)
            self.var2 = self.salvaLexema()
            a1 = int(self.valor)
            self.mult()
            self.restoAdd()
            a2 = int(self.var2)
            total = a1 - a2
            self.tabsimb.atribuiValor(self.var1, total)
        else:
           pass
       
    def mult(self):
        self.uno()
        self.restoMult()
        
    def restoMult(self):
        if self.tokenEsperadoEncontrado(tt.MULT):
           self.consome(tt.MULT)
           self.var2 = self.salvaLexema()
           a1 = int(self.valor)
           self.uno()
           self.restoMult()
           a2 = int(self.var2)
           total = a1 * a2
           self.tabsimb.atribuiValor(self.var1, total)
        if self.tokenEsperadoEncontrado(tt.DIV):
           self.consome(tt.DIV)
           self.var2 = self.salvaLexema()
           a1 = int(self.valor)
           self.uno()
           self.restoMult()
           a2 = int(self.var2)
           total = a1 / a2
           self.tabsimb.atribuiValor(self.var1, total)
        if self.tokenEsperadoEncontrado(tt.MOD):
           self.consome(tt.MOD)
           self.var2 = self.salvaLexema()
           a1 = int(self.valor)
           self.uno()
           self.restoMult()
           a2 = int(self.var2)
           total = a1 % a2
           self.tabsimb.atribuiValor(self.var1, total)
        else:
           pass
       
    def uno(self):
        if self.tokenEsperadoEncontrado(tt.ADD):
           self.consome(tt.ADD)
           self.uno()
        if self.tokenEsperadoEncontrado(tt.SUB):
           self.consome(tt.SUB)
           self.uno()
        else:
           self.fator()
           
    def fator(self):
        if self.tokenEsperadoEncontrado(tt.INT):
            self.valor = self.salvaLexema()
            self.tabsimb.atribuiValor(self.var1, self.valor)
            # self.valor = None
            # self.var1 = None
            self.consome(tt.INT)
        if self.tokenEsperadoEncontrado(tt.FLOAT):
            self.valor = self.salvaLexema()
            self.tabsimb.atribuiValor(self.var1, self.valor)
            # self.valor = None
            # self.var1 = None
            self.consome(tt.FLOAT)
        elif self.tokenEsperadoEncontrado(tt.OPENPAR):
            self.consome(tt.OPENPAR)
            self.atrib()
            self.consome(tt.CLOSEPAR)
            
    def call(self):
        self.consome(tt.OPENPAR)
        self.explist()
        self.consome(tt.CLOSEPAR)
    
    def explist(self):
        self.exp()
        while self.tokenEsperadoEncontrado(tt.VIRG):
            self.consome(tt.VIRG)
            self.exp()