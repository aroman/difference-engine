## Simulator for Babbage's Difference Engine

This program is written in Python. It was written and tested against the latest stable version, 3.5, but it should work fine with any version >= 3.2.

To run the program, simply pass the `engine.py` file to your Python 3 interpreter, e.g. `python3 engine.py`. The specific interpreter alias is machine-dependent, and you'll need to know what it is for your machine.

### Basic usage

Follow the in-console prompts.

Example:

```
$ python3 engine.py
Difference Engine Simulator (degree = 8)
f(x): x^2 + 3x + 4
number of cranks: 3
Δ0: x^2 + 3x + 4
Δ1: 2x + 3
Δ2: 2
0   0   0   0   0   0   0   0
0   0   0   0   0   0   0   0
2   1   0   0   0   0   0   0
2   0   2   0   0   0   0   0
```

## Advanced use (embellishments)

### Polynomial input

As you've noticed from the basic usage section, you do not need to compute the
difference functions by hand to calculate the initial values -- you can just
type in the polynomial f(x) function by hand. The parser supports any
single-variable polynomial with no negative terms.

Valid input examples:

f(x): 8x^4 + x^2 + 2x + 19
f(x): 8t^4 + t^2 + 2t + 19 -> you need not use x, but they'll be treated as such
f(x): 8x4 + x2 + 2x + 19 -> carets may be omitted
f(x): x^18 -> only useful if you've increased the degree cap, see below
f(x): 100000

Invalid input examples:

f(x): hello -> only polynomials are supported
f(x): cos(x) -> only polynomials are supported
f(x): -10x^2 -> negative terms not supported
f(x): x^2 - 1 -> negative terms not supported

### Higher-degree polynomials (increased columns)

The engine supports arbitrary polynomials up to any degree. By default, it
only supports up to 8th-degree polynomials, as per the writeup. However, you can
set this limit to any integer you want, by passing that number as a command-line argument.

Example:

```
$ python3 engine.py 15
Difference Engine Simulator (degree = 15)
f(x): 8x4 + x2 + 2x + 19
number of cranks: 10
Δ0: 8x^4 + x^2 + 2x + 19
Δ1: 32x^3 + 48x^2 + 34x + 11
Δ2: 96x^2 + 192x + 114
Δ3: 192x + 288
Δ4: 192
0   7   1   2   0   0   0   0   0   0   0   0   0   0   0
1   1   6   2   1   0   0   0   0   0   0   0   0   0   0
3   5   3   0   9   0   0   0   0   0   0   0   0   0   0
9   1   4   8   2   0   0   0   0   0   0   0   0   0   0
```
