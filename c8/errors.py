
class ParseError(Exception):
    def __init__(self, message :str):
        Exception.__init__(self, f"\033[1;31m{message}\033[0m")
        raise self
class Unimplemented(ParseError): pass
class Unreachable(ParseError): pass
