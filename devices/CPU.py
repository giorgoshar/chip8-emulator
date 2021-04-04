class CPU:
    def __init__(self):
        self.v      = bytearray([0] * 16)
        self.i      = 0
        self.sp     = 0
        self.pc     = 0x200

        self.stack  = [0] * 16
        self.timer = {
            'delay' : 0,
            'sound' : 0
        }
        self.cycle  = 0
        self.opcode = 0x0

    def dump(self):
        print(
            f'============[ CPU REGISTERS ]============\n'
            f'v: {[{idx: hex(b)} for idx, b in enumerate(self.v)]}\n'
            f'i: {hex(self.i)}\n'
            f'pc: {hex(self.pc)}\n'
            f'sp: {hex(self.sp)}\n'
            f'stack: {[ {idx: hex(b)} for idx, b in enumerate(self.stack)]}\n'
            f'delay: {self.timer["delay"]}\n'
            f'sound: {self.timer["sound"]}\n'
            f'============[ INSTRUCTION ]============\n'
            f'opcode   : {hex( self.opcode)}\n'
            f'operation: {hex((self.opcode & 0xf000) >> 12)}\n'
            f'x        : {hex((self.opcode & 0x0f00) >> 8)}\n'
            f'y        : {hex((self.opcode & 0x00f0) >> 4)}\n'
            f'nibble   : {hex( self.opcode & 0x000f)}\n'
            f'kk       : {hex( self.opcode & 0x00ff)}\n'
            f'nnn      : {hex( self.opcode & 0x0fff)}'
        )



    def tick(self, cycle):
        pass

