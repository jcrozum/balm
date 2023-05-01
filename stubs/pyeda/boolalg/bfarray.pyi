"""
This type stub file was generated by pyright.
"""

"""
The :mod:`pyeda.boolalg.bfarray` module implements multi-dimensional arrays
of Boolean functions.

Interface Functions:

* :func:`bddzeros` --- Return a multi-dimensional array of BDD zeros
* :func:`bddones` --- Return a multi-dimensional array of BDD ones
* :func:`bddvars` --- Return a multi-dimensional array of BDD variables

* :func:`exprzeros` --- Return a multi-dimensional array of expression zeros
* :func:`exprones` --- Return a multi-dimensional array of expression ones
* :func:`exprvars` --- Return a multi-dimensional array of expression variables

* :func:`ttzeros` --- Return a multi-dimensional array of truth table zeros
* :func:`ttones` --- Return a multi-dimensional array of truth table ones
* :func:`ttvars` --- Return a multi-dimensional array of truth table variables

* :func:`uint2bdds` --- Convert unsigned *num* to an array of BDDs
* :func:`uint2exprs` --- Convert unsigned *num* to an array of expressions
* :func:`uint2tts` --- Convert unsigned *num* to an array of truth tables
* :func:`int2bdds` --- Convert *num* to an array of BDDs
* :func:`int2exprs` --- Convert *num* to an array of expressions
* :func:`int2tts` --- Convert *num* to an array of truth tables

* :func:`fcat` --- Concatenate a sequence of farrays

Interface Classes:

* :func:`farray`
"""
_VAR = ...
def bddzeros(*dims): # -> farray:
    """Return a multi-dimensional array of BDD zeros.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of BDD zeros::

       >>> zeros = bddzeros(4, 4)
       >>> zeros
       farray([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]])
    """
    ...

def bddones(*dims): # -> farray:
    """Return a multi-dimensional array of BDD ones.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of BDD ones::

       >>> ones = bddones(4, 4)
       >>> ones
       farray([[1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1]])
    """
    ...

def bddvars(name, *dims): # -> farray:
    """Return a multi-dimensional array of BDD variables.

    The *name* argument is passed directly to the
    :func:`pyeda.boolalg.bdd.bddvar` function,
    and may be either a ``str`` or tuple of ``str``.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of BDD variables::

       >>> vs = bddvars('a', 4, 4)
       >>> vs
       farray([[a[0,0], a[0,1], a[0,2], a[0,3]],
               [a[1,0], a[1,1], a[1,2], a[1,3]],
               [a[2,0], a[2,1], a[2,2], a[2,3]],
               [a[3,0], a[3,1], a[3,2], a[3,3]]])
    """
    ...

def exprzeros(*dims): # -> farray:
    """Return a multi-dimensional array of expression zeros.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of expression zeros::

       >>> zeros = exprzeros(4, 4)
       >>> zeros
       farray([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]])
    """
    ...

def exprones(*dims): # -> farray:
    """Return a multi-dimensional array of expression ones.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of expression ones::

       >>> ones = exprones(4, 4)
       >>> ones
       farray([[1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1]])
    """
    ...

def exprvars(name, *dims): # -> farray:
    """Return a multi-dimensional array of expression variables.

    The *name* argument is passed directly to the
    :func:`pyeda.boolalg.expr.exprvar` function,
    and may be either a ``str`` or tuple of ``str``.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of expression variables::

       >>> vs = exprvars('a', 4, 4)
       >>> vs
       farray([[a[0,0], a[0,1], a[0,2], a[0,3]],
               [a[1,0], a[1,1], a[1,2], a[1,3]],
               [a[2,0], a[2,1], a[2,2], a[2,3]],
               [a[3,0], a[3,1], a[3,2], a[3,3]]])
    """
    ...

def ttzeros(*dims): # -> farray:
    """Return a multi-dimensional array of truth table zeros.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of truth table zeros::

       >>> zeros = ttzeros(4, 4)
       >>> zeros
       farray([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]])
    """
    ...

def ttones(*dims): # -> farray:
    """Return a multi-dimensional array of truth table ones.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of truth table ones::

       >>> ones = ttones(4, 4)
       >>> ones
       farray([[1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1],
               [1, 1, 1, 1]])
    """
    ...

def ttvars(name, *dims): # -> farray:
    """Return a multi-dimensional array of truth table variables.

    The *name* argument is passed directly to the
    :func:`pyeda.boolalg.table.ttvar` function,
    and may be either a ``str`` or tuple of ``str``.

    The variadic *dims* input is a sequence of dimension specs.
    A dimension spec is a two-tuple: (start index, stop index).
    If a dimension is given as a single ``int``,
    it will be converted to ``(0, stop)``.

    The dimension starts at index ``start``,
    and increments by one up to, but not including, ``stop``.
    This follows the Python slice convention.

    For example, to create a 4x4 array of truth table variables::

       >>> vs = ttvars('a', 4, 4)
       >>> vs
       farray([[a[0,0], a[0,1], a[0,2], a[0,3]],
               [a[1,0], a[1,1], a[1,2], a[1,3]],
               [a[2,0], a[2,1], a[2,2], a[2,3]],
               [a[3,0], a[3,1], a[3,2], a[3,3]]])
    """
    ...

