from collections import Counter


def inserir_erro(codigo: str) -> str:
    lista_bits = list(codigo)

    while True:
        print(f"\nCódigo atual: {''.join(lista_bits)}")
        escolha = input("Digite o índice do bit (0 até {0}) para alterar ou Enter para parar: ".format(len(lista_bits)-1))

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
