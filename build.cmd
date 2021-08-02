cls
rm .\test.o
py .\asm\asm.py .\test.asm
py .\emulator\chip8.py .\test.o
py .\disasm\disasm.py  .\test.o