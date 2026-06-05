from modulos.hamming import Hamming
from modulos.repeticao import Repeticao
import zlib


def aplicar_correcao(bits: str, metodo: str, param: int = 0) -> str:
    if metodo == "hamming":
        return Hamming.hamming74_encode(bits)
    if metodo == "repeticao":
        return Repeticao.repeticao_encode(bits, param)
    return bits


def remover_correcao(bits: str, metodo: str, param: int = 0) -> str:
    if metodo == "hamming":
        return Hamming.hamming74_decode(bits)
    if metodo == "repeticao":
        return Repeticao.repeticao_decode(bits, param)
    return bits


def calc_crc(bits: str) -> int:
    return zlib.crc32(bits.encode()) & 0xFFFFFFFF


def check_crc(bits: str, crc: int) -> bool:
    return calc_crc(bits) == crc
