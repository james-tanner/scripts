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


def get_unique_speakers(transcription):
    return set([utt['speaker'] for utt in transcription['segments']])


def convert_utterance(utterance, tier, text_name, words, verbose):

    if verbose:
        print("\n")
        print(utterance)

    if words:
        for word in utterance['words']:
            if verbose:
                print(word['start'], word['end'], word[text_name])

            interval = make_interval(word['start'], word['end'], word[text_name])
            tier.addInterval(interval)

    else:
        interval = make_interval(utterance['start'], utterance['end'], utterance['text'])
        tier.addInterval(interval)

    return tier


def whisper2textgrid(input_name, words = False, verbose = False, multispeaker = False):

    ## create a new empty TextGrid and interval tier
    tg = TextGrid()

    ## get the name of the text label
    tname = get_text_name(input_name)

    if multispeaker:
        speakers = get_unique_speakers(input_name)

        for speaker in speakers:
            if verbose:
                print(speaker)
            tier = IntervalTier(name = speaker)
            for utterance in input_name['segments']:
                if utterance['speaker'] == speaker:
                    tier = convert_utterance(utterance, tier, text_name = tname, words = words, verbose = verbose)
            tg.append(tier)

    else:
        tier = IntervalTier(name = "words")
        for utterance in input_name['segments']:
            tier = convert_utterance(utterance, tier, text_name = tname, words = words, verbose = verbose)
        tg.append(tier)

    return tg


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input", type = Path)
    parser.add_argument("output", type = Path)
    parser.add_argument("--words", "-w", action = "store_true", help = "Create word-level intervals instead of utterances (default: False)")
    parser.add_argument("--verbose", "-v", action = "store_true", help = "Print transcription information (default: False)")
    parser.add_argument("--multispeaker", "-ms", action = "store_true", help = "Convert multispeaker transcription (default: False)")
    args = parser.parse_args()

    ## check if the input is a single JSON file
    ## or a directory of JSON files
    if args.input.is_file():
        inp_json = get_input(args.input)
        tg_out = whisper2textgrid(inp_json, args.words, args.verbose, args.multispeaker)
        tg_out.write(args.output.joinpath(args.input.stem + ".TextGrid"))

    ## if directory, iterate through JSON files
    elif args.input.is_dir():
        inputs = list(args.input.glob("*.json"))
        for inp in inputs:
            print(f"Converting {inp.stem}")
            inp_json = get_input(inp)
            tg_out = whisper2textgrid(inp_json, args.words, args.verbose, args.multispeaker)
            tg_out.write(args.output.joinpath(inp.stem + ".TextGrid"))
    else:
        raise("Not a file or directory")

