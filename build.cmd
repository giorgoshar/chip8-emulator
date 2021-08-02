cls
rm .\maze.o
py .\asm\asm.py .\maze.asm
py .\emulator\chip8.py .\maze.o