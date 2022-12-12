"""
    
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


    Tokens::
    ID | ATRIB | PTOVIRG | ARIT | OPENPAR | CLOSEPAR | NUM | ERROR | EOF

    Palavras reservadas::
    IF | WHILE | ELSE | ARIT | OPENPAR | CLOSEPAR | NUM | ERROR | EOF

"""

from os import path

class TipoToken:
    ID = (1, 'id')
    
    
    
    IDENT = (1, 'ident')
    ATRIB = (2, '=')
    READ = (3, 'read')
    PTOVIRG = (4, ';')
    PRINT = (5, 'print')
    ADD = (6, '+')
    MULT = (7, '*')
    OPENPAR = (8, '(')
    CLOSEPAR = (9, ')')
    NUM = (10, 'numero')
    ERROR = (11, 'erro')
    FIMARQ = (12, 'fim-de-arquivo')

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'print': TipoToken.PRINT, 'read': TipoToken.READ }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha = self.linha + 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif car in {'=', ';', '+', '*', '(', ')'}:
                    estado = 4
                elif car == '#':
                    estado = 5
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    # terminou o nome
                    self.ungetChar(car)
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TipoToken.IDENT, lexema, self.linha)
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isdigit()):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.NUM, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':
                    return Token(TipoToken.ATRIB, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTOVIRG, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.ADD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULT, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
            elif estado == 5:
                # consumindo comentario
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                self.ungetChar(car)
                estado = 1


if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = 'exemplo.toy'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TipoToken.FIMARQ[0]:
           break
   lex.fechaArquivo()
