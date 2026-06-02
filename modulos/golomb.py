# Setup para tudo relacionado a Golomb
import math


class Golomb:
    def __init__(self):
        return self

    # Validar se entrada é compatível para Golomb
    @staticmethod
    def validar_entrada_golomb(k):
        return k == 2**(int(math.log2(k)))

    @staticmethod
    def golomb_encode(mensagem, divisor):  # Codificação Golomb
        output = ''
        for c in mensagem:
            dividendo = ord(c)
            quociente = dividendo // divisor  # Calcular quociente
            resto = dividendo % divisor  # Calcular resto

            prefixo = '0' * quociente + '1'  # Gerar prefixo

        # Calcular número de bits necessários para representar o sufixo
            k = math.ceil(math.log2(divisor))
        # Calcular o limiar para determinar o sufixo
            threshold = (2 ** k) - divisor

            if resto < threshold:  # Determinar sufixo com base no limiar
                sufixo = format(resto, f'0{k-1}b')  # Gerar sufixo
            else:
                resto += threshold  # Ajustar o resto para o caso em que ele é maior ou igual ao limiar
                sufixo = format(resto, f'0{k}b')  # Gerar sufixo
            output += prefixo + sufixo
        return output

    @staticmethod
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
