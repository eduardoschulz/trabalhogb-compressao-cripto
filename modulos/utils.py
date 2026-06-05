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
    n = 1
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
