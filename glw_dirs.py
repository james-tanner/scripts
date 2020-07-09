## Automated script for making Glaswasian speaker directories
## James Tanner
## July 2020

import argparse
import re
import os
import shutil
import pandas as pd
import textgrid

parser = argparse.ArgumentParser()
parser.add_argument("inputCSV", help = "Path to the CSV containing speaker and file names")
parser.add_argument("inputFiles", help = "Path to the files to be copied")
parser.add_argument("outputDir", help = "Path to the directory for speaker directories to be made")
parser.add_argument("--speaker_id", help = "Name of speaker ID column (default = 'speaker_id')", default = "speaker_id")
parser.add_argument("--file", help = "Name of filename column (default = 'file')", default = "file")

## read speaker metadata file
df = pd.read_csv(args.inputCSV)

for index, row in df.iterrows():

	speaker = args.speaker_id
	file = args.file

	print("Processing {} for {}".format(file, speaker))
	## make speaker directory
	## if it doesn't exist
	if not os.path.isdir(os.path.join(args.outputDir, row['speaker'])):
		os.mkdir(os.path.join(args.outputDir, row['speaker']))

	## start modifying the textgrid
	## to just have tiers from
	## that speaker
	tg = textgrid.TextGrid()
	tg_new = textgrid.TextGrid()

	tg.read(os.path.join(args.inputFiles, row['file'] + ".TextGrid"))

	for tier in tg:

		## find tiers containing the speaker name
		if re.match(row['speaker'], tier.name):
			tg_new.append(tier)

	## formulate the output path
	outPath = os.path.join(args.outputDir, row['speaker'])

	## save textgrid to the new directory
	## and copy the audio file
	tg_new.write(os.path.join(outPath, row['file'] + row['speaker'] + ".TextGrid"))
	shutil.copy(os.path.join(args.inputCSV, row['file'] + ".wav"), os.path.join(outPath, row['file'] + row['speaker'] + ".wav"))

print("Done!")
