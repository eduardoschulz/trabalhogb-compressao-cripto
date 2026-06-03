
class Fibonacci:
    def __init__(self):
        return self

    @staticmethod
    def fibonacci_encode(text):
        bits = []
        for ch in text:
            n = ord(ch)
 
            fib = [1, 2]
            while fib[-1] <= n:
                fib.append(fib[-1] + fib[-2])
            fib = fib[:-1]
 
            code = []
            for f in reversed(fib):
                if f <= n:
                    code.append('1')
                    n -= f
                else:
                    code.append('0')
 
            code.reverse()
            bits.append(''.join(code) + '1')
 
        return ''.join(bits)


    @staticmethod
    def fibonacci_decode(code):
        fib = [1, 2]
        chars = []
        current = []
 
        i = 0
        while i < len(code):
            current.append(code[i])
 
            if len(current) >= 2 and current[-1] == '1' and current[-2] == '1':
                current = current[:-1]
 
                while len(fib) < len(current):
                    fib.append(fib[-1] + fib[-2])
 
                num = sum(fib[j] for j, b in enumerate(current) if b == '1')
                chars.append(chr(num))
                current = []
 
            i += 1
 
        return ''.join(chars)
