## Replace names in Modern RP corpus
## James Tanner
## July 2019

import os
import re
import argparse
import textgrid
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("inputCSV", help = "Path to the CSV containing speaker information")
parser.add_argument("inputDir", help = "Path to TextGrid directory")
args = parser.parse_args()

## import CSV
data = pd.read_csv(args.inputCSV)

## iterate through speakers
for index, row in data.iterrows():
	print("Processing speaker: {}".format(row["Speaker ID"]))

	## read TextGrid
	tg = textgrid.TextGrid()
	tg.read(os.path.join(args.inputDir, row["File name"] + ".TextGrid"),
		round_digits = 6)

	## find the tier names that contain the original name
	## and replace with anonymised speaker ID
	for tier in tg:
		if re.match(row["tier_name"], tier.name):
			tier.name = re.sub(row["tier_name"], row["Speaker ID"].strip(), tier.name)

	## overwrite the original TextGrid
	tg.write(os.path.join(args.inputDir, row["File name"] + ".TextGrid"))

print("Done!")