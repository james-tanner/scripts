## Strip puncuation from word-level textgrid transcriptions
## James Tanner
## June 2019

import os
import re
import argparse
import string
import textgrid

parser = argparse.ArgumentParser()
parser.add_argument("inputDir", help = "The directory containing textgrids you want to clean")
parser.add_argument("outputDir", help = "THe directory in which to write the cleaned textgrids")
args = parser.parse_args()

## remove punctation from a word if there is any
def strip_punct(word):
	return "".join([w for w in word if w not in string.punctuation])

## iterate through subfolders (assuming directory structure
## same in both input and output folders)
for root, dirs, files in os.walk(args.inputDir):
	for directory in dirs:
		for name in files:

			# find Textgrids
			if name.endswith(".TextGrid"):
				print("Processing: {}".format(os.path.join(root, directory, name)))

				tg = textgrid.TextGrid()
				tg.read(os.path.join(path, file))

				# read transcript tier
				wt = textgrid.IntervalTier()

				# Find the name of the transcript tiers
				# regex match as some tiers have extensions
				for item in tg.getNames():
					if re.search('(transcript.*)', item) is None:
						continue
					tierName = re.findall('(transcript.*)', item)[0]
					print("Using {}...".format(tierName))

					# loop through intervals and remove punctuation
					for interval in tg.getList(tierName)[0]:
						wt.add(interval.minTime,interval.maxTime,
							strip_punct(interval.mark))

					# Remove the original tier and replace
					# with the punctuation-less version
					tg.pop(tg.getNames().index(tierName))
					wt.name = tierName

					# add tier to textgrid and save
					tg.append(wt)
					print("Saving as: {}".format(os.path.join(args.outputDir, directory, file)))
					tg.write(os.path.join(args.outputDir, directory file))
print("Done!")