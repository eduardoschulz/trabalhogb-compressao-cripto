from collections import Counter
import random


def texto_para_bits(texto):
    return ''.join(format(ord(c), '08b') for c in texto)


def bits_para_texto(bits):
    resultado = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            resultado += chr(int(byte, 2))
    return resultado


def inserir_erro_manual(codigo: str) -> str:
    lista_bits = list(codigo)

    while True:
        print(f"\nCódigo atual: {''.join(lista_bits)}")
        escolha = input("Digite o índice do bit (0 até {0}) para alterar ou Enter para parar: ".format(
            len(lista_bits)-1))

        if escolha == "":
            break

        if escolha.isdigit():
            indice = int(escolha)

            if 0 <= indice < len(lista_bits):
                if lista_bits[indice] == '0':
                    lista_bits[indice] = '1'
                else:
                    lista_bits[indice] = '0'
            else:
                print("Erro: Índice fora dos limites da string de bits!")
        else:
            print("Erro: Digite um número válido!")

    return ''.join(lista_bits)


def inserir_erro_auto(codigo: str) -> str:
    lista_bits = list(codigo)
    n = random.randint(1, len(lista_bits))
    indices = random.sample(range(len(lista_bits)), n)
    for i in indices:
        lista_bits[i] = '1' if lista_bits[i] == '0' else '0'
    return ''.join(lista_bits)


def inserir_erro(codigo: str) -> str:
    print("\n--- Inserir Erro ---")
    print("1 - Não inserir erro")
    print("2 - Inserir erro automático")
    print("3 - Inserir erro manual")
    op = input("Escolha: ")

    if op == "2":
        return inserir_erro_auto(codigo)
    elif op == "3":
        return inserir_erro_manual(codigo)
    return codigo


def huffman_menu():
    """Sub-menu interativo para Huffman."""
    from main import huffman_encode, huffman_decode

    texto = input("Digite o texto a ser codificado: ")

    if not texto:
        print("Texto vazio!")
        return

    codigo, tabela, raiz = huffman_encode(texto)

    # Exibe tabela de códigos
    print("\n--- Tabela de Códigos Huffman ---")
    print(f"{'Símbolo':<10} {'Freq':<8} {'Código'}")
    freq = Counter(texto)
    for simbolo in sorted(tabela):
        exibe = repr(simbolo) if simbolo in (' ', '\t', '\n') else simbolo
        print(f"  {exibe:<8} {freq[simbolo]:<8} {tabela[simbolo]}")

    print(f"\nTexto original  : {texto}")
    print(f"Codificado      : {codigo}")
    codigo = inserir_erro(codigo)
    print(f"Novo codificado : {codigo}")

    try:
        decodificado = huffman_decode(codigo, raiz)
        print(f"Decodificado    : {decodificado}")
    except ValueError as e:
        print(f"Falha ao decodificar (árvore corrompida pelo erro): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def menu():
    while True:
        print("\n===== ESCOLHA UMA OPÇÃO =====")
        print("1 - Golomb")
        print("2 - Elias-Gamma")
        print("3 - Fibonacci")
        print("4 - Huffman")
        print("0 - Sair")

        op = input("Escolha o método: ")

        try:
            if op == '1':
                n = input("Digite a mensagem: ")
                k = int(input("Digite o número k (potência de 2): "))

                if not validar_entrada_golomb(k):
                    print("\nEntrada inválida! K deve ser uma potência de 2.")
                    continue  # Se a entrada for inválida, retorna ao menu
                print("\nEntrada válida!")

                codigo = golomb_encode(n, k)
                if codigo is not None:
                    print(f"\nResultado: {codigo}")
                codigo = inserir_erro(codigo)
                print(f"Resultado com erro: {codigo}")
                decodificado = golomb_decode(codigo, k)
                if decodificado:
                    print(f"Decodificado: {decodificado[0]}")

            elif op == '2':
                try:
                    n = int(input("Digite um número inteiro positivo: "))

                    if n <= 0:
                        print("Entrada inválida!")
                        continue

                    codigo = elias_gamma_encode(n)
                    print(f"\nCodificado (Elias-Gamma): {codigo}")

                    codigo = inserir_erro(codigo)
                    print(f"Codificado com erro: {codigo}")

                    decodificado = elias_gamma_decode(codigo)
                    if decodificado:
                        print(f"Decodificado: {decodificado[0]}")

                except Exception as e:
                    print(f"Erro na decodificação: {e}")

            elif op == '3':
                try:
                    n = int(input("Digite um número inteiro positivo: "))

                    if n <= 0:
                        print("Entrada inválida!")
                        continue

                    codigo = fibonacci_encode(n)
                    print(f"\nCodificado (Fibonacci): {codigo}")

                    codigo = inserir_erro(codigo)
                    print(f"Codificado com erro: {codigo}")

                    decodificado = fibonacci_decode(codigo)
                    if decodificado:
                        print(f"Decodificado: {decodificado[0]}")

                except Exception as e:
                    print(f"Erro na decodificação: {e}")

            elif op == '4':
                try:
                    huffman_menu()
                except Exception as e:
                    print(f"Erro: {e}")

            elif op == '0':
                break

            else:
                print("Opção inválida!")

        except Exception as e:
            print(f"Erro: {e}")
