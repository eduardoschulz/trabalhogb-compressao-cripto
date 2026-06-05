class Crc:
    def __init__(self):
        pass
 
    @staticmethod
    def crc_resto(bits, polinomio="10011"):
        dados = list(bits)
 
        for i in range(len(bits) - len(polinomio) + 1):
            if dados[i] == '1':
                for j in range(len(polinomio)):
                    dados[i + j] = str(int(dados[i + j]) ^ int(polinomio[j]))
 
        return ''.join(dados[-4:])
 
    @staticmethod
    def crc_encode(bits):
        polinomio = "10011"
        mensagem = bits + "0000"
        crc = Crc.crc_resto(mensagem, polinomio)
        codeword = bits + crc
 
        print(f"\nDados:\n{bits}")
        print(f"\nCRC:\n{crc}")
        print(f"\nCodeword:\n{codeword}")
 
        return codeword
 
    @staticmethod
    def crc_decode(codeword):
        polinomio = "10011"
        resto = Crc.crc_resto(codeword, polinomio)
        erro = resto != "0000"
 
        return not erro, resto
