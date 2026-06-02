
class Fibonacci:
    def __init__(self):
        return self

    @staticmethod
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

    @staticmethod
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
