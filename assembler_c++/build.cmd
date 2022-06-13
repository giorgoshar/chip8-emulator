echo off
rm -r .\main.exe
REM g++ main.c -L"C:\Program Files\mingw-w64\mingw64\x86_64-w64-mingw32\lib -Wall -o main
g++ main.cpp -L"C:\Program Files\mingw-w64\mingw64\x86_64-w64-mingw32\lib" -Wall -o main
.\main.exe