import json

from argparse import ArgumentParser
from audiofile import duration
from pathlib import Path
from textgrid import TextGrid, IntervalTier, Interval

def get_input(fname):
    with open(fname, "r") as jsonout:
        out = json.load(jsonout)
    return out


def get_text_name(input_name):
    ## determine if whisper text label is either 'text' or 'word'
    try:
        if input_name['segments'][0]['words'][0]:
            return "word"
    except KeyError:
        return "text"


def get_wav_dur(json_fpath):
    wav_fpath = str(json_fpath).replace(".json", ".wav")
    return duration(wav_fpath)


def make_interval(start, end, text):
    interval = Interval(
        minTime = start,
        maxTime = end,
        mark = text
        )
    return interval


def get_unique_speakers(transcription):
    speakers = []
    for utt in transcription['segments']:
        try:
            speakers.append(utt['speaker'])
        except KeyError:
            utt['speaker'] = "unknown"
            speakers.append(utt['speaker'])
    return set(speakers)


def convert_utterance(utterance, tier, text_name, words, verbose):
    if verbose:
        print("\n")
        print(utterance)

    if words:
        for word in utterance['words']:
            if verbose:
                print(word['start'], word['end'], word[text_name])

            ## create word-level intervals
            interval = make_interval(word['start'], word['end'], word[text_name])
            tier.addInterval(interval)

    else:
        ## create utterance-level intervals
        interval = make_interval(utterance['start'], utterance['end'], utterance['text'])
        tier.addInterval(interval)

    return tier


def whisper2textgrid(input_name, wav_duration, words = False, verbose = False, multispeaker = False):

    ## create a new empty TextGrid and interval tier
    tg = TextGrid()

    ## get the name of the text label
    tname = get_text_name(input_name)

    if multispeaker:
        speakers = get_unique_speakers(input_name)

        ## get each speaker name and
        ## write separate tiers for each
        for speaker in speakers:
            if verbose:
                print(speaker)
            tier = IntervalTier(name = speaker, minTime = 0, maxTime = wav_duration)

            for utterance in input_name['segments']:

                ## write intervals to the tier
                ## corresponding to that speaker
                try:
                    if utterance['speaker'] == speaker:
                        tier = convert_utterance(utterance, tier, text_name = tname, words = words, verbose = verbose)
                except ValueError as e:
                    print(f"Skipping malformed interval: {e}")
                    continue

            ## add tier to textgrid
            tg.append(tier)

    else:
        ## make a single tier and write
        ## all intervals to it
        tier = IntervalTier(name = "words", minTime = 0, maxTime = wav_duration)
        for utterance in input_name['segments']:
            try:
                tier = convert_utterance(utterance, tier, text_name = tname, words = words, verbose = verbose)
            except ValueError as e:
                print(f"Skipping malformed interval: {e}")
                continue
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
        wav_dur = get_wav_dur(args.input)
        inp_json = get_input(args.input)
        tg_out = whisper2textgrid(inp_json, wav_dur, args.words, args.verbose, args.multispeaker)
        tg_out.write(args.output.joinpath(args.input.stem + ".TextGrid"))

    ## if directory, iterate through JSON files
    elif args.input.is_dir():
        inputs = list(args.input.glob("*.json"))
        for inp in inputs:
            print(f"Converting {inp.stem}")
            wav_dur = get_wav_dur(inp)
            inp_json = get_input(inp)
            tg_out = whisper2textgrid(inp_json, wav_dur, args.words, args.verbose, args.multispeaker)
            tg_out.write(args.output.joinpath(inp.stem + ".TextGrid"))
    else:
        raise("Not a file or directory")

