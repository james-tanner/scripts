## Script to convert Japanese kanji & hiragana to romaji for forced alignment
## James Tanner
## July 2019

import os
import re
import textgrid
import argparse
import pykakasi

parser = argparse.ArgumentParser()
parser.add_argument("inputDir",
	help = "The directory containing textgrids to be converted")
parser.add_argument("outputDir",
	help = "The directory to place the converted textgrids")
parser.add_argument("--speaker_name",
	help = "Use the name of the directory as the tier name; else uses filename (default: False)",
	action = 'store_true')
parser.add_argument("--kana_tier",
	help = "The name of the tier containing the kana/kanji transcription")
args = parser.parse_args()

# see kanji converter
kakasi = pykakasi.kakasi()
kakasi.setMode("H","a") # Hiragana to ascii, default: no conversion
kakasi.setMode("K","a") # Katakana to ascii, default: no conversion
kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
kakasi.setMode("s", True) # add space, default: no separator
kakasi.setMode("C", False) # capitalize, default: no capitalize
conv = kakasi.getConverter()

for root, dirs, files in os.walk(args.inputDir):
	for name in files:
		if name.endswith(".TextGrid"):
			print("Processing {}".format(name), end = "...")

			## read textgrid
			tg = textgrid.TextGrid()
			tg.read(os.path.join(root, name))

			# search textgrid for a tier with a specific name
			# if no name specified, look at the first tier
			for Tier in tg:
				if args.kana_tier is None:
					args.kana_tier = tg.getNames()[0]

				if Tier.name == args.kana_tier:

					romajiTier = textgrid.IntervalTier()
					if args.speaker_name:
						path = os.path.basename(os.path.dirname(os.path.join(root, name)))
						romajiTier.name = path
					else:
						romajiTier.name = os.path.splitext(name)[0]

					# convert kanji to romaji
					for interval in Tier.intervals:

						# skip intervals with dummy silence
						if interval.mark == "#":
							continue

						# take interval information from original
						# and apply convertor to the interval name
						else:
							romajiInt = textgrid.Interval(
								minTime = interval.minTime,
								maxTime = interval.maxTime,
								mark = conv.do(interval.mark))

						romajiTier.addInterval(romajiInt)

			# create an empty TextGrid object to write romaji tier to
			newTg = textgrid.TextGrid()
			newTg.append(romajiTier)

			# write textgrid to file
			print("saving to {}".format(os.path.join(args.outputDir, name)))
			newTg.write(os.path.join(args.outputDir, name))

print("Done")