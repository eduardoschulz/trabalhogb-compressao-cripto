# Trabalho Prático 1 - Teoria da Informação: Computação e Criptografia
# Alunos: Gabriel Cezar Walber, Renan Zampeze, Arthur Wild, Eduardo Schulz
import math
import heapq
from collections import Counter

def validar_entrada_golomb(k): # Validar se entrada é compatível para Golomb
    return k == 2**(int(math.log2(k)))

def golomb_encode(mensagem, divisor): # Codificação Golomb
    output = ''
    for c in mensagem:
        dividendo = ord(c)
        quociente =  dividendo // divisor # Calcular quociente
        resto = dividendo % divisor # Calcular resto

        prefixo = '0' * quociente + '1' # Gerar prefixo

        k = math.ceil(math.log2(divisor)) # Calcular número de bits necessários para representar o sufixo
        threshold = (2 ** k) - divisor # Calcular o limiar para determinar o sufixo

        if resto < threshold: # Determinar sufixo com base no limiar
            sufixo = format(resto, f'0{k-1}b') # Gerar sufixo
        else:
            resto += threshold # Ajustar o resto para o caso em que ele é maior ou igual ao limiar
            sufixo = format(resto, f'0{k}b') # Gerar sufixo
        output += prefixo + sufixo
    return output

def golomb_decode(codigo, k):
    resultado = ""
    pos = 0
    while pos < len(codigo):
        quociente = 0
        while codigo[pos] == '0':
            quociente += 1
            pos += 1
        pos += 1
        num = 0
        for i in range(int(math.log2(k))):
            num += int(codigo[pos])
            num *= 2
            pos += 1
        num += 2**quociente
        resultado += chr(num)
    return resultado

def fibonacci_encode(n):
    if n <= 0:
        raise ValueError("Fibonacci só codifica inteiros positivos")

    fib = [1, 2]

    # Gera Fibonacci até passar de n
    while fib[-1] <= n:
        fib.append(fib[-1] + fib[-2])

    fib = fib[:-1]  # remove o maior que n

    code = []

    # Monta código (Zeckendorf)
    for f in reversed(fib):
        if f <= n:
            code.append('1')
            n -= f
        else:
            code.append('0')

    code.reverse()

    return ''.join(code) + '1'  # vira "11" no final

def fibonacci_decode(code):
    fib = [1, 2]
    result = []
    current = []

    i = 0
    while i < len(code):
        current.append(code[i])

        # Detecta "11"
        if len(current) >= 2 and current[-1] == '1' and current[-2] == '1':
            current = current[:-1]  # remove último "1"

            # Gera Fibonacci suficiente
            while len(fib) < len(current):
                fib.append(fib[-1] + fib[-2])

            num = 0
            for j in range(len(current)):
                if current[j] == '1':
                    num += fib[j]

            result.append(num)
            current = []

        i += 1

    return result

def elias_gamma_encode(n):
    if n <= 0:
        raise ValueError("Elias-Gamma só codifica inteiros positivos")
 
    k = int(math.log2(n))          # número de bits do prefixo unário
    prefixo = '0' * k              # k zeros
    sufixo = format(n, f'0{k+1}b') # representação binária de n com k+1 bits
 
    return prefixo + sufixo
 
def elias_gamma_decode(code):
    result = []
    i = 0
 
    while i < len(code):
        # Conta zeros iniciais para determinar k
        k = 0
        while i < len(code) and code[i] == '0':
            k += 1
            i += 1
 
        # Lê os próximos k+1 bits como o valor
        if i + k >= len(code):
            break  # bits insuficientes para completar o código
 
        bits = code[i:i + k + 1]
        i += k + 1
        result.append(int(bits, 2))
 
    return result

