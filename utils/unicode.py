base = "\\u{:>04}"

def encode(string: str, **kwargs) -> str:
    buffer = ""
    try:
        for char in bytearray(string, "utf8"):
            buffer += base.format(hex(char)[2:])
    except Exception as e:
        buffer = str(e)
    
    return buffer


def decode(string: str, **kwargs) -> str:
    #string = string.encode("utf8")
    for x in string:
        print(chr(x))
    return string