import enum

class Instruction:
    def __init__(self, assemble, disasm):
        self.assemble = assemble
        self.disasm   = disasm

    def __str__(self):
        return f'{self.name = }, '
# opcode = (0x1000 | (addr & 0x0FFF)).to_bytes(2, 'big')
instrSet = {
    0x1000: Instruction(lambda addr: 0x1000 | (addr & 0x0FFF), 'JMP %s'),
    0x6000: Instruction(lambda Vx, Vy: 0x6000 | (Vx << 8) | ( Vy & 0x00ff), 'LD V%d V%d'),
    0xF065: Instruction(lambda Vx: 0xF065 | (Vx << 8), 'LD V%d I'),
}
addr = 0x200
jmp = instrSet[0x1000].assemble(addr)
load_Vx_I = instrSet[0xF065](1)
print(jmp, load_Vx_I)