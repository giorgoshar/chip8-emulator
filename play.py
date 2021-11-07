import os
import sys


class Registers:
    def __init__(self):
        self.regs = [0 for i in range(16)]

regs = [0 for i in range(16)]

def load_Vx_kk(x, kk):
    regs[x] = kk
def load_Vx_Vy(x, y):
    regs[x] = regs[y]
def subn_Vx_Vy(x, y):
    regs[0xf] = 1 if (regs[y] > regs[x]) else 0
    regs[x]   = (regs[y] - regs[x]) & 0xff
def add_Vx_kk(x, kk):
    regs[x] += kk
def sne_Vx_kk(x, kk):
    if regs[x] != kk:
        return True
    return False
def lo_shr(x, y):
    regs[0xf] = regs[x] & 0x1
    regs[x]   = (regs[x] >> 1) & 0xff
def lo_shl(x, y):
    regs[0xf] = regs[x] >> 7
    regs[x]   = (regs[x] << 1) & 0xff


os.system("cls")
load_Vx_kk(0x0, 0)
load_Vx_kk(0x1, 5)

for _ in range(0, 10):

    load_Vx_Vy(0x2, 0x0)
    subn_Vx_Vy(0x2, 0x1)

    print(regs, end=' | ')
    if(sne_Vx_kk(0xf, 0x0)):
        print('SKIP', end = '')
    print()
    
    add_Vx_kk(0x0,  1)

print('----------- FINISH -----------')
print(regs)