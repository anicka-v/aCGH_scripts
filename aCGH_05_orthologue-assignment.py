! /home/user/env python
# coding: utf-8
# Use: $ python aCGH_05_orthologue-assignment.py /ABS/PATH/TO/Z-or-A-linked.txt /ABS/PATH/TO/HaMStR-Outfile.txt

#1) INPUT FILE LOADING

import sys, getopt
import os
import re

inFile01 = sys.argv[1]
inFile02 = sys.argv[2]

newName = input("Input name of the output file: ")

#2) ASSIGN ORTHOLOGS

with open(inFile01, 'r') as inFile1: #Pcal
    with open(inFile02, 'r') as inFile2: #GeneIDs BMORI
            with open(newName, 'a') as outFile:
                for line1 in inFile1:
                        splitRow1 = line1.split('\t')
                        Pcal_header = splitRow1[0]
                        Pcal_ID_regex = re.compile(r'(EOG.*_)(DN.*)')
                        match = Pcal_ID_regex.search(Pcal_header)
                        Pcal_locus = (match.group(1)).strip('_')
                        inFile2.seek(0)
                        for line2 in inFile2:
                                if Pcal_locus in line2:
                                        splitRow2 = line2.split('\t')
                                        newRowList = (splitRow1[0]).strip('\n'), splitRow2[0], splitRow2[1], splitRow2[2]
                                        newRow = ('\t'.join(newRowList))
                                        outFile.write(newRow)

outFile.close()
