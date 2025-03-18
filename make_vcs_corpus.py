import re
import shutil

from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

def get_files(regex, wav, tg_dir):
    speaker_name = regex.search(wav.stem).groups()[0]
    tg = tg_dir.joinpath(wav.stem).with_suffix(".TextGrid")
    return (speaker_name, wav, tg)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("wav_dir", type = Path)
    parser.add_argument("tg_dir", type = Path)
    parser.add_argument("out_dir", type = Path)
    parser.add_argument("--clean", action = "store_true")
    args = parser.parse_args()

    args.out_dir.mkdir(parents = True, exist_ok = True)
    if args.clean:
        print("Cleaning output directory...")
        shutil.rmtree(args.out_dir)

    ## get list of wavs
    wavs = list(args.wav_dir.glob("*.wav"))

    ## determine the mapping between speakers and files
    speaker_regex = re.compile(r"Vcs_(.*)\_naming")
    speaker_wavs_tgs = [get_files(speaker_regex, wav, args.tg_dir) for wav in wavs]
    speakers = set([tup[0] for tup in speaker_wavs_tgs])

    for speaker in tqdm(speakers):
        speaker_dir = args.out_dir.joinpath(speaker)
        speaker_dir.mkdir(parents = True, exist_ok = True)

        for spk, wav, tg in speaker_wavs_tgs:
            if spk == speaker:
                shutil.copy(wav, speaker_dir)
                try:
                    shutil.copy(tg, speaker_dir)
                except FileNotFoundError:
                    pass

    print("Done!")
