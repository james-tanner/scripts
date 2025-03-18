import re

from argparse import ArgumentParser
from pathlib import Path

from polyglotdb import CorpusContext
import polyglotdb.io as pgio

def get_phone_set(corpus):
    with CorpusContext(corpus) as c:
        q = c.query_lexicon(c.lexicon_phone)
        q = q.order_by(c.lexicon_phone.label)
        q = q.columns(c.lexicon_phone.label.column_name('phone'))
        phone_results = q.all()
        phone_set = [x.values[0] for x in phone_results]

        non_speech_set = ['<SIL>', 'sil', 'spn']
        vowel_regex = '^[AEOUI].[0-9]'
        vowel_set = [re.search(vowel_regex, p).string for p in phone_set
                    if re.search(vowel_regex, p) != None and p not in non_speech_set]
    return vowel_set

def encode_types(corpus, vowels, pause_labels, pause_length = 0.15):
    with CorpusContext(corpus) as c:

        if 'syllable' not in c.annotation_types:
            c.encode_type_subset('phone', vowels, 'vowel')
            c.encode_syllables(syllabic_label='vowel')

            c.encode_pauses(pause_labels)
            c.encode_utterances(min_pause_length = pause_length)
            c.encode_rate('utterance', 'syllable', 'speech_rate')
        else:
            print("Syllabics already encoded -- skipping")
    return None

def make_query(corpus):
    with CorpusContext(corpus) as c:
        q = c.query_graph(c.phone).filter(c.phone.subset == 'vowel')
        q = q.columns(c.phone.speaker.name.column_name('speaker'),
                      c.phone.discourse.name.column_name('file'),
                      c.phone.utterance.speech_rate.column_name('speech_rate'),
                      c.phone.word.label.column_name('word'),
                      c.phone.label.column_name('phone_label'),
                      c.phone.previous.label.column_name('previous_phone'),
                      c.phone.following.label.column_name('following_phone'),
                      c.phone.begin.column_name('phone_begin'),
                      c.phone.end.column_name('phone_end'),
                      c.phone.F1.column_name('F1'),
                      c.phone.F2.column_name('F2'),
                      c.phone.F3.column_name('F3'))
    return q

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("corpus_dir", type = Path)
    parser.add_argument("csv_path", type = Path)
    parser.add_argument("--reload", action = "store_true")
    parser.add_argument("--formants", action = "store_true")
    parser.add_argument("--praat-path", nargs = "?", default = "/usr/bin/praat")
    args = parser.parse_args()

    corpus = args.corpus_dir
    corpus_name = corpus.stem

    if args.reload:
        mfa = pgio.inspect_mfa(corpus)
        mfa.call_back = print
        with CorpusContext(corpus_name) as c:
            c.load(mfa, corpus)

    vowel_set = get_phone_set(corpus_name)
    encode_types(corpus_name, vowel_set, ["<SIL>"])
    
    if args.formants:
        print("Calculating formant points")
        with CorpusContext(corpus_name) as c:
            c.config.praat_path = args.praat_path
            c.analyze_formant_points(vowel_label='vowel', call_back=print)
    
    vowel_query = make_query(corpus_name)
    vowel_query.to_csv(str(args.csv_path))