""" 
Classe para testar as implementações de codificação e decodificação dos algoritmos Golomb, Elias-Gamma, Fibonacci e Huffman. 
O código gera uma mensagem de teste, codifica e decodifica usando cada algoritmo, e imprime os resultados para verificação.
"""

from modulos.golomb import Golomb
from modulos.fibonacci import Fibonacci
from modulos.eliasgamma  import EliasGamma
from modulos.huffman import NoHuffman


mensagem = "Teste codificação e decodificação"

encode = Golomb.golomb_encode(mensagem, 64)
print("Golomb:", encode)
decode = Golomb.golomb_decode(encode, 64)
print("Golomb Decodificado:", decode)

print("\n")

encode = EliasGamma.elias_gamma_encode(mensagem)
print("Elias-Gamma:", encode)
decode = EliasGamma.elias_gamma_decode(encode)
print("Elias-Gamma Decodificado:", decode)

print("\n")

encode = Fibonacci.fibonacci_encode(mensagem)
print("Fibonacci:", encode)
decode = Fibonacci.fibonacci_decode(encode)
print("Fibonacci Decodificado:", decode)

print("\n")

huffman = NoHuffman(None, 0)
huffman.testar(mensagem)