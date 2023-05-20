import re
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("input_path", type=Path)
parser.add_argument("output_path", type=Path)
args = parser.parse_args()

## simple table for converting dialect labels
dialect_dict = {
    "ir" : "Ireland",
    "mi" : "Midlands England",
    "no" : "Northern England",
    "sc" : "Scotland",
    "so" : "Southern England",
    "we" : "Welsh"
}

## get the speaker IDs from the filenames
files = args.input_path.glob("*.TextGrid")
speaker_ids = set([re.match(r"([a-z]{3}\_\d+)", f.name).groups()[0] for f in files])

with open(args.output_path, "w") as f:
    ## write column headers
    f.write(",".join(["speaker", "dialect", "gender"]) + "\n")

    ## ID format:
    ## first 2 chars = dialect
    ## 3rd = gender
    ## rest is (non)unique number assignment
    for speaker in speaker_ids:
        spk = speaker[:3]
        dialect_abbrev, gender_abbrev = spk[0:2], spk[2:]

        ## expand gender    
        gender = "female" if gender_abbrev == "f" else "male"
        dialect = dialect_dict[dialect_abbrev]

        f.write(",".join([spk, dialect, gender]) + "\n")

print("Done!")
