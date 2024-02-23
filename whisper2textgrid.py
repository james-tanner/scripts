import json

from argparse import ArgumentParser
from pathlib import Path
from textgrid import TextGrid, IntervalTier, Interval

def get_input(fname):
    with open(fname, "r") as jsonout:
        out = json.load(jsonout)
    return out

def whisper2textgrid(input_name):

    ## read the JSON input file
    json_input = get_input(input_name)

    ## create a new empty TextGrid and interval tier
    tg = TextGrid()
    tier = IntervalTier(name = "phones")

    tname = "text" if "text" in json_input['segments'][0]['words'][0] else "word"

    ## go through each of the utterance sections
    for utterance in json_input['segments']:
        ## write each word as a new interval
        ## based on the whisper output
        for word in utterance['words']:
            print(word['start'], word['end'], word[tname])
            interval = Interval(
                minTime = word['start'],
                maxTime = word['end'],
                mark = word[tname]
            )
            tier.addInterval(interval)

    ## add the tier to the
    ## TextGrid and write out
    tg.append(tier)
    print(tg.tiers)

    return tg

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", type = Path)
    parser.add_argument("output", type = Path)
    args = parser.parse_args()

    input_name = args.input.stem
    tg_out = whisper2textgrid(args.input)

    tg_out.write(args.output.joinpath(input_name + ".TextGrid"))
