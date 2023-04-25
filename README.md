# binmagic: Convert Binary to MSX Basic

**binmagic** is a Python script that converts a binary to an MSX BASIC program.

The binary is fully embedded into the DATA section of the self-contained program. When executed, the program loads the binary into the specified address and passes the control to it.

## Usage

```
./binmagic <infile> <outfile> <addr>
```

`<infile>` - Input binary file to be converted
`<outfile>` - The output BASIC file in text format
`<address>` - The memory address (in HEX) the code is expected to be loaded to and executed from.

### Sample Usage

```
./binmagic.py scr1bold.bin scr1bold C000
```

## Sample Output

```
10 DATA"3E0132AFFCDD215F00FD2AC0FCCD1C00F3010008210000CD2DC0DB9857CB0AB2CD34
20 DATA"C0D398230B78B120ECFBC97DD3997CD399C9F57DD3997CF640D399F1C9
30 D=&HC000:FOR A=1 TO 2:READ L$:B=1
40 IF B<LEN(L$) THEN POKE D,VAL("&H"+MID$(L$,B,2)):D=D+1:B=B+2:GOTO 40
50 NEXT A
60 DEF USR=&HC000:A=USR(0)
```



