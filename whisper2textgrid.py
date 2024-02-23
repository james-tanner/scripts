import json

from argparse import ArgumentParser
from pathlib import Path
from textgrid import TextGrid, IntervalTier, Interval

def get_input(fname):
    with open(fname, "r") as jsonout:
        out = json.load(jsonout)
    return out


def get_text_name(input_name):
    ## determine if whisper text label is
    ## either 'text' or 'word'
    return "text" if "text" in input_name['segments'][0]['words'][0] else "word"


def make_interval(start, end, text):
    interval = Interval(
        minTime = start,
        maxTime = end,
        mark = text
        )
    return interval


def whisper2textgrid(input_name, words = False, verbose = False):

    ## create a new empty TextGrid and interval tier
    tg = TextGrid()
    tier = IntervalTier(name = "phones")

    ## get the name of the text label
    tname = get_text_name(input_name)

    ## go through each of the utterance sections
    for utterance in input_name['segments']:
        if verbose:
            print("\n")
            print(utterance)

        if words:
            ## write each word as a new interval
            ## based on the whisper output
            for word in utterance['words']:
                if verbose:
                    print(word['start'], word['end'], word[tname])

                interval = make_interval(word['start'], word['end'], word[tname])
                tier.addInterval(interval)
        else:
            interval = make_interval(utterance['start'], utterance['end'], utterance['text'])
            tier.addInterval(interval)

    ## add the tier to the
    ## TextGrid and write out
    tg.append(tier)

    return tg

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", type = Path)
    parser.add_argument("output", type = Path)
    parser.add_argument("--words", "-w", action = "store_true", help = "Create word-level intervals instead of utterances (default: False)")
    parser.add_argument("--verbose", "-v", action = "store_true", help = "Print transcription information (default: False)")
    args = parser.parse_args()

    ## check if the input is a single JSON file
    ## or a directory of JSON files
    if args.input.is_file():
        inp_json = get_input(args.input)
        tg_out = whisper2textgrid(inp_json, args.words, args.verbose)
        tg_out.write(args.output.joinpath(args.input.stem + ".TextGrid"))

    ## if directory, iterate through JSON files
    elif args.input.is_dir():
        inputs = list(args.input.glob("*.json"))
        for inp in inputs:
            print(f"Converting {inp.stem}")
            inp_json = get_input(inp)
            tg_out = whisper2textgrid(inp_json, args.words, args.verbose)
            tg_out.write(args.output.joinpath(inp.stem + ".TextGrid"))
    else:
        raise("Not a file or directory")

