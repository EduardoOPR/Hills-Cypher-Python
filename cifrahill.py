
'''
 - Para cifrar um documento de texto basta executar o comando: python cifrahill.py -enc textoclaro.txt -out textocifrado.txt
  Para isso tem que ter o python e a biblioteca do numpy instalados
  O documento de texto para esse caso tem que ter o nome textoclaro, ou pelo menos tem que ser o mesmo do arquivo de texto que estiver no mesmo local do programa
  A cifra não está funcionando para caracteres com acentos

 - Para deficfrar execute o comando: python cifrahill.py -dec textocifrado.txt -out textoclaro.txt
  o arquivo tem que estar com o nome textocifrado (também pode alterar o o nome do arquivo no comando que vai na linha de comando se preferir)

 Para alterar a chave basta mudar o valor da variável chave, porém seu tamanho tem que ser um quadrado perfeito
 
'''

import numpy as np
import argparse

#O tamanho da chave precisa ser um quadrado perfeito (4, 9, 16 ...)
chave = "testabcde"

#Mapeamento do alfabeto, indo do asci 32 (space) até o 126 (~), símbolo para número
MA = {chr(i): i - 32 for i in range(32, 127)}

#Mapeamento reverso, para quando for necessário converter os números para símbolos
MA_rev = {i - 32:chr(i)  for i in range(32, 127)}

#Mapeando os símbolos da chave
chave_numeros = [MA[i] for i in chave]

#Tamanho do bloco para saber o tamanho da matriz
TB = int(pow(len(chave_numeros), 1/2))
#Definindo as matrizes como 2x2 ou 3x3
if(TB != 2):
  TB = 3

#Transformando a chave em uma matriz
chave_matriz = np.array(chave_numeros).reshape(TB, TB)

#Função que recebe um texto claro e o retorna um texto cifrado
def cifrar(TextoClaro):
  #Garantindo que o texto claro seja divisível pelo tamanho da chave
  while(not (len(TextoClaro) % TB == 0)):
    TextoClaro += "0"

  #Mapeando os símbolos do texto claro para a cifra
  TextoClaro_numeros = [MA[i] for i in TextoClaro]

  #Transformando a lista em um array
  TextoClaro_array = np.array(TextoClaro_numeros)

  #Dividindo o texto claro em n blocos, onde o tamanho é dado pelo tamanho do texto claro / tamanho da matriz da chave 
  TextoClaro_blocos = np.split(TextoClaro_array, len(TextoClaro_array)//TB)

  #Obtendo os blocos do texto cifrado através da multiplicação das matrizes do texto claro, com a chave e fazendo o módulo ao final para que os valorem permanecem dentro da faixa
  TC_blocos = [np.matmul(TextoClaro_blocos[i], chave_matriz) % 95 for i in range(len(TextoClaro)//TB)]

  #Concatenando os blocos em um array
  TC_array = np.concatenate(TC_blocos)

  #Fazendo o mapeamento inverso do array para sair o texto cifrado
  TC = [MA_rev[TC_array[i]] for i in range(len(TC_array))]
  return(''.join(TC))

#Função que recebe um texto cifrado e o retorna um decifrado
def decifrar(TextoCifrado):

  TextoCifrado = list(TextoCifrado)
  #Convertendo o texto cifrado para os números da cifra
  TC_numeros = [MA[i] for i in TextoCifrado]

  #Calculando o determinante da matriz da chave
  determinante = round(np.linalg.det(chave_matriz))

  #Multiplicando a matriz inversa da chave com a sua determinante
  adj_chave_matriz = np.linalg.inv(chave_matriz) * round(np.linalg.det(chave_matriz)) 

  #obtendo a chave inversa
  chave_inverse = (pow(determinante,-1,95) * adj_chave_matriz) % 95

  #Decriptando

  #Transformando a lista em um array para facilicar algumas operações
  TC_array = np.array(TC_numeros)

  #Dividindo o array em blocos
  TC_blocos = np.split(TC_array, len(TC_numeros)//TB)

  #Multiplicando os blocos com a chave inversa e realizando o módulo ao final para que os valorem permanecem dentro da faixa especificada
  TextoClaro_blocos = [np.matmul(TC_blocos[i], chave_inverse) % 95 for i in range(len(TextoCifrado)//TB)]

  #Concatenando os blocos em um array
  TextoClaro_array = np.concatenate(TextoClaro_blocos)

  #Essa linha é para corrigir um erro que para chaves não divisíveis por 2 o espaço era criptografado para um valor que não pertencia a cifra.
  TextoClaro_array = [0 if round(number) == 95 else number for number in TextoClaro_array]

  #Fazendo o mapeamento reverso do alfabeto para obter o texto com os símbolos na saída
  TD = [MA_rev[round(i)] for i in TextoClaro_array]

  #removendo os zeros do final que podem ter sido adicionados na correção do tamanho do texto plano
  if(len(TD) > 2):
     i = 1
     while(TD[len(TD) - i] == '0'):
        TD.pop()
           
  return(''.join(TD))

# Configurar argumentos da linha de comando
parser = argparse.ArgumentParser(description='Cifra ou decifra um arquivo de texto usando a cifra de Hill')
parser.add_argument('-enc', dest='modo', action='store_const', const='enc', help='Cifrar o arquivo de entrada')
parser.add_argument('-dec', dest='modo', action='store_const', const='dec', help='Decifrar o arquivo de entrada')
parser.add_argument('entrada', help='Arquivo de entrada (texto claro ou texto cifrado)')
parser.add_argument('-out', dest='saida', required=True, help='Arquivo de saída')

# Parse dos argumentos
args = parser.parse_args()

# Abrindo o arquivo de entrada e lendo o conteúdo
with open(args.entrada, 'r') as arquivo_entrada:
    texto = arquivo_entrada.read()

if args.modo == 'dec':
    # Decifra o texto lido
    texto_decifrado = decifrar(texto)

    # Escreve o texto decifrado no arquivo de saída
    with open(args.saida, 'w') as arquivo_saida:
        arquivo_saida.write(texto_decifrado)
else:
    # Cifra o texto lido
    texto_cifrado = cifrar(texto)

    # Escreve o texto cifrado no arquivo de saída
    with open(args.saida, 'w') as arquivo_saida:
        arquivo_saida.write(texto_cifrado)

