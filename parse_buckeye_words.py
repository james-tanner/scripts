## Parse Buckeye corpus for final vowel + obstruent syllables
## James Tanner
## July 2019 

import os
import re
import csv
import argparse
import pandas as pd
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("inputDir", help = "The directory of the .words files")
parser.add_argument('outputDir', help = "The directory of the resulting CSV file")
args = parser.parse_args()

d = []

vowels = ["aa", "ae", "ay", "aw", "ao", "oy", "ow", "eh", "ey", "er", "ah", "uw", "ih", "iy", "uh", "aan", "aen", "ayn", "awn", "aon", "oyn", "own", "ehn", "eyn", "ern", "ahn", "uwn", "ihn", "iyn", "uhn"]
obstruents = ["p", "t", "k", "b", "d", "g", "f", "v", "s", "z", "th", "dh", "ch", "zh"]

def parse_words(file):

	misparsed_lines = []

	# read each line of the file
	# parsing taken from MM's Buckeye parser
	# https://github.com/MontrealCorpusTools/PolyglotDB/blob/master/polyglotdb/io/parsers/buckeye.py
	with open(file, 'r') as file_handle:
		f = re.split(r"#\r{0,1}\n", file_handle.read())[1]
		line_pattern = re.compile("; | \d{3} ")
		begin = 0.0
		flist = f.splitlines()

		# extract just the last word
		for l in flist:
			line = line_pattern.split(l.strip())
			try:
				end = float(line[0])
				word = line[1].replace(' ', '_')
				if word[0] != "<" and word[0] != "{":
					citation = line[2]
					phonetic = line[3]
					if len(line) > 4:
						category = line[4]
						# if word in FILLERS:
							# category = 'UH'
					else:
						category = None
				else:
					citation = None
					phonetic = None
					category = None
			except IndexError:
				misparsed_lines.append(l)
				continue

			if citation is not None:
				add_to_dict(word, citation)

def add_to_dict(word, citation):

	# look for last two phones in the transcription
	exp = re.compile('.*\s(.*)\s(.*)$')
	trans = exp.findall(citation)

	ObsDict = {}
	# check if they are vowel + obstruent
	for t in trans:
		if t[0] in vowels and t[1] in obstruents:
			ObsDict = {word : "True"}
		else:
			ObsDict = {word : "False"}
	# check if word is already in the dictionary or not
	if not ObsDict in d:
		d.append(ObsDict)

for root, dirs, files in os.walk(args.inputDir):
	for name in files:
		if name.endswith(".words"):
			print("Processing: {}".format(name))
			parse_words(os.path.join(root, name))

filename = os.path.join(args.outputDir, "buckeye_obstruents.csv")
print("Writing to {}".format(filename))

# write the dictionary to a csv
with open(filename, "w") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(["Word", "ContainsVowelObstruent"])
	for line in d:
		for key, value in line.iteritems():
			writer.writerow([key, value])

print("Done!")