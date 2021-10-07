# chip8-emulator
----------------------

A chip8 emulator in python with assembler/disassembler

```
usage:
  ./build.ps1 testcases run              : compiles and checks the recorded tests are equal to current compiled 
                        record           : recompiles the testcases for later test
              run       filename output  : compiles the assembly filename and runs it
              comp      filename output  : like run but only compiles
```

You can also run the follow python scripts
```
usage:
  ./python3 asm.py    ./filename_input.asm binary_output.o
  ./python3 chip8.py  ./binary.o
  ./python3 disasm.py ./binary.o
```
