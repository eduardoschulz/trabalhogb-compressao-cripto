# Trabalho Prático 2 - Teoria da Informação: Compressão e Criptografia
# Alunos: Gabriel Cezar Walber, Renan Zampeze, Arthur Wild, Eduardo Schulz
import socket
import ast
from modulos.golomb import Golomb
from modulos.eliasgamma import EliasGamma
from modulos.fibonacci import Fibonacci
from modulos.repeticao import Repeticao
from modulos.hamming import Hamming
from modulos.utils import bits_para_texto
from modulos.cabecalho import Cabecalho


def decodificar_crc(bits, tipo_crc, param_crc):
    if tipo_crc == "repeticao":
        r = int(param_crc)
        resultado = Repeticao.repeticao_decode(bits, r)
        erros = sum(1 for i in range(0, len(bits), r)
                    if '0' in bits[i:i+r] and '1' in bits[i:i+r])
        if erros:
            print(f"  -> Erros detectados e corrigidos em {erros} bloco(s) (Repetição r={r})")
        else:
            print(f"  -> Nenhum erro detectado (Repetição r={r})")
        return resultado

    if tipo_crc == "hamming":
        resultado = Hamming.hamming74_decode(bits)
        # verifica se havia erro re-encodando e comparando
        recod = Hamming.hamming74_encode(resultado)
        if recod != bits:
            print("  -> Erros detectados e corrigidos (Hamming)")
        else:
            print("  -> Nenhum erro detectado (Hamming)")
        return resultado

    print("  -> CRC não aplicado")
    return bits


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

    cab = Cabecalho()
    cab.desempacotar(msg)

    if cab.tipo_decode == "golomb":
        k_str, codigo = cab.codigo_crc.split(":", 1)
        k = int(k_str)
        codigo = decodificar_crc(codigo, cab.tipo_crc, cab.param_crc)
        decodificado = Golomb.golomb_decode(codigo, k)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif cab.tipo_decode == "eliasgamma":
        codigo = decodificar_crc(cab.codigo_crc, cab.tipo_crc, cab.param_crc)
        decodificado = EliasGamma.elias_gamma_decode(codigo)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif cab.tipo_decode == "fibonacci":
        codigo = decodificar_crc(cab.codigo_crc, cab.tipo_crc, cab.param_crc)
        decodificado = Fibonacci.fibonacci_decode(codigo)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif cab.tipo_decode == "huffman":
        dump, codigo = cab.codigo_crc.split("|", 1)
        tabela = ast.literal_eval(dump)
        codigo = decodificar_crc(codigo, cab.tipo_crc, cab.param_crc)
        decodificado = huffman_decode_from_table(codigo, tabela)
        print(f"Codificado : {codigo}")
        print(f"Decodificado: {decodificado}")

    elif cab.tipo_decode == "repeticao":
        r_str, codigo = cab.codigo_crc.split(":", 1)
        r = int(r_str)
        bits = Repeticao.repeticao_decode(codigo, r)
        mensagem = bits_para_texto(bits)
        print(f"Codificado : {codigo}")
        print(f"Bits corrigidos: {bits}")
        print(f"Mensagem recuperada: {mensagem}")

    elif cab.tipo_decode == "hamming":
        bits = Hamming.hamming74_decode(cab.codigo_crc)
        mensagem = bits_para_texto(bits)
        print(f"Codificado : {cab.codigo_crc}")
        print(f"Bits corrigidos: {bits}")
        print(f"Mensagem recuperada: {mensagem}")

    else:
        print(f"Formato desconhecido: {msg}")
