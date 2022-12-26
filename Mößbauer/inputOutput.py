import os
import csv
import re
import math
from tkinter import Tk

def readRawData(fileName) -> list[list]:
	directory = os.path.dirname(os.path.realpath('__file__'))
	absFileName = directory + "/" + fileName
	reader = csv.reader(open(absFileName, 'r'), delimiter='\t', skipinitialspace = True)
	channels = []
	counts = []
	wordReg = re.compile('[a-zA-Z]')
	for row in reader:
		if (row[0].startswith(("!","#")) or wordReg.match(row[0]) != None):
			continue
		else:
			# print(f"row ${row}")
			channel, countNumber, folded = row
			channels.append(int(channel))
			counts.append(int(countNumber))
	return (channels, counts)

def readRawKalib(fileName) -> list[list]:
	directory = os.path.dirname(os.path.realpath('__file__'))
	absFileName = directory + "/" + fileName
	reader = csv.reader(open(absFileName, 'r'), delimiter='\t', skipinitialspace = True)
	voltages = []
	velocities = []
	velErrs = []
	voltErrs = []
	for row in reader:
		if (row[0].startswith(("!","#"))):
			continue
		else:
			# print(f"row ${row}")
			volt, vel, velErr, voltErr = row
			voltages.append(float(volt))
			velocities.append(float(vel))
			velErrs.append(float(velErr))
			voltErrs.append(float(voltErr))
	return (voltages, velocities, velErrs, voltErrs)

def zipValuesErrors(values: list, errors: list, roundValues: bool = False):
	negValues = False
	
	if roundValues:
		# find lowest value
		lowestAbsVal = math.inf
		for v in errors:
			if (v < 0):
				v *= -1
				negValues = True
			if v < lowestAbsVal:
				lowestAbsVal = v
		for v in values:
			if (v < 0):
				v *= -1
				negValues = True
			if v < lowestAbsVal:
				lowestAbsVal = v
		
		magnitude = math.floor(math.log10(lowestAbsVal))
		if (lowestAbsVal / (10 ** magnitude) <= 2.5):
			magnitude -= 1
		
		for i in range(len(values)):
			values[i] = round(values[i], -magnitude)
			errors[i] = round(errors[i], -magnitude)
		if (magnitude >= 0):
			values = [int(value) for value in values]
			errors = [int(error) for error in errors]
	
	list = []
	
	if (magnitude >= 0):
		for value, error in zip(values, errors):
			list.append(f"${value} \pm {error}$")
	else:
		lengthV = 0
		for value in values:
			s = str(abs(value))
			lengthV = max(lengthV, len(s))
		
		lengthE = 0
		for error in errors:
			s = str(abs(error))
			lengthE = max(lengthE, len(s))
		
		for value, error in zip(values, errors):
			strV = " " if value > 0 else ""
			strV += str(value)
			while (len(strV) <= lengthV):
				strV += "0"
			
			strE = str(error)
			while (len(strE) < lengthE):
				strE += "0"
			
			list.append(f"${strV} \pm {strE}$".replace(".", ","))
	
	return list

def showListAsLatexTable(caption: str, label, headers: list[str], valueLists: list, justCol: str = None):
	numCol = len(headers)
	
	text = """\\begin{table}[ht]
	\caption{%s}
	\centering
	\\begin{tabular}{|""" % caption
	
	# insert structure
	if (justCol):
		text+=justCol
	else:
		for values in valueLists:
			if (type(values[0]) == int or type(values[0]) == float
			  or (type(values[0]) == str and values[0].startswith("$"))):
				text += "r|"
			else:
				text += "l|"
	
	text += """}
		\hline
		"""
	# insert headers
	for i in range(numCol):
		text += str(headers[i])
		text += "\\\\\n\t\t\hline\n\t\t" if i == numCol - 1 else " & "
	
	# insert values
	for row in range(len(valueLists[0])):
		for i in range(numCol):
			text += str(valueLists[i][row])
			text += "\\\\\n\t\t" if i == numCol - 1 else " & "
	
	# bottom
	text += """\hline
	\end{tabular}  
	\label{tab:%s}
\end{table}""" % label
	
	# output
	
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(text)
	r.update() # now it stays on the clipboard after the window is closed
	r.destroy()
	
	print("--- LaTeX Table for (%s) ---\n" % caption)
	print(text)

filePath = "D:\Workspace\F-Praktikum\Röntgen\hkl.csv"
headers = ["""$m$""", """$n$""", """$r_\\t{Mess}$""", """$\Delta r_\\t{Mess}$""", """$r_\\t{Vesta}$"""]
reader = csv.reader(open(filePath, 'r'), delimiter='\t', skipinitialspace = True)
mList = nList = rList = rErrList = rExpList = []
for row in reader:
	m, n, r, rErr, rExp = row
	mList.append(m)
	nList.append(n)
	rList.append(r)
	rErrList.append(rErr)
	rExpList.append(rExp)
showListAsLatexTable("Verhältnisse $r$ aller Kombinationen der gemessenen Peaks", "r", headers, [mList, nList, rList, rErrList, rExpList])

def saveListAsCSV(columns: list[list[any]], fileName: str, headers: list[str] = None):
	file = open(fileName, "w", newline="")
	writer = csv.writer(file, delimiter="\t")
	
	if (headers != None):
		writer.writerow(headers)
	
	for row in zip(*columns):
		writer.writerow(row)