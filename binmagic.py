#!/usr/bin/env python3

# binmagic v0.1
# Converts a binary into a self-contained BASIC program.
# Single file implementation.
#
# BSD 3-Clause License
#
# Copyright (c) 2017-2023, Vlad Shurupov
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys

class BinMagic:

    def __init__(self, infile, outfile, addr):
        self.infile = infile;
        self.outfile = outfile;
        if len(addr) > 4 or \
            not all(c in "0123456789abcdefABCDEF" for c in addr):
                print("Invalid address %s" % addr, file=sys.stderr)
                sys.exit(2)
        self.addr = addr.upper();
        self.blocks = 34;
        self.line = 0;
        self.bline = 10

    def __str__(self):
        return "[BinMagic: infile='%s', outfile='%s', addr=%s]" % (self.infile,
            self.outfile, self.addr)

    def __out(self, s="", end="\n"):
        print(s, end=end)
        self.wfile.write(s)
        self.wfile.write(end)
        if len(end) > 0:
            self.bline += 10;

    def __open_dataline(self):
        self.__out('%d DATA"' % self.bline, end="")
        self.line += 1;

    def __append_loader(self):
        self.__out("%d D=&H%s:FOR A=1 TO %d:READ L$:B=1" % (self.bline,
                self.addr, self.line))
        self.__out('%d IF B<LEN(L$) THEN POKE D,VAL("&H"+MID$(L$,B,2)):'
                'D=D+1:B=B+2:GOTO %d' % (self.bline, self.bline))
        self.__out("%d NEXT A" % self.bline)
        self.__out("%d DEF USR=&H%s:A=USR(0)" % (self.bline, self.addr))

    def run(self):
        self.wfile = open(self.outfile, "w", newline='\r\n')
        i = 0
        open_line = True
        for b in read_bytes(self.infile):
            if open_line:
                self.__open_dataline()
                open_line = False;
            self.__out("%02X" % b, end="")
            i += 1
            if i % self.blocks == 0:
                self.__out()
                open_line = True
        if not open_line:
                self.__out()
        self.__append_loader()
        self.wfile.close();


def read_bytes(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

if len(sys.argv) != 4:
    print("Usage: %s <infile> <outfile> <addr>" % sys.argv[0])
    sys.exit(1)
        
BinMagic(sys.argv[1], sys.argv[2], sys.argv[3]).run()
