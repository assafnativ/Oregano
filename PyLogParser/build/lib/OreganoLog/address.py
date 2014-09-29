
from .parserAPI import CAddress
from .regIter import *
from .regValue import *
from .valueInTime import *

class Address(object):
    def __init__(self, cycle, address=None):
        if None==address:
            if isinstance(cycle, tuple):
                self.cycle, self.address = cycle
            elif isinstance(cycle, Address):
                self.address = cycle.address
                self.cycle   = cycle.cycle
            elif isinstance(cycle, (RegIter, RegValue, ValueInTime)):
                self.address = cycle.value
                self.cycle   = cycle.cycle
            elif isinstance(cycle, CAddress):
                self.address = cycle.addr
                self.cycle   = cycle.cycle
            else:
                raise TypeError('Need cycle & address')
        else:
            self.cycle   = cycle
            self.address = address
    def __repr__(self):
        return '{0:x}:{1:x}'.format(self.cycle, self.address)
    def __hex__(self):
        return '0x{0:x}:0x{1:x}'.format(self.cycle, self.address)
    def __str__(self):
        return '({0:d},{1:x})'.format(self.cycle, self.address)
    def __oct__(self):
        return '{0:d}:0{1:s}'.format(self.cycle, oct(self.address))
    def __int__(self):
        return self.address
    def __long__(self):
        return long(self.address)
    def __eq__(self, other):
        if isinstance(other, Address):
            return self.address == other.address
        return self.address == other
    def __ne__(self, other):
        if isinstance(other, Address):
            return self.address != other.address
        return self.address != other
    def __lt__(self, other):
        if isinstance(other, Address):
            return self.address < other.address
        return self.address < other
    def __le__(self, other):
        if isinstance(other, Address):
            return self.address <= other.address
        return self.address <= other
    def __gt__(self, other):
        if isinstance(other, Address):
            return self.address > other.address
        return self.address > other
    def __ge__(self, other):
        if isinstance(other, Address):
            return self.address >= other.address
        return self.address >= other
    def __add__(self, other):
        if isinstance(other, Address):
            return Address(self.cycle, self.address + other.address)
        return Address(self.cycle, self.address + other)
    def __sub__(self, other):
        if isinstance(other, Address):
            return Address(self.cycle, self.address - other.address)
        return Address(self.cycle, self.address - other)
    def __mul__(self, other):
        return Address(self.cycle, self.address * other)
    def __div__(self, other):
        return Address(self.cycle, self.address / other)
    def __mod__(self, other):
        return Address(self.cycle, self.address % other)
    def __divmod__(self, other):
        return Address(self.cycle, divmod(self.address, other))
    def __radd__(self, other):
        return Address(self.cycle, other + self.address)
    def __rsub__(self, other):
        return Address(self.cycle, other - self.address)
    def __rmul__(self, other):
        return Address(self.cycle, other * self.address)
    def __rdiv__(self, other):
        return Address(self.cycle, other / self.address)
    def __rmod__(self, other):
        return Address(self.cycle, other % self.address)
    def __rdivmod(self, other):
        return Address(self.cycle, divmod(other, self.address))
    def __and__(self, other):
        return Address(self.cycle, self.address & other)
    def __rand__(self, other):
        return Address(self.cycle, other & self.address)
    def __or__(self, other):
        return Address(self.cycle, self.address | other)
    def __ror__(self, other):
        return Address(self.cycle, other | self.address)
    def __xor__(self, other):
        return Address(self.cycle, self.address ^ other)
    def __rxor__(self, other):
        return Address(self.cycle, other ^ self.address)
    def __iadd__(self, other):
        if isinstance(other, Address):
            self.address += other.address
            self.cycle = max(self.cycle, other.cycle)
        else:
            self.address += other
    def __isub__(self, other):
        if isinstance(other, Address):
            self.address -= other.address
            self.cycle = max(self.cycle, other.cycle)
        else:
            self.address -= other
    def __imul__(self, other):
        self.address *= other
    def __idiv__(self, other):
        self.address /= other
    def __imod__(self, other):
        self.address %= other
    def __iand__(self, other):
        self.address &= other
    def __ior__(self, other):
        self.address |= other
    def __ixor__(self, other):
        self.address ^= other


