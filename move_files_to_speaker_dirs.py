import re
import shutil
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("input_path", type=Path)
parser.add_argument("output_path", type=Path)
args = parser.parse_args()

## get the unique speaker IDs
files = args.input_path.glob(r"*[TextGrid|wav]")
speaker_ids = set([re.match(r"([a-z]{3}\_\d+)", f.name).groups()[0] for f in files])

for speaker in speaker_ids:
    speaker_files = args.input_path.glob(f"{speaker}*")
    args.output_path.joinpath(f"{speaker}").mkdir(parents=True, exist_ok=True)
    print(args.output_path.joinpath(f"{speaker}"))
    for f in speaker_files:
        shutil.move(str(f), str(args.output_path.joinpath(f"{speaker}")))