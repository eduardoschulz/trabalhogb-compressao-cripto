class Cabecalho:
    # pacote = "tipo_decode|tipo_crc|param_crc|codigo_crc"
    # Ex: "golomb|repeticao|3|4:101010"
    # Ex: "huffman|none||{'a':'0'}|10110"
    # Ex: "fibonacci|hamming||10110"
    def __init__(self):
        self.tipo_decode: str = ""
        self.tipo_crc: str = "none"
        self.param_crc: str = ""
        self.codigo_crc: str = ""
        self.mensagem: str = ""

    def empacotar(self):
        return f"{self.tipo_decode}|{self.tipo_crc}|{self.param_crc}|{self.codigo_crc}"

    def desempacotar(self, pacote: str):
        self.tipo_decode, self.tipo_crc, self.param_crc, self.codigo_crc = pacote.split("|", 3)
