#! /home/user/env python
# coding: utf-8
# Use: python script.py </PATH/File01.txt> </PATH/File02.txt>

#1) DATA INPUT FILE LOADING

import sys, getopt
import os
import re

inFile01 = sys.argv[1]
inFile02 = sys.argv[2]
print(inFile01)
print(inFile02)

newName = input("Input name of output file: ")

#2) PROCESS DATA OF INTEREST

with open(inFile01, 'r') as inFile1, open(inFile02, 'r') as inFile2, open (newName, 'a') as outFile:
    for line1 in inFile1:
        splitRow01 = line1.split('\t')
        headerIn1 = splitRow01[0]
        inFile2.seek(0)
        for line2 in inFile2:
                if headerIn1 in line2:
                        splitRow02 = line2.split('\t')
                        newRowList = splitRow01[0], (splitRow01[1]).strip('\n'), splitRow02[1]
                        newRow = ('\t'.join(newRowList))
                        outFile.write(newRow)
                        break
                        

