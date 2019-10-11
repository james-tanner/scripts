## Convert word-level intervals to utterances
## James Tanner
## October 2019

import os
import textgrid
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputDir', help = "Path to the TextGrid directory")
parser.add_argument('outputDir', help = "Path for the TextGrid output")
args = parser.parse_args()

# iterate through the files in the directory:
for root, dirs, files in os.walk(args.inputDir):
	for name in files:
		# for the purposes of testing,
		# just match the one file
		if name == "word_extract_current.TextGrid":
			print("Processing {}".format(name))

			tg = textgrid.TextGrid()
			tg.read(os.path.join(root, name))

			# also make a new TG to write to
			ntg = textgrid.TextGrid()

			## start iterating through the tiers
			for tier in tg:

				# make new interval tier with speaker name
				ntier = textgrid.IntervalTier(name = tier.name)

				# loop through the intervals
				wordList = []
				intList = []
				for interval in tier.intervals:

					# add non-silence to a word list
					if interval.mark != "!SIL":
						wordList.append(interval.mark)
						intList.append(interval)

					else:
						# check it's not just the start
						if len(wordList) > 0:
							# merge the list together,
							# take the start of the first interval
							# and end of the last interval
							ntier.add(
								mark = ' '.join(wordList),
								minTime = intList[0].minTime,
								maxTime = intList[-1].maxTime)

							# refresh lists
							intList = []
							wordList = []

				# Once you've reached the end of the tier,
				# append this to the new textgrid
				ntg.append(ntier)

			# Write the next TextGrid to file
			ntg.write(os.path.join(args.outputDir, name))
