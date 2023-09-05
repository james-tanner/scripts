from argparse import ArgumentParser
from pathlib import Path
from pyjuliusalign import alignFromTextgrid
from textgrid import TextGrid, IntervalTier
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument("wavdir", type=Path)
parser.add_argument("tgdir", type=Path)
parser.add_argument("tempdir", type=Path)
args = parser.parse_args()

## prelimiaries: set paths
julius = "" ## path to julius segmentation-kit
sox = "sox"
cabocha = "cabocha"
perl = "perl"

print("Cleaning TextGrids...")
## get the list of TextGrids
tgList = list(args.tgdir.glob("M*.TextGrid"))

## Since the TextGrids are not correctly formatted,
## it's necessary to reformat them and save them to the 
for tg in tqdm(tgList):
    try:
        tgrid = TextGrid()
        tgrid = tgrid.fromFile(args.tgdir.joinpath(tg))

        ## SSC textgrids have two tiers:
        ## [speakername, comment]
        ## grab the speakername tier, which has the transcription
        textTier = tgrid.getList(tgrid.getNames()[0])[0]

        ## this tier has explicitly marked 'pz' intervals for pauses,
        ## which need to be dropped
        cleanIntervals = []
        for interval in textTier:
            if interval.mark == "pz":
                interval.mark = ""
            cleanIntervals.append(interval)

        ## create IntervalTier object and add intervals to it
        cleanTier = IntervalTier(
            name = "utterances",
            minTime = textTier.minTime,
            maxTime = textTier.maxTime,
        )
        
        for interval in cleanIntervals:
            cleanTier.addInterval(interval)
        
        ## make a new TextGrid object, add updated interval tier, and
        ## write to the to-align temp dir
        newTg = TextGrid(
            minTime = textTier.minTime,
            maxTime = textTier.maxTime
        )
        newTg.append(cleanTier)
        newTg.write(args.tempdir.joinpath(tg.name))

    except ValueError:
        pass

## generate the julius-interpretable transcription file
print("Generating transcriptions...")
alignFromTextgrid.textgridToCSV(
    inputPath = args.tempdir,
    outputPath = args.tempdir,
    outputExt = ".txt"
)

## convert transcriptions to kana
print("Converting transcriptions...")

cabocha_output = Path(args.tempdir.joinpath("cabocha_output"))
cabocha_output.mkdir(parents=True, exist_ok=True)

alignFromTextgrid.convertCorpusToKanaAndRomaji(
    inputPath = str(args.tempdir),
    outputPath = str(cabocha_output),
    cabochaEncoding = "euc-jp",
    cabochaPath = cabocha,
    encoding = "utf-8"
)