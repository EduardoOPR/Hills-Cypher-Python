# Hills-Cypher-Python
Cifra de Hills implementada utilizando a linguagem Python

 - Para cifrar um documento de texto basta executar o comando: python cifrahill.py -enc textoclaro.txt -out textocifrado.txt
  Para isso tem que ter o python e a biblioteca do numpy instalados
  O documento de texto para esse caso tem que ter o nome textoclaro, ou pelo menos tem que ser o mesmo do arquivo de texto que estiver no mesmo local do programa
  A cifra não está funcionando para caracteres com acentos

 - Para deficfrar execute o comando: python cifrahill.py -dec textocifrado.txt -out textoclaro.txt
  o arquivo tem que estar com o nome textocifrado (também pode alterar o o nome do arquivo no comando que vai na linha de comando se preferir)

 Para alterar a chave basta mudar o valor da variável chave, porém seu tamanho tem que ser um quadrado perfeito
