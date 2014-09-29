
from .parserAPI import API
from .regValue import *
from .valueInTime import *

class RegIter(object):
    def __init__(self, log, regId, cycle):
        # Assume that regId is valid
        self.startCycle = cycle
        self.regId = regId
        self._log = log
        self._ctx = API.regLogIter(self._log, regId, cycle)
        if None == self._ctx:
            raise Exception("Failed to create reg iter")
        self.cycle = API.regLogIterGetCycle(self._ctx)
        self.value = API.regLogIterGetValue(self._ctx)

    def __repr__(self):
        return 'Reg{0:x}_{1:x}:{2:x}'.format(self.regId, self.cycle, self.value)

    def next(self, steps=1, isVerbose=True):
        if 1 != steps:
            raise Exception("None single step are not implemented yet")
        API.regLogIterNext(self._ctx)
        self.cycle = API.regLogIterGetCycle(self._ctx)
        self.value = API.regLogIterGetValue(self._ctx)
        if API.INVALID_CYCLE == self.cycle:
            raise StopIteration()
        if isVerbose:
            print(self.__repr__())
        #return RegValue(self.cycle, self.value)

    def prev(self, steps=1, isVerbose=True):
        if 1 != steps:
            raise Exception("None single step are not implemented yet")
        API.regLogIterPrev(self._ctx)
        self.cycle = API.regLogIterGetCycle(self._ctx)
        self.value = API.regLogIterGetValue(self._ctx)
        if API.INVALID_CYCLE == self.cycle:
            raise StopIteration()
        if isVerbose:
            print(self.__repr__())
        #return RegValue(self.cycle, self.value)

    def __iter__(self):
        return self

    def __hex__(self):
        return '0x{0:x}:0x{1:x}'.format(self.cycle, self.value)
    def __str__(self):
        return '({0:d},{1:x})'.format(self.cycle, self.value)
    def __oct__(self):
        return '{0:d}:0{1:s}'.format(self.cycle, oct(self.value))
    def __int__(self):
        return self.value
    def __long__(self):
        return long(self.value)
    def __eq__(self, other):
        if isinstance(other, RegIter):
            return self.value == other.value
        return self.value == other
    def __ne__(self, other):
        if isinstance(other, RegIter):
            return self.value != other.value
        return self.value != other
    def __lt__(self, other):
        if isinstance(other, RegIter):
            return self.value < other.value
        return self.value < other
    def __le__(self, other):
        if isinstance(other, RegIter):
            return self.value <= other.value
        return self.value <= other
    def __gt__(self, other):
        if isinstance(other, RegIter):
            return self.value > other.value
        return self.value > other
    def __ge__(self, other):
        if isinstance(other, RegIter):
            return self.value >= other.value
        return self.value >= other

    def __add__(self, other):
        if isinstance(other, RegIter):
            return ValueInTime(self.cycle, self.value + other.value)
        return ValueInTime(self.cycle, self.value + other)
    def __sub__(self, other):
        if isinstance(other, RegIter):
            return ValueInTime(self.cycle, self.value - other.value)
        return ValueInTime(self.cycle, self.value - other)
    def __mul__(self, other):
        return ValueInTime(self.cycle, self.value * other)
    def __div__(self, other):
        return ValueInTime(self.cycle, self.value / other)
    def __mod__(self, other):
        return ValueInTime(self.cycle, self.value % other)
    def __divmod__(self, other):
        return ValueInTime(self.cycle, divmod(self.value, other))
    def __radd__(self, other):
        return ValueInTime(self.cycle, other + self.value)
    def __rsub__(self, other):
        return ValueInTime(self.cycle, other - self.value)
    def __rmul__(self, other):
        return ValueInTime(self.cycle, other * self.value)
    def __rdiv__(self, other):
        return ValueInTime(self.cycle, other / self.value)
    def __rmod__(self, other):
        return ValueInTime(self.cycle, other % self.value)
    def __rdivmod(self, other):
        return ValueInTime(self.cycle, divmod(other, self.value))
    def __and__(self, other):
        return ValueInTime(self.cycle, self.value & other)
    def __rand__(self, other):
        return ValueInTime(self.cycle, other & self.value)
    def __or__(self, other):
        return ValueInTime(self.cycle, self.value | other)
    def __ror__(self, other):
        return ValueInTime(self.cycle, other | self.value)
    def __xor__(self, other):
        return ValueInTime(self.cycle, self.value ^ other)
    def __rxor__(self, other):
        return ValueInTime(self.cycle, other ^ self.value)

    def __iadd__(self, other):
        if isinstance(other, RegIter):
            self.value += other.value
            self.cycle = max(self.cycle, other.cycle)
        else:
            self.value += other
    def __isub__(self, other):
        if isinstance(other, value):
            self.value -= other.value
            self.cycle = max(self.cycle, other.cycle)
        else:
            self.value -= other
    def __imul__(self, other):
        self.value *= other
    def __idiv__(self, other):
        self.value /= other
    def __imod__(self, other):
        self.value %= other
    def __iand__(self, other):
        self.value &= other
    def __ior__(self, other):
        self.value |= other
    def __ixor__(self, other):
        self.value ^= other
