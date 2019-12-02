## Make EDA speaker directories
## James Tanner
## December 2019

import os
import pandas as pd
import argparse
import re
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("inputCSV", help = "Path to the CSV containing speaker and file names")
parser.add_argument("inputFiles", help = "Path to the files to be copied")
parser.add_argument("outputDir", help = "Path to the directory for speaker directories to be made")
args = parser.parse_args()

# import CSV
data = pd.read_csv(args.inputCSV)

# iterate through speaker names:
for speaker in data.speaker_id.unique():
	# print("Making speaker directories for {}".format(speaker))

	# filter dataframe to match speakers
	temp = data[data.speaker_id == speaker]

	# speaker IDs are numbers to coerce to string
	speaker = str(speaker)

	for index, row in temp.iterrows():

		# checking that the file is in the input directory
		if os.path.isfile(os.path.join(args.inputFiles, row['filename'])):

			# remove file extension (in order to copy both WAV and TextGrid)
			filename = os.path.splitext(row['filename'])[0]
			
			# check if the speaker directory exists
			if not os.path.isdir(os.path.join(args.outputDir, speaker)):
				print("Making directory for {}".format(speaker))
				os.mkdir(os.path.join(args.outputDir, speaker))

			# copy files
			shutil.copy(os.path.join(args.inputFiles, filename + ".wav"), os.path.join(args.outputDir, speaker))
			shutil.copy(os.path.join(args.inputFiles, filename + ".TextGrid"), os.path.join(args.outputDir, speaker))
print("Done!")
