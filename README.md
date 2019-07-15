# Miscellanous scripts

In this repository is a collection of scripts I have created for various text and language processing tasks during my PhD research.

* `add_audioBNC_dialects.r` was used expand dialect codes used in the AudioBNC corpus (<http://www.phon.ox.ac.uk/AudioBNC>), and group them into larger linguistic macro regions based on *The Dialects of England* (Trudgill 2000).
* `clean_textgrids.py` removes punctuation from the word tier of the Sounts of the City corpus (<https://soundsofthecity.arts.gla.ac.uk/>).
* `parse_buckeye_words.py` was used to extract the underlying (force aligned) transcription from the Buckeye corpus (<https://buckeyecorpus.osu.edu/>). Since the alignment and transcription of the Buckeye corpus was manually adjusted after alignment, this code allows one to approximate the original force-aligned transcription (which may be more comparable with other available speech corpora).
* `replace_speaker_names.py` was used to anonymise the Modern RP corpus (Fabricus 2000) by iteratively replacing the speaker names on the TextGrid tiers with predefined speaker IDs.

### References

Fabricus, Anne. (2000). *T-glottalling between stigma and prestige: A sociolinguistic study of modern RP*. PhD thesis, Copenhagen Business School

Trudgill, Peter. (2000). *The Dialects of England*. Oxford: Blackwell
