'''Text Generator Usage: generate.py GRAMMAR [-n LINES] [-t | --tree]

Options:
    -h --help    show this
    -n LINES --number=LINES  number of lines to be generated [default: 1]
    -t --tree  generate a tree structure
'''
from collections import defaultdict
from docopt import docopt
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def expand(self, symbol, show):
        return '(%s %s)' % (symbol, self.gen(symbol, show)) if show else self.gen(symbol, show)

    def gen(self, symbol,show):
        expansion = self.random_expansion(symbol)
        return " ".join(s if self.is_terminal(s) else self.expand(s,show) for s in expansion)

    def random_sent(self, show=False):
        return self.expand("ROOT", show)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # print arguments
    pcfg = PCFG.from_file(arguments['GRAMMAR'])
    sentences = '\n'.join(pcfg.random_sent(arguments['--tree']) for i in range(0,int(arguments['--number'])))
    print sentences