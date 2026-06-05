# Trabalho Prático 2 - Teoria da Informação: Compressão e Criptografia
# Alunos: Gabriel Cezar Walber, Renan Zampeze, Arthur Wild, Eduardo Schulz
import socket
import json
from modulos.golomb import Golomb
from modulos.eliasgamma import EliasGamma
from modulos.fibonacci import Fibonacci
from modulos.huffman import NoHuffman
from modulos.repeticao import Repeticao
from modulos.hamming import Hamming
from modulos.crc import Crc
from modulos.utils import inserir_erro, texto_para_bits
from modulos.cabecalho import Cabecalho

UDP_IP = "127.0.0.1"
UDP_PORT = 5000


def enviar(sock, dados):
    sock.sendto(dados.encode(), (UDP_IP, UDP_PORT))
    print("Código enviado para o servidor.")
    sock.settimeout(5)
    try:
        resposta, _ = sock.recvfrom(4096)
        print(f"Resposta do servidor: {resposta.decode()}")
    except socket.timeout:
        print("Sem resposta do servidor.")


def menu():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        n = input("\nDigite a mensagem (deixe vazio para sair):\n")
        if n == "":
            break

        print("\nOpções de Compressão:")
        print("1 - Golomb")
        print("2 - Elias-Gamma")
        print("3 - Fibonacci")
        print("4 - Huffman")
        print("0 - Nenhum")

        op_c = input("Escolha o método: ")

        tipo_decode = ""
        extra_c = ""
        codigo = n
        dump = ""

        try:
            if op_c == '1':
                k = int(input("Digite o número k (potência de 2): "))
                if not Golomb.validar_entrada_golomb(k):
                    print("\nEntrada inválida! K deve ser uma potência de 2.")
                    continue
                codigo = Golomb.golomb_encode(n, k)
                tipo_decode = "golomb"
                extra_c = str(k)
                print(f"\nCodificado (Golomb): {codigo}")

            elif op_c == '2':
                codigo = EliasGamma.elias_gamma_encode(n)
                tipo_decode = "eliasgamma"
                print(f"\nCodificado (Elias-Gamma): {codigo}")

            elif op_c == '3':
                codigo = Fibonacci.fibonacci_encode(n)
                tipo_decode = "fibonacci"
                print(f"\nCodificado (Fibonacci): {codigo}")

            elif op_c == '4':
                codigo, tabela, raiz = NoHuffman.huffman_encode(n)
                tipo_decode = "huffman"
                dump = json.dumps({s: c for s, c in tabela.items()})
                print(f"\nCodificado (Huffman): {codigo}")

            elif op_c == '0':
                codigo = texto_para_bits(n)

            else:
                print("Opção inválida!")
                continue

        except Exception as e:
            print(f"Erro: {e}")
            continue

        print("\nOpções de Tratamento de Erro:")
        print("1 - Código de Repetição")
        print("2 - Hamming (7,4)")
        print("3 - CRC")
        print("0 - Nenhum")

        op_te = input("Escolha o método: ")

        tipo_crc = "none"
        param_crc = ""
        tamanho_original = len(codigo)

        try:
            if op_te == '1':
                r = int(input("Digite o valor de R (ímpar): "))
                if not Repeticao.validar_repeticao(r):
                    print("R deve ser ímpar.")
                    continue
                codigo = Repeticao.repeticao_encode(codigo, r)
                if op_c == '0':
                    tipo_decode = "repeticao"
                    extra_c = str(r)
                else:
                    tipo_crc = "repeticao"
                    param_crc = str(r)
                print(f"\nCodificado (Repetição): {codigo}")

            elif op_te == '2':
                codigo = Hamming.hamming74_encode(codigo)
                if op_c == '0':
                    tipo_decode = "hamming"
                else:
                    tipo_crc = "hamming"
                    param_crc = str(tamanho_original)
                print(f"\nCodificado (Hamming): {codigo}")

            elif op_te == '3':
                codigo = Crc.crc_encode(codigo)
                tipo_crc = "crc"
                if op_c == '0':
                    tipo_decode = "crc"
                print(f"\nCodificado (CRC): {codigo}")

            elif op_te == '0':
                if op_c == '0':
                    print("Nenhuma compressão nem tratamento de erro selecionado.")
                    continue

            else:
                print("Opção inválida!")
                continue

        except Exception as e:
            print(f"Erro: {e}")
            continue

        codigo = inserir_erro(codigo)
        print(f"Codificado com erro: {codigo}")

        cab = Cabecalho()
        cab.tipo_crc = tipo_crc
        cab.param_crc = param_crc

        if tipo_decode == "golomb":
            cab.tipo_decode = "golomb"
            cab.codigo_crc = f"{extra_c}\x00{codigo}"
        elif tipo_decode == "huffman":
            cab.tipo_decode = "huffman"
            cab.codigo_crc = f"{dump}\x00{codigo}"
        elif tipo_decode == "repeticao":
            cab.tipo_decode = "repeticao"
            cab.codigo_crc = f"{extra_c}\x00{codigo}"
        elif tipo_decode == "hamming":
            cab.tipo_decode = "hamming"
            cab.codigo_crc = codigo
        else:
            cab.tipo_decode = tipo_decode
            cab.codigo_crc = codigo

        enviar(sock, cab.empacotar())

    sock.close()


menu()