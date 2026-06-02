import math


class EliasGamma:
    def __init__(self):
        return self

    @staticmethod
    def elias_gamma_encode(n):
        if n <= 0:
            raise ValueError("Elias-Gamma só codifica inteiros positivos")

        k = int(math.log2(n))          # número de bits do prefixo unário
        prefixo = '0' * k              # k zeros
        # representação binária de n com k+1 bits
        sufixo = format(n, f'0{k+1}b')

        return prefixo + sufixo

    @staticmethod
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
