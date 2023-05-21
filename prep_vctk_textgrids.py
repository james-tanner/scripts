import librosa
import re
import shutil
import textgrid
from argparse import ArgumentParser
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("inputdir", type=Path)
parser.add_argument("wavdir", type=Path)
parser.add_argument("outputdir", type=Path)
args = parser.parse_args()

def make_tgs(speaker_dir):
    text_files = speaker_dir.glob("*")

    for text in text_files:
        ## first make the dir if it isn't exist
        args.outputdir.joinpath(speaker_dir.stem).mkdir(parents=True, exist_ok=True)

        ## first get the wav file duration
        wav_fname = str(args.wavdir.joinpath(speaker_dir.stem).joinpath(text.stem)) + ".wav"
        audio, sr = librosa.load(
        args.inputdir.joinpath(wav_fname),
        sr=None)
        audio_dur = librosa.get_duration(y=audio, sr=sr)

        ## make the textgrid from the text
        with open(text, "r") as f:
            t = f.read()

        tg = textgrid.TextGrid()
        tier = textgrid.IntervalTier(name=text.stem)
        tier.add(minTime=0, maxTime=audio_dur, mark=t)
        tg.append(tier)

        tg_name = text.stem + ".TextGrid"
        tg.write(args.outputdir.joinpath(speaker_dir.stem).joinpath(tg_name))


if __name__ == "__main__":
    dirs = list(args.inputdir.glob("*"))

    ## run in parallel
    with Pool(12) as pool:
        list(tqdm(pool.imap_unordered(make_tgs, dirs), total = len(dirs)))