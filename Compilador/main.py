"""

Nome Discente: Henrique Fugie de Macedo
Matrícula: 0056151
Data: 14/12

"""
#bibliotecas usadas para utilizar o sistema através do terminal
import sys
import getopt

from lexico import Lexico, TipoToken
from sintatico import Sintatico

#funcao que possibilita a exeucacao do compilador pelo terminal
def myfunc(argv):
   nome1 = ""
   salvar = ""
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
   print('Tradutor Monga')
   nome1 = input('Digite o nome do arquivo .monga que deseja utilizar na analise: ') #Recebe o nome do arquivo que o analisador lexico e sintatico/semantico vão analisar
   
   print('Lexico')
   #LEXICO
   nome = ('codigos/'+nome1)
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
      token = lex.getToken()
      print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
      if token.const == TipoToken.FIMARQ[0]:
         break
   lex.fechaArquivo()
    
   print('Sintatico e Semantico')
    #SINTATICO e Semantico
   nome = ('codigos/'+nome1)
   parser = Sintatico()
   ok = parser.traduz(nome)
   if ok:
     tabela = parser.tabela()
     with open("codigos/"+salvar, "w") as f:
          f.write(tabela)
          
     print("Arquivo sintaticamente e semanticamente correto.")
    
if __name__ == '__main__':
   myfunc(sys.argv)
   
