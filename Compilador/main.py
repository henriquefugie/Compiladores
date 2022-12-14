"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12

"""

from lexico import Lexico, TipoToken
from sintatico import Sintatico

if __name__ == '__main__':
   
   print('Tradutor Monga \n')
    
   #LEXICO
    
   nome = 'codigos/teste_sintatico.monga'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
      token = lex.getToken()
      print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
      if token.const == TipoToken.FIMARQ[0]:
         break
   lex.fechaArquivo()
    
    #SINTATICO
    
   nome = 'codigos/teste_sintatico.monga'
   parser = Sintatico()
   ok = parser.traduz(nome)
   if ok:
      print("Arquivo sintaticamente correto.")
    
    
 