def uint2bdds(num, length=...): # -> farray:
    """Convert unsigned *num* to an array of BDDs.

    The *num* argument is a non-negative integer.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be zero-extended to match *length*.

    For example, to convert the byte 42 (binary ``0b00101010``)::

       >>> uint2bdds(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
    """
    ...

def uint2exprs(num, length=...): # -> farray:
    """Convert unsigned *num* to an array of expressions.

    The *num* argument is a non-negative integer.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be zero-extended to match *length*.

    For example, to convert the byte 42 (binary ``0b00101010``)::

       >>> uint2exprs(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
    """
    ...

def uint2tts(num, length=...): # -> farray:
    """Convert unsigned *num* to an array of truth tables.

    The *num* argument is a non-negative integer.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be zero-extended to match *length*.

    For example, to convert the byte 42 (binary ``0b00101010``)::

       >>> uint2tts(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
    """
    ...

def int2bdds(num, length=...): # -> farray:
    """Convert *num* to an array of BDDs.

    The *num* argument is an ``int``.
    Negative numbers will be converted using twos-complement notation.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be sign-extended to match *length*.

    For example, to convert the bytes 42 (binary ``0b00101010``),
    and -42 (binary ``0b11010110``)::

       >>> int2bdds(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
       >>> int2bdds(-42, 8)
       farray([0, 1, 1, 0, 1, 0, 1, 1])
    """
    ...

def int2exprs(num, length=...): # -> farray:
    """Convert *num* to an array of expressions.

    The *num* argument is an ``int``.
    Negative numbers will be converted using twos-complement notation.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be sign-extended to match *length*.

    For example, to convert the bytes 42 (binary ``0b00101010``),
    and -42 (binary ``0b11010110``)::

       >>> int2exprs(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
       >>> int2exprs(-42, 8)
       farray([0, 1, 1, 0, 1, 0, 1, 1])
    """
    ...

def int2tts(num, length=...): # -> farray:
    """Convert *num* to an array of truth tables.

    The *num* argument is an ``int``.
    Negative numbers will be converted using twos-complement notation.

    If no *length* parameter is given,
    the return value will have the minimal required length.
    Otherwise, the return value will be sign-extended to match *length*.

    For example, to convert the bytes 42 (binary ``0b00101010``),
    and -42 (binary ``0b11010110``)::

       >>> int2tts(42, 8)
       farray([0, 1, 0, 1, 0, 1, 0, 0])
       >>> int2tts(-42, 8)
       farray([0, 1, 1, 0, 1, 0, 1, 1])
    """
    ...

def fcat(*fs): # -> farray:
    """Concatenate a sequence of farrays.

    The variadic *fs* input is a homogeneous sequence of functions or arrays.
    """
    ...

