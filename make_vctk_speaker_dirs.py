import pandas as pd
import shutil
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("inputcsv", type=Path)
parser.add_argument("wavdir", type=Path)
parser.add_argument("tgdir", type=Path)
parser.add_argument("outputdir", type=Path)
args = parser.parse_args()

## split dataset by dialect
df = pd.read_csv(args.inputcsv)
df_list = [d for _, d in df.groupby(['dialect2'])]

for d in df_list:
    ## make dir for each dialect
    dialect = d['dialect2'].unique()[0].strip()
    print(f"{dialect}\t\t{len(d['speaker'])}")
    dialect_path = args.outputdir.joinpath(dialect)
    dialect_path.mkdir(parents=True, exist_ok=True)

    ## copy the speaker file to the dir
    shutil.copy(args.inputcsv, dialect_path)
    
    for speaker in tqdm(d['speaker']):
        ## make a subdir for each speaker:
        ## str = dialect/speaker/speaker_XXX.[wav|TextGrid]
        speaker_path = dialect_path.joinpath(speaker)
        speaker_path.mkdir(parents=True, exist_ok=True)

        ## find all the wavs files for the speaker
        for wav in args.wavdir.glob(rf"{speaker}*.wav"):
            shutil.copy(args.wavdir.joinpath(wav), speaker_path)

        for tg in args.tgdir.glob(rf"{speaker}*.TextGrid"):
            shutil.copy(args.tgdir.joinpath(tg), speaker_path)

print("Done!")
