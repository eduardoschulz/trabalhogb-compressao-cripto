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
menu()