def encode(string: str, **kwargs) -> str:
    sep = kwargs["sep"]
    return "".join([f"{sep}{format(ord(_), 'x'):>02}" for _ in string])


def decode(string:str, **kwargs) -> str:
    return decode_hex(string.replace(kwargs["sep"], ""))


def decode_hex(encoded):
    decoded = ""
    for index in range(0, len(encoded), 2):
        decoded += chr(int(encoded[index:index+2], 16))
    return decoded