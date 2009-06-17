#!/usr/bin/env python2.6
from fractions import Fraction
from itertools import izip
from pympfr import pympfr, GMP_RNDN, GMP_RNDU, GMP_RNDD

def semiconvergents(x):
    """Semiconvergents of continued fraction expansion of a Fraction x."""

    (q, n), d = divmod(x.numerator, x.denominator), x.denominator
    yield Fraction(q)
    p0, q0, p1, q1 = 1, 0, q, 1
    while n:
        (q, n), d = divmod(d, n), n
        for _ in xrange(q):
            p0, q0 = p0+p1, q0+q1
            yield Fraction(p0, q0)
        p0, q0, p1, q1 = p1, q1, p0, q0

def logn2(n, p):
    """Best p-bit lower and upper bounds for log(2)/log(n), as Fractions."""

    down, up = RoundTowardNegative, RoundTowardPositive

    extra = 10
    while True:
        with precision(p+extra):
            with rounding(up):
                log2upper = log2(n)
            with rounding(down):
                log2lower = log2(n)

        with rounding(down):
            lower = 1/log2upper
        with rounding(up):
            upper = 1/log2lower




    with rounding(down):
        with precision(p+extra):
            log2lower = log2(n)

 upper = log2(n)
    with rounding(up): upper = 1/upper


    lower, upper, lower_copy = map(pympfr, [p]*3)
    y = pympfr(p + 10)
    one = pympfr()
    one.set_d(1.0, GMP_RNDN)
    # convert n to a pympfr instance
    fn = pympfr()
    if fn.set_d(n, GMP_RNDN):
        raise ValueError("Default precision too low to represent n exactly.")
    n = fn

    while True:
        # get lower and upper bounds for log(2)/log(n) ( = 1/log2(n))
        y.log2(n, GMP_RNDU)
        lower.div(one, y, GMP_RNDD)
        y.log2(n, GMP_RNDD)
        upper.div(one, y, GMP_RNDU)

        # if the two bounds are adjacent (or equal), we're done
        lower_copy.set(lower, GMP_RNDN)
        lower_copy.nexttoward(upper)
        if lower_copy == upper:
            return (Fraction(*lower.as_integer_ratio()),
                    Fraction(*upper.as_integer_ratio()))

        # otherwise, increase the precision and try again
        y.precision += 10

marks_results = {}
all_n = [n for n in xrange(3, 63) if n & (n-1)]
for n in all_n:
    # 76-bit upper approximation used for the computation of m
    approx = logn2(n, 76)[1]
    # Find first semiconvergent s s.t. log(2)/log(n) < s < approx.  To
    # get semiconvergents of log(2)/log(n), get lower and upper bounds,
    # find semiconvergents of those, then use the matching initial portions
    # of the two lists.
    l, u = logn2(n, 100)  # 100 seems to be big enough
    for lc, uc in izip(semiconvergents(l), semiconvergents(u)):
        if lc != uc: raise RuntimeError("not enough semiconvergents")
        if u <= lc < approx:
            marks_results[n] = lc.denominator
            break

# from http://websympa.loria.fr/wwsympa/arc/mpfr/2009-06/msg00034.html:
check_values = r"""
3,  975675645481  & 21, 500866275153  & 37, 1412595553751 & 52, 4234025992181\\
5,  751072483167  & 22, 1148143737877 & 38, 2296403499681 & 53, 1114714558973\\
6,  880248760192  & 23, 2963487537029 & 39, 227010038198  & 54, 653230957562 \\
7,  186564318007  & 24, 930741237529  & 40, 3574908346547 & 55, 1113846215983\\
9,  1951351290962 & 25, 751072483167  & 41, 458909109357  & 56, 385930970803 \\
10, 1074541795081 & 26, 1973399062219 & 42, 1385773590791 & 57, 676124411642 \\
11, 890679595344  & 27, 1193652440098 & 43, 945885487008  & 58, 330079387370 \\
12, 727742578896  & 28, 319475419871  & 44, 1405607880410 & 59, 276902299279 \\
13, 1553566199646 & 29, 1645653531910 & 45, 421759749499  & 60, 2304608467893\\
14, 253019868939  & 30, 1190119072066 & 46, 376795094250  & 61, 1364503143363\\
15, 947578699731  & 31, 2605117443408 & 47, 1352868311988 & 62, 414481628603 \\
17, 628204683310  & 33, 1138749817330 & 48, 1133739896162 \\
18, 2280193268258 & 34, 1611724268329 & 49, 186564318007  \\
19, 2290706306707 & 35, 820222240621  & 50, 842842574535  \\
20, 645428387961  & 36, 1760497520384 & 51, 1435927298893 \\
"""

pauls_results = dict(map(int, piece.split(','))
                     for line in check_values.rstrip('\\\n').split(r'\\')
                     for piece in line.split('&'))

for b, n in sorted(marks_results.items()):
    print b, n
print "Results match Paul Zimmerman's: ", marks_results == pauls_results
