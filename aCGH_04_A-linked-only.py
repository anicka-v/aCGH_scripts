#! /home/user/env python
# coding: utf-8
#
##Script to extract A-linked genes
#USAGE: python A-linked_ONLY.py /ABS/PATH/TO/DIR/Infile_OK.txt
#
#1) PREPARE WORKSPACE
import sys
import os
import statistics

inputFile = sys.argv[1]
species = input("Input abbreviation of your species: ")

treshold = "0.5"

with open(inputFile, 'r') as inFile, open((species + "_A-linked_ONLY.txt"), 'w') as outFile:
	for line in inFile:
		if line.startswith("E"):
			splitRow = line.split('\t')
			geneID = splitRow[0] + '\n'
			repValues = splitRow[1:]
			Floats = [float(i) for i in repValues]
			medianReps = statistics.median(Floats)
			if medianReps < float(treshold):
				outFile.write(geneID)
			else:
                        	continue
inFile.close()
outFile.close()

print("Analysis done.")
                

