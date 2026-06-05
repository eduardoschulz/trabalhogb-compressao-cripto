class Fibonacci:
    def __init__(self):
        pass

    @staticmethod
    def fibonacci_encode(mensagem):
        resultado = ""
        for c in mensagem:
            n = ord(c)
            code = ""

            # Monta código (Zeckendorf)
            fib = [1, 2]
            pos = 1
            while fib[pos] <= n:
                pos += 1
                fib.append(fib[pos-2] + fib[pos-1])
            while pos > 0:
                pos -= 1
                if n >= fib[pos]:
                    n -= fib[pos]
                    code = '1' + code
                else:
                    code = '0' + code

            code += '1'  # vira "11" no final
            resultado += code
        return resultado


    @staticmethod
    def fibonacci_decode(code):
        result = ""
        fib = [1, 2]
        pos = 0
        f = 0
        num = 0
        while pos < len(code):
            if code[pos] == '1':
                while len(fib)-1 < f:
                    fib.append(fib[-2] + fib[-1])
                num += fib[f]
                pos += 1
                f += 1
                if pos < len(code) and code[pos] == '1':
                    result += chr(num)
                    num = 0
                    f = -1
            pos += 1
            f += 1
        return result
