from collections import Counter
import heapq


class NoHuffman:
    """Nó da árvore de Huffman."""

    def __init__(self, simbolo, freq):
        self.simbolo = simbolo  # caractere ou None (nó interno)
        self.freq = freq     # frequência acumulada
        self.esq = None     # filho esquerdo  → bit 0
        self.dir = None     # filho direito   → bit 1

    # heapq compara por (freq, desempate) — usamos o símbolo como desempate
    def __lt__(self, outro):
        if self.freq != outro.freq:
            return self.freq < outro.freq
        # Desempate: folhas antes de nós internos; depois ordem alfabética
        s1 = self.simbolo if self.simbolo is not None else '\xff'
        s2 = outro.simbolo if outro.simbolo is not None else '\xff'
        return s1 < s2

    @staticmethod
    def huffman_build_tree(texto):
        """Constrói a árvore de Huffman a partir de uma string e retorna a raiz."""
        if not texto:
            raise ValueError("Texto vazio!")

        freq = Counter(texto)

        # Caso especial: apenas um símbolo distinto
        if len(freq) == 1:
            simbolo, f = next(iter(freq.items()))
            raiz = NoHuffman(None, f)
            raiz.esq = NoHuffman(simbolo, f)
            return raiz

        # Monta heap mínimo
        heap = [NoHuffman(s, f) for s, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            esq = heapq.heappop(heap)
            dir = heapq.heappop(heap)
            interno = NoHuffman(None, esq.freq + dir.freq)
            interno.esq = esq
            interno.dir = dir
            heapq.heappush(heap, interno)

        return heap[0]  # raiz

    @staticmethod
    def huffman_build_codes(no, prefixo='', tabela=None):
        """Percorre a árvore recursivamente e preenche a tabela símbolo → código."""
        if tabela is None:
            tabela = {}

        if no is None:
            return tabela

        if no.simbolo is not None:          # folha
            tabela[no.simbolo] = prefixo if prefixo else '0'
            return tabela

        NoHuffman.huffman_build_codes(no.esq, prefixo + '0', tabela)
        NoHuffman.huffman_build_codes(no.dir, prefixo + '1', tabela)
        return tabela

    def huffman_encode(self, texto):
        """
        Codifica 'texto' com Huffman.
        Retorna (codigo_binario: str, tabela: dict, raiz: NoHuffman).
        """
        raiz = self.huffman_build_tree(texto)
        tabela = self.huffman_build_codes(raiz)
        codigo = ''.join(tabela[c] for c in texto)
        return codigo, tabela, raiz

    def huffman_decode(self, codigo, raiz):
        """Decodifica uma string de bits usando a árvore de Huffman."""
        resultado = []
        no_atual = raiz

        for bit in codigo:
            no_atual = no_atual.esq if bit == '0' else no_atual.dir

            if no_atual is None:
                raise ValueError(
                    "Código inválido — bit inesperado na sequência.")

            if no_atual.simbolo is not None:   # chegou numa folha
                resultado.append(no_atual.simbolo)
                no_atual = raiz                # volta à raiz

        return ''.join(resultado)

    def testar(self, texto):
        """Codifica e decodifica uma string, printando os resultados."""
        codigo, tabela, raiz = self.huffman_encode(texto)
        print(f"Huffman Codificado: {codigo}")
        print(f"Huffman Decodificado: {self.huffman_decode(codigo, raiz)}")