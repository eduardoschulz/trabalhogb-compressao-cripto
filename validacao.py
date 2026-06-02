from modulos.golomb import Golomb
from modulos.fibonacci import Fibonacci
from modulos.eliasgamma  import EliasGamma
from modulos.huffman import NoHuffman
import modulos.utils as utils

mensagem = "Teste para validação de codificações"

encode = Golomb.golomb_encode(mensagem, 64)
print("Golomb:", encode)
decode = Golomb.golomb_decode(encode, 64)
print("Golomb Decodificado:", decode)