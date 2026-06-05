class Cabecalho:
    # pacote = "tipo_decode\x00tipo_crc\x00param_crc\x00codigo_crc"
    # Ex: "golomb\x00repeticao\x003\x004:101010"
    # Ex: "huffman\x00none\x00\x00{'a':'0'}|10110"
    # Ex: "fibonacci\x00hamming\x00\x0010110"
    def __init__(self):
        self.tipo_decode: str = ""
        self.tipo_crc: str = "none"
        self.param_crc: str = ""
        self.codigo_crc: str = ""
        self.mensagem: str = ""
 
    def empacotar(self):
        return f"{self.tipo_decode}\x00{self.tipo_crc}\x00{self.param_crc}\x00{self.codigo_crc}"
 
    def desempacotar(self, pacote: str):
        self.tipo_decode, self.tipo_crc, self.param_crc, self.codigo_crc = pacote.split("\x00", 3)
 