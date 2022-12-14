"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12

"""
import sys
import getopt

from lexico import Lexico, TipoToken
from sintatico import Sintatico

def myfunc(argv):
   salvar = ""
   arg_output = ""
   arg_user = ""
   arg_help = "{0} -t <nome_arquivo>".format(argv[0])
    
   try:
        opts, args = getopt.getopt(argv[1:], "ht:", ["help", "nome_arquivo="])
   except:
        print(arg_help)
        sys.exit(2)
    
   for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-t", "--nome_arquivo"):
            salvar = arg
   print('Tradutor Monga \n')
   
   print('Lexico')
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
    
   print('Sintatico')
    #SINTATICO
    
   nome = 'codigos/teste_sintatico.monga'
   parser = Sintatico()
   ok = parser.traduz(nome)
   if ok:
      print("Arquivo sintaticamente correto.")
    
if __name__ == '__main__':
   myfunc(sys.argv)
