import os
import sys


mem   = [ 0x0 for i in range (0, 0xFFFF) ]
regs  = [0 for i in range(16)]
pc    = 0

def load_Vx_kk(x, kk):
    regs[x] = kk
def load_Vx_Vy(x, y):
    regs[x] = regs[y]
def add_Vx_kk(x, kk):
    regs[x] += kk
def sne_Vx_kk(x, kk):
    if regs[x] != kk:
        return True
    return False
def se_Vx_Vy(x, y):
    return True if regs[x] == regs[y] else False
def se_Vx_kk(x, kk):
    return True if regs[x] == kk else False
def subn_Vx_Vy(x, y):
    regs[x]   = (regs[y] - regs[x]) & 0xff
    regs[0xf] = 1 if (regs[y] > regs[x]) else 0
def lo_sub(x, y):
    regs[x]   = (regs[x] - regs[y]) & 0xff
    regs[0xf] = 1 if (regs[x] > regs[y]) else 0
def lo_shr(x, y):
    regs[0xf] = regs[x] & 0x1
    regs[x]   = (regs[x] >> 1) & 0xff
def lo_shl(x, y):
    regs[0xf] = regs[x] >> 7
    regs[x]   = (regs[x] << 1) & 0xff

# print("('----------- BEGIN (REG1 < REG2) -----------")
# load_Vx_kk(0x0, 0)
# load_Vx_kk(0x1, 5)
# for _ in range(0, 20):
#     load_Vx_Vy(0xf, 0x1)
#     subn_Vx_Vy(0xf, 0x0)
#     print(regs, end=' | ')
#     if not sne_Vx_kk(0xf, 0x0):
#         print('False', end='')
#         add_Vx_kk(0x0,  1)
#     else:
#         load_Vx_kk(0x0, 0)
#     print()
# print('----------- END (REG1 < REG2) -----------')



# regs = [0 for i in range(16)]
# print("('----------- BEGIN (REG1 > REG2) -----------")

load_Vx_kk(0x5, 0)
load_Vx_kk(0x6, 4)



for i in range(0, 10):
    print(regs)

    load_Vx_Vy(0xf, 0x6)
    subn_Vx_Vy(0xf, 0x5)
    sne_Vx_kk(0xf, 0x0)

    add_Vx_kk(0x5, 1)
    