class farray:
    """Multi-dimensional array of Boolean functions

    The *objs* argument is a nested sequence of homogeneous Boolean functions.
    That is, both [a, b, c, d] and [[a, b], [c, d]] are valid inputs.

    The optional *shape* parameter is a tuple of dimension specs,
    which are ``(int, int)`` tuples.
    It must match the volume of *objs*.
    The shape can always be automatically determined from *objs*,
    but you can supply it to automatically reshape a flat input.

    The optional *ftype* parameter is a proper subclass of ``Function``.
    It must match the homogeneous type of *objs*.
    In most cases, *ftype* can automatically be determined from *objs*.
    The one exception is that you must provide *ftype* for ``objs=[]``
    (an empty array).
    """
    def __init__(self, objs, shape=..., ftype=...) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __iter__(self): # -> Generator[Unknown | farray, None, None]:
        ...
    
    def __len__(self): # -> int:
        ...
    
    def __getitem__(self, key): # -> farray:
        ...
    
    def __setitem__(self, key, item): # -> None:
        ...
    
    def __invert__(self): # -> farray:
        """Bit-wise NOT operator"""
        ...
    
    def __or__(self, other): # -> farray:
        """Bit-wise OR operator"""
        ...
    
    def __and__(self, other): # -> farray:
        """Bit-wise AND operator"""
        ...
    
    def __xor__(self, other): # -> farray:
        """Bit-wise XOR operator"""
        ...
    
    def __lshift__(self, obj): # -> Self@farray | farray:
        """Left shift operator

        The *obj* argument may either be an ``int``, or ``(int, farray)``.
        The ``int`` argument is *num*, and the ``farray`` argument is *cin*.

        .. seealso:: :meth:`lsh`
        """
        ...
    
    def __rshift__(self, obj): # -> Self@farray | farray:
        """Right shift operator

        The *obj* argument may either be an ``int``, or ``(int, farray)``.
        The ``int`` argument is *num*, and the ``farray`` argument is *cin*.

        .. seealso:: :meth:`rsh`
        """
        ...
    
    def __add__(self, other): # -> farray:
        """Concatenation operator

        The *other* argument may be a Function or farray.
        """
        ...
    
    def __radd__(self, other): # -> farray:
        ...
    
    def __mul__(self, num): # -> farray:
        """Repetition operator"""
        ...
    
    def __rmul__(self, num): # -> farray:
        ...
    
    def restrict(self, point): # -> farray:
        """Apply the ``restrict`` method to all functions.

        Returns a new farray.
        """
        ...
    
    def vrestrict(self, vpoint): # -> farray:
        """Expand all vectors in *vpoint* before applying ``restrict``."""
        ...
    
    def compose(self, mapping): # -> farray:
        """Apply the ``compose`` method to all functions.

        Returns a new farray.
        """
        ...
    
    @property
    def size(self): # -> int:
        """Return the size of the array.

        The *size* of a multi-dimensional array is the product of the sizes
        of its dimensions.
        """
        ...
    
    @property
    def offsets(self): # -> tuple[Unknown | Literal[0], ...]:
        """Return a tuple of dimension offsets."""
        ...
    
    @property
    def ndim(self): # -> int:
        """Return the number of dimensions."""
        ...
    
    def reshape(self, *dims): # -> farray:
        """Return an equivalent farray with a modified shape."""
        ...
    
    @property
    def flat(self): # -> Generator[Unknown, None, None]:
        """Return a 1D iterator over the farray."""
        ...
    
    def to_uint(self): # -> int:
        """Convert vector to an unsigned integer, if possible.

        This is only useful for arrays filled with zero/one entries.
        """
        ...
    
    def to_int(self): # -> int:
        """Convert vector to an integer, if possible.

        This is only useful for arrays filled with zero/one entries.
        """
        ...
    
    def zext(self, num): # -> farray:
        """Zero-extend this farray by *num* bits.

        Returns a new farray.
        """
        ...
    
    def sext(self, num): # -> farray:
        """Sign-extend this farray by *num* bits.

        Returns a new farray.
        """
        ...
    
    def uor(self): # -> Any:
        """Unary OR reduction operator"""
        ...
    
    def unor(self): # -> Any:
        """Unary NOR reduction operator"""
        ...
    
    def uand(self): # -> Any:
        """Unary AND reduction operator"""
        ...
    
    def unand(self): # -> Any:
        """Unary NAND reduction operator"""
        ...
    
    def uxor(self): # -> Any:
        """Unary XOR reduction operator"""
        ...
    
    def uxnor(self): # -> Any:
        """Unary XNOR reduction operator"""
        ...
    
    def lsh(self, num, cin=...): # -> tuple[Self@farray, farray] | tuple[farray, farray]:
        """Left shift the farray by *num* places.

        The *num* argument must be a non-negative ``int``.

        If the *cin* farray is provided, it will be shifted in.
        Otherwise, the carry-in is zero.

        Returns a two-tuple (farray fs, farray cout),
        where *fs* is the shifted vector, and *cout* is the "carry out".

        Returns a new farray.
        """
        ...
    
    def rsh(self, num, cin=...): # -> tuple[Self@farray, farray] | tuple[farray, farray]:
        """Right shift the farray by *num* places.

        The *num* argument must be a non-negative ``int``.

        If the *cin* farray is provided, it will be shifted in.
        Otherwise, the carry-in is zero.

        Returns a two-tuple (farray fs, farray cout),
        where *fs* is the shifted vector, and *cout* is the "carry out".

        Returns a new farray.
        """
        ...
    
    def arsh(self, num): # -> tuple[Self@farray, farray] | tuple[farray, farray]:
        """Arithmetically right shift the farray by *num* places.

        The *num* argument must be a non-negative ``int``.

        The carry-in will be the value of the most significant bit.

        Returns a new farray.
        """
        ...
    
    def decode(self): # -> farray:
        r"""Return a :math:`N \rightarrow 2^N` decoder.

        Example Truth Table for a 2:4 decoder:

        .. csv-table::
           :header: :math:`A_1`, :math:`A_0`, \
                    :math:`D_3`, :math:`D_2`, :math:`D_1`, :math:`D_0`
           :stub-columns: 2

           0, 0, 0, 0, 0, 1
           0, 1, 0, 0, 1, 0
           1, 0, 0, 1, 0, 0
           1, 1, 1, 0, 0, 0
        """
        ...
    

