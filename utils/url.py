import urllib.parse


def encode(string: str, **kwargs) -> str:
    try:
        encode = urllib.parse.quote(string, [])
        encode = encode.replace(".", "%2e")
    except Exception as e:
        encode = str(e)
    
    return encode


def decode(string: str, **kwargs) -> str:
    try:
        decode = urllib.parse.unquote(string)
    except Exception as e:
        decode = str(e)
    
    return decode
