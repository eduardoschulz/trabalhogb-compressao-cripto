class Hamming:
    def __init__(self):
        pass

    @staticmethod
    def hamming74_encode(bits):
        resultado = ""
        while len(bits) % 4 != 0:
            bits += '0'
        for i in range(0, len(bits), 4):
            d1, d2, d3, d4 = map(int, bits[i:i+4])
            p1 = d1 ^ d2 ^ d3
            p2 = d2 ^ d3 ^ d4
            p3 = d1 ^ d3 ^ d4
            bloco = (
                str(d1) + str(d2) + str(d3) + str(d4) +
                str(p1) + str(p2) + str(p3)
            )
            resultado += bloco
        return resultado

    @staticmethod
    def hamming74_decode(codigo):
        dados = ""
        tabela_erros = {
            (1,0,1): 0,
            (1,1,0): 1,
            (1,1,1): 2,
            (0,1,1): 3,
            (1,0,0): 4,
            (0,1,0): 5,
            (0,0,1): 6
        }
        for i in range(0, len(codigo), 7):
            bloco = list(codigo[i:i+7])
            if len(bloco) < 7:
                break
            d1, d2, d3, d4 = map(int, bloco[:4])
            p1, p2, p3 = map(int, bloco[4:7])
            s1 = p1 ^ d1 ^ d2 ^ d3
            s2 = p2 ^ d2 ^ d3 ^ d4
            s3 = p3 ^ d1 ^ d3 ^ d4
            if (s1, s2, s3) != (0,0,0):
                indice = tabela_erros[(s1, s2, s3)]
                bloco[indice] = '1' if bloco[indice] == '0' else '0'
            dados += ''.join(bloco[:4])
        return dados
