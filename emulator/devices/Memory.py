import sys

class Memory:
    def __init__(self, size):
        self.buffer = [0] * size
        self.size   = size - 1

    def read(self, addr: int) -> int:
        assert 0 <= addr <= self.size
        return self.buffer[addr]

    def write(self, addr: int, value: int) -> None:
        assert isinstance(value, int)
        assert 0 <= value <= 0xff
        self.buffer[ addr ] = value & 0xff
    
    def clear(self) -> None:
        self.buffer = [0] * (self.size + 1)

    def dump(self, _from: int = 0, _to: int = -1, step: int = 2) -> None:
        if _to == -1: _to = self.size
        for addr in range(_from, _to, step):
            string = f'0x{addr:<4x}|'
            for i in range(0, step):
                if (addr + i) > self.size:
                    break
                string += f' {self.buffer[addr + i]:<02x}'
            print(string)

    def __repr__(self):
        return self.dump(0, self.size, 10)

if __name__ == '__main__':
    mem = Memory(0x1000)
    mem.write(0xfff, 255)
    mem.dump(step=16)
    sys.exit(0)