class NoHuffman:
    """Nó da árvore de Huffman."""
    def __init__(self, simbolo, freq):
        self.simbolo = simbolo  # caractere ou None (nó interno)
        self.freq    = freq     # frequência acumulada
        self.esq     = None     # filho esquerdo  → bit 0
        self.dir     = None     # filho direito   → bit 1
 
    # heapq compara por (freq, desempate) — usamos o símbolo como desempate
    def __lt__(self, outro):
        if self.freq != outro.freq:
            return self.freq < outro.freq
        # Desempate: folhas antes de nós internos; depois ordem alfabética
        s1 = self.simbolo  if self.simbolo  is not None else '\xff'
        s2 = outro.simbolo if outro.simbolo is not None else '\xff'
        return s1 < s2
 
 
def huffman_build_tree(texto):
    """Constrói a árvore de Huffman a partir de uma string e retorna a raiz."""
    if not texto:
        raise ValueError("Texto vazio!")
 
    freq = Counter(texto)
 
    # Caso especial: apenas um símbolo distinto
    if len(freq) == 1:
        simbolo, f = next(iter(freq.items()))
        raiz = NoHuffman(None, f)
        raiz.esq = NoHuffman(simbolo, f)
        return raiz
 
    # Monta heap mínimo
    heap = [NoHuffman(s, f) for s, f in freq.items()]
    heapq.heapify(heap)
 
    while len(heap) > 1:
        esq = heapq.heappop(heap)
        dir = heapq.heappop(heap)
        interno = NoHuffman(None, esq.freq + dir.freq)
        interno.esq = esq
        interno.dir = dir
        heapq.heappush(heap, interno)
 
    return heap[0]  # raiz
 
 
def huffman_build_codes(no, prefixo='', tabela=None):
    """Percorre a árvore recursivamente e preenche a tabela símbolo → código."""
    if tabela is None:
        tabela = {}
 
    if no is None:
        return tabela
 
    if no.simbolo is not None:          # folha
        tabela[no.simbolo] = prefixo if prefixo else '0'
        return tabela
 
    huffman_build_codes(no.esq, prefixo + '0', tabela)
    huffman_build_codes(no.dir, prefixo + '1', tabela)
    return tabela
 
 
def huffman_encode(texto):
    """
    Codifica 'texto' com Huffman.
    Retorna (codigo_binario: str, tabela: dict, raiz: NoHuffman).
    """
    raiz   = huffman_build_tree(texto)
    tabela = huffman_build_codes(raiz)
    codigo = ''.join(tabela[c] for c in texto)
    return codigo, tabela, raiz
 
 
def huffman_decode(codigo, raiz):
    """Decodifica uma string de bits usando a árvore de Huffman."""
    resultado = []
    no_atual  = raiz
 
    for bit in codigo:
        no_atual = no_atual.esq if bit == '0' else no_atual.dir
 
        if no_atual is None:
            raise ValueError("Código inválido — bit inesperado na sequência.")
 
        if no_atual.simbolo is not None:   # chegou numa folha
            resultado.append(no_atual.simbolo)
            no_atual = raiz                # volta à raiz
 
    return ''.join(resultado)
 

