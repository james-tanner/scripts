## Quick script for changing tiers for P2FA-aligned corpora
## James Tanner
## May 2020

import argparse
import os
import re
import textgrid

parser = argparse.ArgumentParser()
parser.add_argument("inputDir", help = "Path to TextGrid input directory")
parser.add_argument('outputDir', help = "Path to TextGrid output directory")
args = parser.parse_args()

## start iterating through files in the input directory

for root, dirs, files in os.walk(args.inputDir):
	for name in files:
		if name.endswith(".TextGrid"):
			print("Processing: {}".format(name))

			tg = textgrid.TextGrid()
			tg.read(os.path.join(args.inputDir, name))

			## extract speaker name
			speaker = re.search("(.*)\.TextGrid", name).groups(1)[0]
			
			for t in tg.tiers:
				if speaker in t.name:
					t.name = speaker + " - words"
				elif t.name == "phone":
					t.name = speaker + " - phones"
				else:
					continue

			tg.write(os.path.join(args.outputDir, name))

