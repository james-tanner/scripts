## Replace A/B speaker names with Speaker IDs from CSV
## James Tanner
## September 2019

import os
import re
import argparse
import textgrid
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('inputCSV', help = "Path to the CSV containing speaker information")
parser.add_argument('inputDir', help = "Path to the TextGrid directory")
args = parser.parse_args()

## import CSV
data = pd.read_csv(args.inputCSV)

# Iterate through rows
for index, row in data.iterrows():
	print("Processing speaker: {}".format(row["ID"]))

	## open TextGrid
	tg = textgrid.TextGrid()
	# filename needs the corpus code prepended
	filename = "sw0" + str(row["ID"])

	# don't have access to all of the files
	# so only open the ones that can be found
	try:
		tg.read(os.path.join(args.inputDir, filename + ".TextGrid"))

		## find and replace A or B with tier name
		for tier in tg:
			if re.match("A - [phone|word]", tier.name):
				tier.name = re.sub("A", str(row["caller_from"]), tier.name, 1)
				print(tier.name)
			if re.match("B - ['phone|word]", tier.name):
				tier.name = re.sub("B", str(row["caller_to"]), tier.name, 1)
				print(tier.name)

		# overwrite original textgrid
		tg.write(os.path.join(args.inputDir, filename + ".TextGrid"))

	except:
		print("No TextGrid called {}: skipping".format(filename))