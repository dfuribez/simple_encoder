import urllib.parse


def encode(string: str) -> str:
    try:
        encode = urllib.parse.quote(string)
    except Exception as e:
        encode = str(e)
    
    return encode


def decode(string: str) -> str:
    try:
        decode = urllib.parse.unquote(string)
    except Exception as e:
        decode = str(e)
    
    return decode
