import math


class EliasGamma:
    def __init__(self):
        return self

    @staticmethod
    def elias_gamma_encode(text):
        bits = []
        for ch in text:
            n = ord(ch)
            k = int(math.log2(n))
            bits.append('0' * k + format(n, f'0{k+1}b'))
        return ''.join(bits)


    @staticmethod
    def elias_gamma_decode(code):
        chars = []
        i = 0
        while i < len(code):
            k = 0
            while i < len(code) and code[i] == '0':
                k += 1
                i += 1
 
            if i + k >= len(code):
                break
 
            chars.append(chr(int(code[i:i + k + 1], 2)))
            i += k + 1
 
        return ''.join(chars)
