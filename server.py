# Trabalho Prático 2 - Teoria da Informação: Computação e Criptografia
# Alunos: Gabriel Cezar Walber, Renan Zampeze, Arthur Wild, Eduardo Schulz
import socket
import ast
from modulos.golomb import Golomb
from modulos.eliasgamma import EliasGamma
from modulos.fibonacci import Fibonacci


UDP_IP = "127.0.0.1"
UDP_PORT = 5000


def huffman_decode_from_table(codigo, tabela):
    reversa = {v: k for k, v in tabela.items()}
    resultado = []
    temp = ""
    for bit in codigo:
        temp += bit
        if temp in reversa:
            resultado.append(reversa[temp])
            temp = ""
    return "".join(resultado)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Servidor ouvindo em {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(4096)
    msg = data.decode()
    print(f"\nMensagem recebida de {addr}")

    if msg.startswith("golomb:"):
        _, k_str, codigo = msg.split(":", 2)
        k = int(k_str)
        decodificado = Golomb.golomb_decode(codigo, k)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif msg.startswith("eliasgamma:"):
        codigo = msg.split(":", 1)[1]
        decodificado = EliasGamma.elias_gamma_decode(codigo)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif msg.startswith("fibonacci:"):
        codigo = msg.split(":", 1)[1]
        decodificado = Fibonacci.fibonacci_decode(codigo)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif msg.startswith("huffman:"):
        payload = msg.split(":", 1)[1]
        dump, codigo = payload.split("|", 1)
        tabela = ast.literal_eval(dump)
        decodificado = huffman_decode_from_table(codigo, tabela)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    else:
        print(f"Formato desconhecido: {msg}")
