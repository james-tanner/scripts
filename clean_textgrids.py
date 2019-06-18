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
args = parser.parse_args()

## remove punctation from a word if there is any
def strip_punct(word):
    return "".join([w for w in word if w not in string.punctuation])

## iterate through directory
for root, dirs, files in os.walk(args.inputDir):
    for name in files:
        if name.endswith(".TextGrid"):
            print("Processing: {}".format(name))

            ## read textgrid
            tg = textgrid.TextGrid()
            tg.read(os.path.join(root, name))

            for tier in tg.getNames():
                # ignore non-transcript tiers
                if re.search('(transcript.*)', tier) is None:
                    continue
                # make list of 'transcript' tiers
                transcriptTiers = re.findall('(transcript.*)', tier)
                for item in transcriptTiers:
                    pos = tg.getNames().index(item)

                    # create interval tier and
                    # and cleaned intervals
                    wt = textgrid.IntervalTier(name = item)
                    tr = tg.getList(item)[0]
                    tg.tiers.pop(pos)

                    for interval in tr:
                        try:
                            wt.add(interval.minTime, interval.maxTime,
                                    strip_punct(interval.mark))
                        except Exception as e:
                            print(name, e)

                    # Remove the original tier and replace
                    # with the punctuation-less version
                    tg.append(wt)
            # save textgrid
            tg.write(os.path.join(os.path.join(root, name)))
print("Done!")