def huffman_menu():
    """Sub-menu interativo para Huffman."""
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
 
    # O try/except é importante aqui porque um erro no bit pode 
    # fazer o huffman_decode não encontrar a folha da árvore
    try:
        decodificado = huffman_decode(codigo, raiz)
        print(f"Decodificado    : {decodificado}")
    except ValueError as e:
        print(f"Falha ao decodificar (árvore corrompida pelo erro): {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

"""
transforma uma string encodede em array de bits; usa o input do usuario para flippar os bits conforme
o index recebido
"""
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

def repeticao_encode(bits, r): # Codificação código de repetição Ri
    resultado = ""

    for bit in bits:
        resultado += bit * r # Repete cada bit R vezes

    return resultado

def repeticao_decode(codigo, r): # Decodificação código de repetição Ri
    resultado = ""

    print("\nDecodificação bloco a bloco:")

    for i in range(0, len(codigo), r): # Itera sobre a string de bits em blocos de R
        bloco = codigo[i:i+r] # Extrai o bloco de R bits

        zeros = bloco.count('0')
        uns = bloco.count('1')

        if uns > zeros: # Determina o valor do bit decodificado com base na maioria dos bits no bloco
            bit = '1'
            resultado += '1'
        else:
            bit = '0'
            resultado += '0'

        if i + r < len(codigo):
            print(f"{bloco} -> {bit}", end=" / ")
        else:
            print(f"{bloco} -> {bit}")

    return resultado

def validar_repeticao(r): # Valida se R é ímpar
    return r > 0 and r % 2 == 1

def texto_para_bits(texto): # Converte a entrada para bits, representando cada caractere como um byte de 8 bits
    return ''.join(format(ord(c), '08b') for c in texto) # Converte cada caractere para ASCII com uma representação de 8 bits, após junta todos em uma única string

def bits_para_texto(bits): # Converte os bits de volta para texto, agrupando em bytes de 8 bits e convertendo cada byte para um caractere
    resultado = ""

    for i in range(0, len(bits), 8): # Itera sobre a string de bits em passos de 8
        byte = bits[i:i+8] # Agrupa os bits em bytes de 8 bits

        if len(byte) == 8: # Verifica se o byte tem 8 bits completos
            resultado += chr(int(byte, 2)) # Converte o byte para char e adiciona ao resultado

    return resultado

def hamming74_encode(bits):
    resultado = ""

    while len(bits) % 4 != 0: # Preenche com zeros à direita para garantir que o número de bits seja múltiplo de 4
        bits += '0'

    for i in range(0, len(bits), 4):

        d1, d2, d3, d4 = map(int, bits[i:i+4])

        # Calcula os bits de paridade usando XOR
        p1 = d1 ^ d2 ^ d3
        p2 = d2 ^ d3 ^ d4 
        p3 = d1 ^ d3 ^ d4

        bloco = (
            str(d1) +
            str(d2) +
            str(d3) +
            str(d4) +
            str(p1) +
            str(p2) +
            str(p3)
        )

        print(f"\nBloco de dados: {d1}{d2}{d3}{d4} -> Paridades: {p1}{p2}{p3} -> Bloco codificado: {bloco}")
        resultado += bloco

    return resultado

def hamming74_decode(codigo):

    dados = ""
    posicoes_erro = []

    # Tabela para identificar a posição do bit com erro
    tabela_erros = {
        (1,0,1): (0, "D1"),
        (1,1,0): (1, "D2"),
        (1,1,1): (2, "D3"),
        (0,1,1): (3, "D4"),
        (1,0,0): (4, "P1"),
        (0,1,0): (5, "P2"),
        (0,0,1): (6, "P3")
    }

    for i in range(0, len(codigo), 7):

        bloco = list(codigo[i:i+7]) # Extrai um bloco de 7 bits (4 dados + 3 paridade)

        if len(bloco) < 7:
            break

        d1 = int(bloco[0])
        d2 = int(bloco[1])
        d3 = int(bloco[2])
        d4 = int(bloco[3])
        p1 = int(bloco[4])
        p2 = int(bloco[5])
        p3 = int(bloco[6])

        # Calculo para detecção de erros usando XOR
        s1 = p1 ^ d1 ^ d2 ^ d3
        s2 = p2 ^ d2 ^ d3 ^ d4
        s3 = p3 ^ d1 ^ d3 ^ d4

        verificacao = (s1, s2, s3) # Se for (0,0,0), não há erro. Caso contrário, indica a posição do bit com erro.

        if verificacao != (0,0,0): # Se houver erro, corrige o bit identificado usando a tabela de erros

            indice, nome_bit = tabela_erros[verificacao]

            bloco[indice] = ( # Correção do bit com erro, flipando o bit identificado
                '1'
                if bloco[indice] == '0'
                else '0'
            )

            posicoes_erro.append(i + indice) # Posição do bit corrigido

            print(f"Erro detectado no bloco {i//7 + 1}, {nome_bit}") # Exibe o bloco e o bit onde o erro foi detectado

        dados += (
            bloco[0] +
            bloco[1] +
            bloco[2] +
            bloco[3]
        )

    return dados, posicoes_erro

def menu():
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
                n = input("Digite o texto a ser codificado:\n")
                k = int(input("Digite o número k (potência de 2): "))

                if not validar_entrada_golomb(k):
                    print("\nEntrada inválida: K deve ser uma potência de 2.")
                    continue  # Se a entrada for inválida, retorna ao menu
                print("\nEntrada válida!")

                codigo = golomb_encode(n, k)
                if codigo is not None:
                    print(f"\nResultado:\n{codigo}")
                codigo = inserir_erro(codigo)
                print(f"Resultado com erro:\n{codigo}")
                decodificado = golomb_decode(codigo, k)
                if decodificado:
                    print(f"Decodificado:\n{decodificado}")

            elif op == '2':
                try:
                    m = input("Digite o texto a ser codificado:\n")
 
                    codigo = elias_gamma_encode(m)
                    print(f"\nCodificado (Elias-Gamma):\n{codigo}")
 
                    codigo = inserir_erro(codigo)
                    print(f"Codificado com erro:\n{codigo}")

                    decodificado = elias_gamma_decode(codigo)
                    if decodificado:
                        print(f"Decodificado:\n{decodificado}")

                except Exception as e:
                    print(f"Erro na decodificação:\n{e}")

            elif op == '3':
                try:
                    m = input("Digite o texto a ser codificado:\n")

                    codigo = fibonacci_encode(m)
                    print(f"\nCodificado (Fibonacci):\n{codigo}")

                    codigo = inserir_erro(codigo)
                    print(f"Codificado com erro:\n{codigo}")

                    decodificado = fibonacci_decode(codigo)
                    if decodificado:
                        print(f"Decodificado:\n{decodificado}")

                except Exception as e:
                    print(f"Erro na decodificação:\n{e}")


            elif op == '4':
                try:
                    huffman_menu()
                except Exception as e:
                    print(f"Erro:\n{e}")

            elif op == '5':

                texto = input("Digite o texto:\n")

                r = int(input("Digite o valor de R (ímpar): "))

                if not validar_repeticao(r): # Validar se R é ímpar
                    print("R deve ser ímpar.")
                    continue

                bits = texto_para_bits(texto)
                print(f"\nBits originais:\n{bits}")

                codigo = repeticao_encode(bits, r)
                print(f"\nCodificado:\n{codigo}")

                codigo = inserir_erro(codigo)
                print(f"\nCom erro:\n{codigo}")

                corrigido = repeticao_decode(codigo, r)
                print(f"\nBits corrigidos:\n{corrigido}")

                mensagem = bits_para_texto(corrigido)
                print(f"\nMensagem recuperada:\n{mensagem}")

            elif op == '6':

                texto = input("Digite o texto:\n")

                bits = texto_para_bits(texto)
                print(f"\nBits originais:\n{bits}")

                codigo = hamming74_encode(bits)
                print(f"\nCodificado Hamming:\n{codigo}")

                codigo = inserir_erro(codigo)
                print(f"\nCom erro:\n{codigo}")

                corrigido, erros = hamming74_decode(codigo)
                print(f"\nBits corrigidos:\n{corrigido}")

                if erros:
                    print(f"Posições corrigidas: {erros}")
                else:
                    print("Nenhum erro detectado.")

                mensagem = bits_para_texto(corrigido)
                print(f"\nMensagem recuperada:\n{mensagem}")

            elif op == '0':
                break

            else:
                print("Opção inválida!")

        except Exception as e:
            print(f"Erro:\n{e}")
menu()
