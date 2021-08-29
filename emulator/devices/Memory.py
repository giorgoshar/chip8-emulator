# pylint: disable=redefined-outer-name
import sys

class Memory:
    def __init__(self, size):
        self.buffer = [0] * size
        self.size   = size - 1

    def read(self, addr):
        return self.buffer[addr]

    def read_n(self, addr, n=1):
        buff = []
        for i in range(0, n):
            buff.append(self.buffer[addr + i] & 0xff)
        return buff

    def write(self, addr, value):
        if isinstance(value, int):
            if value <= 0xff:
                self.buffer[ addr ] = value & 0xff
        if isinstance(value, list):
            for index, byte in enumerate(value):
                self.buffer[addr + index] = byte & 0xff
    
    def clear(self):
        self.buffer = [0] * (self.size + 1)

    def dump(self, fromLine=0, toLine=-1, stepByte=2):
        string = ''
        
        if toLine == -1:
            toLine = self.size

        for addr in range(fromLine, toLine, stepByte):
            string += f'0x{addr:<4x}|'
            for i in range(0, stepByte):
                if (addr + i) > self.size:
                    break
                string += f' {self.buffer[addr + i]:<02x}'
            string += '\n'
        print(string)

    def __repr__(self):
        return self.dump(0, self.size, 10)

if __name__ == '__main__':
    mem = Memory(0x1000)

    mem.write(0x0, [0x4, 0x41])
    assert mem.read_n(0x0, 2) == [ 0x04, 0x41 ]

    mem.write(0x0, 0xff)
    mem.write(0x1, 0x00)
    assert mem.read_n(0x0, 2) == [ 0xff, 0x00 ]

    mem.write(0x200, list(range(0, 10)))
    print(mem.dump(0x200, 0x20a, 5))

    print(mem)

    sys.exit(0)
