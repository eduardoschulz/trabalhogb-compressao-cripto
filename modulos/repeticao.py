class Repeticao:
    def __init__(self):
        pass

    @staticmethod
    def validar_repeticao(r):
        return r > 0 and r % 2 == 1

    @staticmethod
    def repeticao_encode(bits, r):
        resultado = ""
        for bit in bits:
            resultado += bit * r
        return resultado

    @staticmethod
    def repeticao_decode(codigo, r):
        resultado = ""
        for i in range(0, len(codigo), r):
            bloco = codigo[i:i+r]
            zeros = bloco.count('0')
            uns = bloco.count('1')
            resultado += '1' if uns > zeros else '0'
        return resultado
