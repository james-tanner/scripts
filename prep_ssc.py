import re
import nagisa

from argparse import ArgumentParser
from praatio import textgrid
from praatio.data_classes.interval_tier import IntervalTier
from praatio.utilities.constants import Interval
from tqdm import tqdm
from pathlib import Path
from string import punctuation

parser = ArgumentParser()
parser.add_argument("input_dir", type = Path)
parser.add_argument("output_dir", type = Path)
args = parser.parse_args()

def clean_utterance(utterance):
    if utterance == "pz":
        return ""
    
    ## remove alphanumerics
    utt = re.sub(r'[A-Za-z]*', "", utterance)

    ## cases where specific pronunciation labels are applied
    utt = re.sub(r"\(?\s(.*)\|.*\)", r'\1', utt)

    ## strip remaining punctuation
    utt = utt.translate(str.maketrans('', '', punctuation))

    ## tokenise text and add space between words
    utt_nagisa = nagisa.tagging(utt)
    utt = ' '.join(utt_nagisa.words)
    utt = re.sub('\s+', ' ', utt)

    return utt


if __name__ == "__main__":
    speakers = args.input_dir.iterdir()

    ## make the output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)    

    for speaker in tqdm(list(speakers)):
        ## make a directory (inside out dir) for the speaker
        args.output_dir.joinpath(speaker.stem).mkdir(parents=True, exist_ok=True)

        for tgrid_path in speaker.glob("*.TextGrid"):
            try:
                ## read TextGrid
                tg = textgrid.openTextgrid(tgrid_path, includeEmptyIntervals = True, reportingMode = "silence")
                utt_tier = tg.getTier(speaker.stem)

                ## make a tier to be filled
                cleaned_tier = IntervalTier(name = speaker.stem, entries = [], minT = utt_tier.minTimestamp, maxT = utt_tier.maxTimestamp)

                ## apply cleaning function to each interval
                for utt in utt_tier.entries:
                    cleaned_utt = Interval(utt.start, utt.end, clean_utterance(utt.label))
                    cleaned_tier.insertEntry(cleaned_utt)

                ## save TextGrid with cleaned intervals
                cleaned_tg = textgrid.Textgrid()
                cleaned_tg.addTier(cleaned_tier)
                out_name = args.output_dir.joinpath(speaker.stem).joinpath(tgrid_path.name)

                cleaned_tg.save(
                    fn = out_name,
                    format = "long_textgrid",
                    includeBlankSpaces = True)

            except ValueError as e:
                pass
