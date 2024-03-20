from argparse import ArgumentParser
from pathlib import Path
from textgrid import TextGrid, IntervalTier, Interval
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("input_dir", type = Path)
parser.add_argument("output_dir", type = Path)
args = parser.parse_args()

pauses = {
    "" : "",
    "spn" : "", 
}

vowels = {
    "a" : "a",
    "aː" : "aH",
    "e" : "e",
    "eː" : "eH",
    "i" : "i",
    "iː" : "iH",
    "i̥" : "I",
    "o" : "o",
    "oː" : "oH",
    "ɨ" : "u",
    "ɨː" : "uH",
    "ɨ̥" : "i",
    "ɯ" : "u",
    "ɯː" : "uH",
    "ɯ̥" : "U",
    "ɰ̃" : "u"
}

consonants = {
    "b" : "b",
    "bʲ" : "by",
    "bʲː" : "Qby",
    "bː" : "Qb",
    "c" : "k",
    "cː": "ky",
    "d" : "d",
    "dz" : "dZ",
    "dzː" : "QdZ",
    "dʑ" : "dZ",
    "dʑː" : "QdZ",
    "dʲ" : "dy",
    "dʲː": "Qdy",
    "dː": "Qd",
    "e" : "e",
    "eː" : "eH",
    "h" : "h",
    "hː" : "Qh",
    "j": "y",
    "k" : "k",
    "kː" : "Qk",
    "m" : "m",
    "mʲ" : "my",
    "mʲː" : "Qmy",
    "mː" : "Qm",
    "n" : "n",
    "nː" : "Qn",
    "p" : "p",
    "pʲ" : "py",
    "pʲː" : "Qpy",
    "pː" : "Qp",
    "s" : "s",
    "sː" : "Qs",
    "t" : "t",
    "ts" : " ts",
    "tsː" : "Qts",
    "tɕ" : "ts",
    "tɕː" : "Qts",
    "tʲ" : "ty",
    "tʲː" : "Qty",
    "tː" : "Qt",
    "v" : "v",
    "vʲ" : "vy",
    "w" : "w",
    "wː" : "Qw",
    "z" : "z",
    "ç" : "sh",
    "çː" : "Qsh",
    "ŋ" : "N",
    "ɕ" : "sh",
    "ɕː" : "Qsh",
    "ɟ" : "f",
    "ɟː" : "Qf",
    "ɡ" : "g",
    "ɡː" : "Qg",
    "ɲ" : "n",
    "ɲː" : "n",
    "ɴ" : "N",
    "ɴː" : "N",
    "ɸ" : "b",
    "ɸʲ" : "by",
    "ɸʲː" : "Qby",
    "ɸː" : "Qb",
    "ɾ" : "r",
    "ɾʲ" : "ry",
    "ɾʲː" : "Qry",
    "ɾː" : "Qr",
    "ʑ" : "z",
    "ʔ" : "Q"
}

## combine phone sets
mfa2julius_dict = pauses | vowels | consonants

def clean_phone(phone, nextPhone):
    julphone = mfa2julius_dict[phone]
    julnextphone = mfa2julius_dict[nextPhone]

    if julphone == "ry" and julnextphone == "i":
        outPhone = "r"
    elif julphone == "my" and julnextphone == "i":
        outPhone = "m"
    else:
        outPhone = julphone

    return outPhone


if __name__ == "__main__":
    speakers = args.input_dir.iterdir()

    ## make the output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)    

    for speaker in tqdm(list(speakers)):
        ## make a directory (inside out dir) for the speaker
        args.output_dir.joinpath(speaker.stem).mkdir(parents=True, exist_ok=True)

        for tgrid_path in speaker.glob("*.TextGrid"):

            tg = TextGrid().fromFile(tgrid_path)
            clean_tier = IntervalTier(name = "julius_phones")
            for i, phone in enumerate(tg.getList("phones")[0]):
                try:
                    phone_cleaned = clean_phone(phone.mark, tg.getList("phones")[0][i+1].mark)
                except IndexError:
                    phone_cleaned = mfa2julius_dict[phone.mark]
                clean_interval = Interval(minTime = phone.minTime, maxTime = phone.maxTime, mark = phone_cleaned)
                clean_tier.addInterval(clean_interval)
            tg.append(clean_tier)
            
            tg_out = args.output_dir.joinpath(speaker.stem).joinpath(tgrid_path.name)
            tg.write(tg_out)
