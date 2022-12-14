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
from os import path

class TipoToken:
    ID = (1, 'id')
    OPENPAR = (2, '(')
    CLOSEPAR = (3, ')')
    OPENCHA = (4, '{')
    CLOSECHA = (5, '}')
    OPENCOL = (6, '[')
    CLOSECOL = (7, ']')
    ATRIB = (8, '=')
    DOISPTS = (9, ':')
    PTEVIRG = (10, ';')
    VIRG = (11, ',')
    PT = (12, '.')
    ID2 = (38, 'id2')
    
    VAR = (13, 'var')
    FUNCTION = (14, 'function')
    IF = (15, 'if')
    ELSE = (16, 'else')
    RETURN = (17, 'return')
    WHILE = (18, 'while')
    PRINT = (19, '@')
    
    INT = (20, 'int')
    FLOAT = (21, 'float')
    
    ERRO = (22, 'erro')
    FIMARQ = (23, 'fim-de-arquivo')
    
    AND = (24, '&&')
    OR = (25, '||')
    NOT = (26, '!')
    
    ADD = (27, '+')
    MULT = (28, '*')
    SUB = (29, '-')
    MOD = (30, '%')
    DIV = (31, '/')
    
    MENOR = (32, '<')
    MAIOR = (33, '>')
    MENORIG = (34, '<=')
    MAIORIG = (35, '>=')
    COMPARIG = (36, '==')
    COMPARDIF  = (37, '!=')
    
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
    reservadas = {'VAR': TipoToken.VAR, 'FUNCTION': TipoToken.FUNCTION, 'IF': TipoToken.IF, 'ELSE': TipoToken.ELSE, 'RETURN': TipoToken.RETURN, 'WHILE': TipoToken.WHILE, 'PRINT': TipoToken.PRINT, 'int': TipoToken.INT, 'float': TipoToken.FLOAT}

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
                return c

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        car2 = ''
        
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
                elif car in {'(', ')', '{', '}', '[', ']', '=', ':', ';', ',', '.', '@', '&', '|', '!', '+', '*', '-', '%', '/', '<', '>'}:
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
                    if len(lexema) > 32:
                        return Token(TipoToken.ERRO, lexema, self.linha)
                    else:
                        car2 = self.getChar()
                        if car2 == '(':
                            self.ungetChar(car2)
                            return Token(TipoToken.ID2, lexema, self.linha)
                        else:
                            self.ungetChar(car2)
                            return Token(TipoToken.ID, lexema, self.linha)
                    
            elif estado == 3:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()
                
                if car == '.':
                    estado = 6
                else:
                    if car is None or (not car.isdigit()):
                        # terminou o numero
                        self.ungetChar(car)
                        return Token(TipoToken.INT, lexema, self.linha)
            elif estado == 4:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                
                if car == '(':
                    return Token(TipoToken.OPENPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.CLOSEPAR, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.OPENCHA, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.CLOSECHA, lexema, self.linha)
                elif car == '[':
                    return Token(TipoToken.OPENCOL, lexema, self.linha)
                elif car == ']':
                    return Token(TipoToken.CLOSECOL, lexema, self.linha)
                elif car == '=':
                    car2 = self.getChar()
                    if car2 != '=':
                        self.ungetChar(car2)
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '==':
                            return Token(TipoToken.COMPARIG, lexema, self.linha)
                elif car == ':':
                    return Token(TipoToken.DOISPTS, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTEVIRG, lexema, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '.':
                    return Token(TipoToken.PT, lexema, self.linha)
                elif car == '@':
                    return Token(TipoToken.PRINT, lexema, self.linha)
                elif car == '&':
                    car2 = self.getChar()
                    if car2 != '&':
                        self.ungetChar(car2)
                        return Token(TipoToken.ERRO, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '&&':
                            return Token(TipoToken.AND, lexema, self.linha)
                elif car == '|':
                    car2 = self.getChar()
                    if car2 != '|':
                        self.ungetChar(car2)
                        return Token(TipoToken.ERRO, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '||':
                            return Token(TipoToken.OR, lexema, self.linha)
                elif car == '!':
                    car2 = self.getChar()
                    if car2 != '=':
                        self.ungetChar(car2)
                        return Token(TipoToken.NOT, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '!=':
                            return Token(TipoToken.COMPARDIF, lexema, self.linha)
                elif car == '+':
                    return Token(TipoToken.ADD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULT, lexema, self.linha)
                elif car == '-':
                    return Token(TipoToken.SUB, lexema, self.linha)
                elif car == '%':
                    return Token(TipoToken.MOD, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.DIV, lexema, self.linha)
                elif car == '<':
                    car2 = self.getChar()
                    if car2 != '=':
                        self.ungetChar(car2)
                        return Token(TipoToken.MENOR, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '<=':
                            return Token(TipoToken.MENORIG, lexema, self.linha)
                elif car == '>':
                    car2 = self.getChar()
                    if car2 != '=':
                        self.ungetChar(car2)
                        return Token(TipoToken.MAIOR, lexema, self.linha)
                    else:
                        lexema = lexema + car2
                        if lexema == '>=':
                            return Token(TipoToken.MAIORIG, lexema, self.linha)
                
            elif estado == 5:
                # consumindo comentario
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                self.ungetChar(car)
                estado = 1
                
            elif estado == 6:
                lexema = lexema + car
                car = self.getChar()
                if not car.isdigit():
                    self.ungetChar(car)
                    return Token(TipoToken.FLOAT, lexema, self.linha)