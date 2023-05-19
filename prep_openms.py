## Convert the Open Source Multispeaker English Corpus (Open-MS)
## to a MFA-friendly format
## James Tanner May 2023

import librosa
import re
import shutil
import textgrid
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("inputdir", type=Path)
parser.add_argument("outputdir", type=Path)
args = parser.parse_args()

## make the output directory
args.outputdir.mkdir(parents=True, exist_ok=True)

## read utterance file
with open(args.inputdir.joinpath("line_index.csv"), "r") as f:
    utterances = f.readlines()

for utterance in tqdm(utterances):
    sent_id, utt_id, text = utterance.split(", ")

    ## load audio and prep for moving
    ## keep the original samplerate
    wav_fname = utt_id + ".wav"
    audio, sr = librosa.load(
        args.inputdir.joinpath(wav_fname),
        sr=None)
    audio_dur = librosa.get_duration(y=audio, sr=sr)

    ## copy audio to output dir
    shutil.copy(
        args.inputdir.joinpath(wav_fname),
        args.outputdir.joinpath(wav_fname))

    ## keep both the dialect and speaker id as a single label (to avoid overlap)
    speaker_id = re.match("([a-z]{3}\_\d+)", utt_id).groups()[0]

    tg = textgrid.TextGrid()
    tier = textgrid.IntervalTier(name=speaker_id)
    tier.add(minTime=0, maxTime=audio_dur, mark=text)
    tg.append(tier)

    tg_name = utt_id + ".TextGrid"
    tg.write(args.outputdir.joinpath(tg_name))