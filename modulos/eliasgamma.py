import math


class EliasGamma:
    def __init__(self):
        return self

    @staticmethod
    def elias_gamma_encode(mensagem):
        resultado = ""
        for c in mensagem:
            n = ord(c)
            k = int(math.log2(n))
            prefixo = '0' * k
            sufixo = format(n, f'0{k+1}b')
            resultado += prefixo + sufixo
        return resultado


    @staticmethod
    def elias_gamma_decode(code):
        resultado = ""
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
            resultado += chr(int(bits, 2))
    
        return resultado
