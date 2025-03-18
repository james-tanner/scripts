import re
import shutil

from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("wav_dir", type = Path)
    # parser.add_argument("tg_dir", type = Path)
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
    speakers_wavs_tups = [(speaker_regex.search(wav.stem).groups()[0], wav) for wav in wavs]
    speakers = set([speaker for speaker, _ in speakers_wavs_tups])

    for speaker in tqdm(speakers):
        speaker_dir = args.out_dir.joinpath(speaker)
        speaker_dir.mkdir(parents = True, exist_ok = True)

        for spk, wav in speakers_wavs_tups:
            if spk == speaker:
                shutil.copy(wav, speaker_dir)

    print("Done!")
