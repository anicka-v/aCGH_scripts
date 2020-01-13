#! /home/user/env python
# coding: utf-8
#
## USAGE:
#1) make new directory (= input directory) and move all array outputs there
#2) download Species_GeneList.txt from Agilent eArray website (= probes) 
#3) run script as follows: $ python script.py /ABSOLUTE/PATH/TO/INPUT/directory/ /ABSOLUTE/PATH/TO/probes.txt
#
##ANALYSIS
#01) PREPARE WORKSPACE AND LOAD INPUT FILES

import sys, getopt
import os
import re

inputDir = sys.argv[1]
pathToProbes = sys.argv[2]
speciesName = input("Please input abbreviation of your species: ")

timestamp = time.strftime("%d/%m/%Y %H:%M")
print("aCGH analysis of" + species + ", started " + timestamp + "."
"Loading raw files from:" + inputDir + "."
"Loading probes from"  + pathToProbes + ".")

#02) CREATE WORKING FOLDERS

for file in os.listdir(inputDir):
	if file.endswith(".txt"):
		rawDataFile = file
		newFileName = re.compile(r'(.*)(_\d_\d).txt$')
		mo = newFileName.search(rawDataFile)

		uniqueDirName = speciesName + "_Array_workDir" + mo.group(2)
		workDirPath = inputDir + uniqueDirName + '/'
		os.mkdir(workDirPath)
		os.chdir(workDirPath)
		print(os.getcwd())

#03) CREATING FILE WITH TARGET DATA
		
		rawDataPath = inputDir + rawDataFile
		with open(rawDataPath, 'r') as rawData, open(('f01_TargetDataAll' + mo.group(2) + '.txt'), 'a') as f01:
			for line in rawData:
				splitRow01 = line.split('\t')
				if len(splitRow01) == 43:
					newRow01_list = [splitRow01[6], splitRow01[13], splitRow01[14], splitRow01[17], splitRow01[18], 					splitRow01[19], splitRow01[20], splitRow01[23], splitRow01[24]]
					newRow01 = '\t'.join(newRow01_list)
					f01.write(newRow01 + '\n')
	
		with open(('f01_TargetDataAll' + mo.group(2) + '.txt'), 'r') as f01:
			with open(('f01-1_TargetColumns' + mo.group(2) + '.txt'), 'w') as f011 , open(('f01-2_Discarded' + mo.group(2) + 				'.txt'), 'w') as f012:
				for line in f01:
					RowsRE = re.compile(r'^CUST.*$')
					if RowsRE.match(line):
						f011.write(line)
					else:
						f012.write(line)
						
#04)EXCLUDE DATA IF MAJORITY OF PIXELS SATURATED (gIsSaturated and rIsSaturated = 1)

		with open(('f01-1_TargetColumns' + mo.group(2) + '.txt'), 'r') as f011_in:
			with open(('f02_SatPixelsExcluded' + mo.group(2) + '.txt'), 'a') as f02:
				for line in f011_in:
					StripRow = line.strip('\n')
					SplitRow = StripRow.split("\t")
					if int(SplitRow[7]) == 1:
						pass
					elif int(SplitRow[8]) == 1:
						pass
					else:
						f02.write(line)

#05) EXCLUDE DATA IF MEDIAN PIXEL INTENSITY LESS THAN TWO TIMES BACKGROUND (gMedianSignal>2*gBGMedianSignal and rMedianSignal>2*rBGMedianSignal)

		with open(('f02_SatPixelsExcluded' + mo.group(2) + '.txt'), 'r') as f02_in:
			with open (('f03_LowIntExcluded' + mo.group(2) + '.txt'), 'a') as f03:
				for line in f02_in:
					SplitRow4 = line.split("\t")
					if float(SplitRow4[3]) < 2 * float(SplitRow4[5]):
						pass
					elif float(SplitRow4[4]) < 2 * float(SplitRow4[6]):
						pass
					else:
						NewRow4List = SplitRow4[0], SplitRow4[1], SplitRow4[2]
						NewRow4 = ('\t'.join(NewRow4List) + '\n')
						f03.write(NewRow4)

#06) COUNT LOG2 RATIOS (in Lepidoptera, heterozygous sex is female => defined as male(Cy5)/female(Cy3) intensity => red/green ProcessedSignal)

		import math
		with open(('f03_LowIntExcluded' + mo.group(2) + '.txt'), 'r') as f03_in:
			with open (('f04_Log2Ratios' + mo.group(2) + '.txt'), 'a') as f04:
				for line in f03_in:
					SplitRow5 = line.split("\t")
					ratio = float(SplitRow5[2]) / float(SplitRow5[1])
					log2 = math.log(ratio, 2)
					NewRow5List = SplitRow5[0], str(log2)
					NewRow5 = ('\t'.join(NewRow5List) + '\n')
					f04.write(NewRow5)
#06) MATCH PROBES WITH ORTHOLOGS

		ProbeID_path = pathToProbes
		with open(ProbeID_path, 'r') as probes:
			with open (('f04_Log2Ratios' + mo.group(2) + '.txt'), 'r') as f04_in, open(('f05_ProbesMatched' + mo.group(2) + '.txt'), 'a') as f05:
				for line in f04_in:
					SplitRow6 = line.split("\t")
					probeID = SplitRow6[0]
					probes.seek(0)
					for line in probes:					
						if probeID in line:
							SplitRow7 = line.split("\t")
							NewRow6Line = SplitRow7[0], (SplitRow7[1]).strip('\n'), SplitRow6[1]
							NewRow6 = ('\t'.join(NewRow6Line))
							f05.write(NewRow6)
							break
#07) GROUP PROBES BY GENE ID

		import csv
		Reader = csv.reader(open(('f05_ProbesMatched' + mo.group(2) + '.txt'), 'r'), delimiter="\t")
		DictIDLog={}
		for Row in Reader:
		    if Row[1] not in DictIDLog.keys():
		        DictIDLog[Row[1]] = [Row[2]]
		    else:
		        DictIDLog[Row[1]].append(Row[2])
	
		with open(('f06_ProbesGroupedByGeneID' + mo.group(2) + '.txt'),'w') as f06:
			for key, value in sorted(DictIDLog.items()):
				NewRow7 = (key+'\t'+'\t'.join(value)+"\n")
				f06.write(NewRow7)

#g) MEDIAN OF LOG2 RATIOS

		import statistics
		with open (('f06_ProbesGroupedByGeneID' + mo.group(2) + '.txt'), 'r') as f06_in, open(('f07_MedianPerProbe' + mo.group(2) + '.txt'), 'a') as f07:
			for line in f06_in:
				SplitRow8 = line.split("\t")
				LogValues = SplitRow8[1:]
				Float = [float(i) for i in LogValues]    
				Median = statistics.median(Float)
				NewRowList = SplitRow8[0], str(Median)
				NewRow8 = ('\t'.join(NewRowList) + '\n')
				f07.write(NewRow8)

