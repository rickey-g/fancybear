import base64
from random import choice, randint
import struct


def random_string(length):
    import string
    # from random import choice
    chrs_set = string.letters + string.digits
    str = ''
    for i in range(0, length):
        str += choice(chrs_set)
    return str


def generate_binary_junk(length):
    # from random import randint
    bin = ''
    for i in range(0, length):
        r = randint(0, 255)
        bin += chr(r)
    return bin


def generate_int(begin, end):
    return randint(begin, end)


def xor(data, x, size=0):
    res = ''
    data_size = len(data)
    if size > 0 and size < data_size:
        data_size = size
    mask_size = len(x)
    i = 0
    while i < data_size:
        for k in range(0, mask_size):
            res += chr(ord(data[i]) ^ ord(x[k]))
            i += 1
            if not i < data_size:
                break
    return res + data[data_size:]


def unpack(data, token, b64junk_len=9, binary_junk_len=4):
    data = base64.urlsafe_b64decode(data[b64junk_len:])
    bin_junk = data[:binary_junk_len]
    data = xor(data[binary_junk_len:], bin_junk)
    _token = data[: len(token)]
    if not _token == token:
        raise XABase64Exception("Invalid token!")
    return data[len(token):]


def pack(data, token, b64junk_len=9, binary_junk_len=4):
    bin_junk = generate_binary_junk(binary_junk_len)
    data = xor(token + data, bin_junk)
    data = base64.urlsafe_b64encode(bin_junk + data)
    data = random_string(b64junk_len) + data
    return data


def unpack_xor_part(data, token, xor_part_length, b64junk_len=9, binary_junk_len=4):
    data = base64.urlsafe_b64decode(data[b64junk_len:])
    bin_junk = data[:binary_junk_len]
    data = xor(data[binary_junk_len:], bin_junk, len(token) + xor_part_length)
    _token = data[: len(token)]
    if not _token == token:
        raise XABase64Exception("Invalid token!")
    return data[len(token):]


def pack_xor_part(data, token, xor_part_length, b64junk_len=9, binary_junk_len=4):
    bin_junk = generate_binary_junk(binary_junk_len)
    data = xor(token + data, bin_junk, len(token) + xor_part_length)
    data = base64.urlsafe_b64encode(bin_junk + data)
    data = random_string(b64junk_len) + data

    return data


class XABase64Exception(BaseException):
    pass