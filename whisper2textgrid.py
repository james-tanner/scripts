import json

from argparse import ArgumentParser
from pathlib import Path
from textgrid import TextGrid, IntervalTier, Interval

def get_input(fname):
    with open(fname, "r") as jsonout:
        out = json.load(jsonout)
    return out


def get_text_name(input_name):
    return "text" if "text" in input_name['segments'][0]['words'][0] else "word"


def make_interval(start, end, text):
    interval = Interval(
        minTime = start,
        maxTime = end,
        mark = text
        )
    return interval


def whisper2textgrid(input_name, verbose):

    ## read the JSON input file
    inp = get_input(input_name)

    ## create a new empty TextGrid and interval tier
    tg = TextGrid()
    tier = IntervalTier(name = "phones")

    tname = get_text_name(inp)

    ## go through each of the utterance sections
    for utterance in inp['segments']:
        if verbose:
            print("\n")
            print(utterance)
        ## write each word as a new interval
        ## based on the whisper output
        for word in utterance['words']:
            if verbose:
                print(word['start'], word['end'], word[tname])

            interval = make_interval(word['start'], word['end'], word[tname])
            tier.addInterval(interval)

    ## add the tier to the
    ## TextGrid and write out
    tg.append(tier)

    return tg

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", type = Path)
    parser.add_argument("output", type = Path)
    parser.add_argument("--verbose", "-v", action = "store_true")
    args = parser.parse_args()

    if args.input.is_file():
        tg_out = whisper2textgrid(args.input, args.verbose)
        tg_out.write(args.output.joinpath(args.input.stem + ".TextGrid"))
    elif args.input.is_dir():
        inputs = list(args.input.glob("*.json"))
        for inp in inputs:
            tg_out = whisper2textgrid(inp, args.verbose)
            tg_out.write(args.output.joinpath(inp.stem + ".TextGrid"))
    else:
        raise("Not a file or directory")

