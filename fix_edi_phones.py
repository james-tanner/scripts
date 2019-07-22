## Replace SAMPA labels in Edinburgh corpus
## James Tanner
## July 2019

import os
import re
import argparse
import textgrid

parser = argparse.ArgumentParser()
parser.add_argument("inputDir", help = "Path to TextGrid directory")
args = parser.parse_args()

# phones to check
phones = {
	"i" : "i:",
	"6" : "V",
	"}:" : "u:",
	"{I" : "eI",
	"o" : "@U",
	"aU@" : "aU"
}

for root, dirs, files in os.walk(args.inputDir):
	for name in files:
		if name.endswith(".TextGrid"):

			tg = textgrid.TextGrid()
			tg.read(os.path.join(root, name), encoding = None)

			## iterate through tiers
			for tier in tg:
				if tier.name == "MAU":
					for interval in tier.intervals:


						# look through phone types on that tier
						for k, v in phones.items():
							if re.match("^"+ k + "$", interval.mark):
								# print(interval.mark, interval.minTime, interval.maxTime)
								print("Replacing {} at {} with {}".format(
									"^"+ k + "$", interval.minTime, v))
								interval.name = re.sub("^"+ k + "$", v, interval.mark, 1)

			# overwrite textgrids					
			print("Saving to {}".format(os.path.join(args.inputDir, name)))
			tg.write(os.path.join(args.inputDir, name))
print("Done!")