#!/usr/bin/env python

## Autobk (XAFS background subtraction) in pure Python,
## using Python code from Larch.
from larch import Interpreter, enable_plugins
enable_plugins()

from pre_edge import pre_edge
from autobk import autobk
from columnfile import _read_ascii

_larch = Interpreter()

fname = '../xafsdata/cu_rt01.xmu'

cu = _read_ascii(fname, labels='energy mu i0', _larch=_larch)
print 'Read ASCII File:', cu
print dir(cu)

pre_edge(cu, _larch=_larch)
print 'After pre-edge:'
print dir(cu)

autobk(cu, rbkg=1.0, kweight=1, _larch=_larch)

print 'After autobk:'
print dir(cu)
