class Memory:
    def __init__(self):
        self.buffer = bytearray([0] * 4096)
    def read(self, addr):
        return self.buffer[addr]
    def write(self, addr, value):
        self.buffer[addr] = value
    def dump(self):
        pass
