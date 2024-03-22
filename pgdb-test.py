import polyglotdb.io as pgio

from argparse import ArgumentParser
from pathlib import Path
from polyglotdb import CorpusContext, CorpusConfig
from polyglotdb.exceptions import ParseError


parser = ArgumentParser()
parser.add_argument("corpus_path", type = Path)
args = parser.parse_args()

corpus = args.corpus_path
corpus_name = corpus.stem

pg_parser = pgio.inspect_labbcat(corpus)
pg_parser.callback = print


connection_params = {'host': 'localhost',
                    'graph_http_port': 7474}
config = CorpusConfig('corpus_name', **connection_params)

with CorpusContext(config) as c:
    try:
        c.load(pg_parser, corpus)
    except ParseError as e:
        print()
        pass

    q = c.query_graph(c.word).filter(c.word.label.in_(['are', 'is','am']))
    results = q.all()
    for r in results:
        print(r.label, r.begin)
