# Copyright (C) Avi Romanoff <avi@romanoff.me>

import re
from sys import argv
from functools import partial, reduce
from itertools import repeat, chain, groupby
from math import factorial as fac
from collections import namedtuple

DEGREE = int(argv[1]) if (len(argv) > 1 and argv[1].isdigit()) else 8
flatten = lambda i: chain.from_iterable(i)
extend = lambda xs: (xs + [0] * DEGREE)[:DEGREE]
Term = namedtuple('PolynomialTerm', ['coefficient', 'exponent'])

def main():
    print('Difference Engine Simulator (degree = %i)' % DEGREE)
    terms = parsePolynomial(input('f(x): '))
    cranks = int(input('number of cranks: '))

    differences = list(map(partial(apply, difference, terms), range(DEGREE)))
    coefficients = list(map(partial(solve, 0), differences))

    # print difference functions
    for i, d in enumerate(filter(None, differences[1:]), start=1):
        d = sorted(d, key=lambda t: -t.exponent)
        print('Δ{}: {}'.format(i, ' + '.join(map(rep, d))))

    display(extend(apply(crank, coefficients, cranks)))

def rep(t):
    c = t.coefficient if t.coefficient > 1 else ''
    if t.exponent == 0: return '{}'.format(c)
    elif t.exponent == 1: return '{}x'.format(c)
    else: return '{}x^{}'.format(c, t.exponent)

def apply(f, x, n):
    for _ in range(n):
        x = f(x)
    return x

def simplify(ts):
    c = lambda t: t.coefficient
    e = lambda t: t.exponent
    combine = lambda a, b: Term(a.coefficient + b.coefficient, a.exponent)
    return list(filter(c,
        (reduce(combine, g) for _, g in groupby(sorted(ts, key=e), key=e))
    ))

def solve(x, ts):
    return sum(map(lambda t: t.coefficient * x ** t.exponent, ts))

# f(x) => f(x+1) - f(x)
def difference(ts):
    return simplify(chain(flatten(map(successorTerm, ts)), map(negate, ts)))

def negate(t):
    return Term(coefficient=-t.coefficient, exponent=t.exponent)

# f(x) => f(x+1)
def successorTerm(t):
    C = lambda n, k: round(fac(n) / (fac(k) * fac(n-k)))
    if t.exponent == 0: return (t,)
    if t.exponent == 1: return (t, Term(t.coefficient, 0))
    elif t.exponent > 1: return map(
        lambda z: Term(t.coefficient * C(z[0], z[1]), z[1]),
        zip(
            repeat(t.exponent, t.exponent + 1), # n
            range(t.exponent + 1) # k
        )
    )

def crank(values):
    pairs = zip(values, values[1:])
    return list(map(sum, zip(values, values[1:])))

def display(values, rows=4):
    digits = lambda i: list(map(int, reversed(str(i))))
    cols = [digits(v) for v in values]
    for row in reversed(range(rows)):
        for col in cols:
            print(col[row] if row < len(col) else '0', end='   ')
        print()

def parseTerm(s):
    if s.isdigit(): return Term(coefficient=int(s), exponent=0)
    matches = re.match('(\d*)\w?\^?(\d*)', s.strip())
    return Term(
        coefficient=int(matches.group(1) or 1),
        exponent=int(matches.group(2) or 1)
    )

def parsePolynomial(s):
    terms = map(parseTerm, [c.strip() for c in s.split('+')])
    return sorted(terms, key=lambda t: -t.exponent)

main()
