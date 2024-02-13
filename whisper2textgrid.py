import json
from textgrid import TextGrid, IntervalTier, Interval

## read the file
with open("text.json", "r") as jsonout:
    out = json.load(jsonout)

## create a new empty TextGrid and interval tier
tg = TextGrid()
tier = IntervalTier(name = "phones")

## go through each of the utterance sections
for utterance in out['segments']:

    ## write each word as a new interval
    ## based on the whisper output
    for word in utterance['words']:
        print(word)
        interval = Interval(
            minTime = word['start'],
            maxTime = word['end'],
            mark = word['text']
        )

        ## add that interval to the tier
        tier.addInterval(interval)
    print("\n")

## add the tier to the
## TextGrid and write out
tg.append(tier)
tg.write("text.TextGrid")
