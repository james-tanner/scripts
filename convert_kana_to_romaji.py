## Script to convert Japanese kanji & hiragana to romaji for forced alignment
## James Tanner
## July 2019

import os
import textgrid
import webvtt
import argparse
import pykakasi

parser = argparse.ArgumentParser()
parser.add_argument("inputDir",
	help = "The directory containing textgrids to be converted")
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
			print("Processing {}".format(name))

			## read textgrid
			tg = textgrid.TextGrid()
			tg.read(os.path.join(root, name))

			# assume that Y-t-P outputs a single
			# utterance-level tier
			for kanjiTier in tg:

				romajiTier = textgrid.IntervalTier(
					name = "romaji")

				# convert kanji to romaji
				for interval in kanjiTier.intervals:

					romajiInt = textgrid.Interval(
						minTime = interval.minTime,
						maxTime = interval.maxTime,
						mark = conv.do(interval.mark))

					romajiTier.addInterval(romajiInt)

			# remove the kana/kanji tier
			# as it creates problems for the MFA
			for i, tier in enumerate(tg.tiers):
				if tier.name != "romaji":
					tg.pop(i)
			tg.append(romajiTier)

			tg.write(os.path.join(root, name))
print("Done")