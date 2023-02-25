import os
import re
import shutil
import pandas as pd
from argparse import ArgumentParser
from pathlib import Path
from textgrid import TextGrid

parser = ArgumentParser()
parser.add_argument("input_dir", type = Path)
parser.add_argument("speaker_key", type = Path)
parser.add_argument("output_dir", type = Path)
args = parser.parse_args()

speaker_df = pd.read_csv(args.speaker_key)

def convert_textgrid(file_name, pair):

    tg = TextGrid.fromFile(file_name)

    for t in tg.tiers:
        t.name = re.sub(rf"{pair[0]}", pair[1], t.name)

    return(tg)


for f in args.input_dir.glob("*.TextGrid"):
    speaker_name = Path(f).stem
    
    if speaker_name in speaker_df["Name"].values:
        df = speaker_df[speaker_df["Name"] == speaker_name]
        speaker_code = df["Code"].values[0]
        speaker_code_pair = (speaker_name, speaker_code)
        print(speaker_code_pair)

        new_tg = convert_textgrid(f, speaker_code_pair)
        new_tg.write(args.output_dir.joinpath(f"{speaker_code}.TextGrid"))
        shutil.copy(
            args.input_dir.joinpath(f"{speaker_name}.wav"),
            args.output_dir.joinpath(f"{speaker_code}.wav"))

