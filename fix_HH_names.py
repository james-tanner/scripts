## quick fix for speaker names
## James Tanner
## February 2020

import os
import glob
import textgrid
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('inputFiles', help = "Directory of the textgrids")
parser.add_argument('outputFiles', help = "Directory for where to write textgrids to")
args = parser.parse_args()

for root, dirs, files in os.walk(args.inputFiles):
	for name in files:
		if name.endswith(".TextGrid"):
			print("Processing: {}".format(name))

			tg = textgrid.TextGrid()
			tg.read(os.path.join(args.inputFiles, name))

			for tier in tg:
				tier.name = re.sub("(.*)_(.*)", "\\1\\2", tier.name)

	tg.write(os.path.join(args.outputFiles, name))