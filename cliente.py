# Trabalho Prático 2 - Teoria da Informação: Compressão e Criptografia
# Alunos: Gabriel Cezar Walber, Renan Zampeze, Arthur Wild, Eduardo Schulz
import socket
from modulos.golomb import Golomb
from modulos.eliasgamma import EliasGamma
from modulos.fibonacci import Fibonacci
from modulos.huffman import NoHuffman
from modulos.repeticao import Repeticao
from modulos.hamming import Hamming
from modulos.utils import inserir_erro, texto_para_bits, bits_para_texto

UDP_IP = "127.0.0.1"
UDP_PORT = 5000


def enviar(sock, dados):
    """
    funcao para facilitar o sendto + print
    """
    sock.sendto(dados.encode(), (UDP_IP, UDP_PORT))
    print("Código enviado para o servidor.")


def menu():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        print("\n===== ESCOLHA UMA OPÇÃO =====")
        print("1 - Golomb")
        print("2 - Elias-Gamma")
        print("3 - Fibonacci")
        print("4 - Huffman")
        print("5 - Código de Repetição Ri")
        print("6 - Hamming (7,4)")
        print("0 - Sair")

        op = input("Escolha o método: ")

        try:
            if op == '1':
                n = input("Digite a mensagem: ")
                k = int(input("Digite o número k (potência de 2): "))

                if not Golomb.validar_entrada_golomb(k):
                    print("\nEntrada inválida! K deve ser uma potência de 2.")
                    continue

                codigo = Golomb.golomb_encode(n, k)
                print(f"\nResultado: {codigo}")
                codigo = inserir_erro(codigo)
                print(f"Resultado com erro: {codigo}")
                # manda o tipo de encoding ex. golomb: mensagem_encodada
                enviar(sock, f"golomb:{k}:{codigo}")

            elif op == '2':
                n = input("Digite a mensagem: ")
                codigo = EliasGamma.elias_gamma_encode(n)
                print(f"\nCodificado (Elias-Gamma): {codigo}")
                codigo = inserir_erro(codigo)
                print(f"Codificado com erro: {codigo}")
                enviar(sock, f"eliasgamma:{codigo}")

            elif op == '3':
                n = input("Digite a mensagem: ")
                codigo = Fibonacci.fibonacci_encode(n)
                print(f"\nCodificado (Fibonacci): {codigo}")
                codigo = inserir_erro(codigo)
                print(f"Codificado com erro: {codigo}")
                enviar(sock, f"fibonacci:{codigo}")

            elif op == '4':
                n = input("Digite a mensagem: ")
                h = NoHuffman(None, 0)
                codigo, tabela, raiz = h.huffman_encode(n)
                print(f"\nCodificado (Huffman): {codigo}")
                codigo = inserir_erro(codigo)
                print(f"Codificado com erro: {codigo}")
                dump = str({s: c for s, c in tabela.items()})
                enviar(sock, f"huffman:{dump}|{codigo}")

            elif op == '5':
                texto = input("Digite o texto:\n")
                r = int(input("Digite o valor de R (ímpar): "))

                if not Repeticao.validar_repeticao(r):
                    print("R deve ser ímpar.")
                    continue

                bits = texto_para_bits(texto)
                print(f"\nBits originais:\n{bits}")

                codigo = Repeticao.repeticao_encode(bits, r)
                print(f"\nCodificado:\n{codigo}")

                codigo = inserir_erro(codigo)
                print(f"\nCom erro:\n{codigo}")

                enviar(sock, f"repeticao:{r}:{codigo}")

            elif op == '6':
                texto = input("Digite o texto:\n")

                bits = texto_para_bits(texto)
                print(f"\nBits originais:\n{bits}")

                codigo = Hamming.hamming74_encode(bits)
                print(f"\nCodificado Hamming:\n{codigo}")

                codigo = inserir_erro(codigo)
                print(f"\nCom erro:\n{codigo}")

                enviar(sock, f"hamming:{codigo}")

            elif op == '0':
                break

            else:
                print("Opção inválida!")

        except Exception as e:
            print(f"Erro: {e}")

    sock.close()


menu()
