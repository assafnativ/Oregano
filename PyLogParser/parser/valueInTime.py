
class ValueInTime(object):
    def __init__(self, cycle, value):
        self.cycle = cycle
        self.value = value
    def __repr__(self):
        return '{0:x}:{1:x}'.format(self.cycle, self.value)
    def __hex__(self):
        return hex(self.value)
    def __str__(self):
        return str(self.value)
    def __oct__(self):
        return oct(self.value)
    def __int__(self):
        return int(self.value)
    def __long__(self):
        return long(self.value)
    def __eq__(self, other):
        if isinstance(other, ValueInTime):
            return self.value == other.value
        return self.value == other
    def __ne__(self, other):
        if isinstance(other, ValueInTime):
            return self.value != other.value
        return self.value != other
    def __lt__(self, other):
        if isinstance(other, ValueInTime):
            return self.value < other.value
        return self.value < other
    def __le__(self, other):
        if isinstance(other, ValueInTime):
            return self.value <= other.value
        return self.value <= other
    def __gt__(self, other):
        if isinstance(other, ValueInTime):
            return self.value > other.value
        return self.value > other
    def __ge__(self, other):
        if isinstance(other, ValueInTime):
            return self.value >= other.value
        return self.value >= other
    def __add__(self, other):
        if isinstance(other, ValueInTime):
            return ValueInTime(max(self.cycle, other.cycle), self.value + other.value)
        return self.value + other
    def __sub__(self, other):
        if isinstance(other, ValueInTime):
            return ValueInTime(max(self.cycle, other.cycle), self.value - other.value)
        return self.value - other
    def __mul__(self, other):
        return ValueInTime(self.cycle, self.value * other)
    def __div__(self, other):
        return ValueInTime(self.cycle, self.value / other)
    def __mod__(self, other):
        return ValueInTime(self.cycle, self.value % other)
    def __divmod__(self, other):
        return ValueInTime(self.cycle, divmod(self.value, other))
    def __radd__(self, other):
        if isinstance(other, ValueInTime):
            return ValueInTime(max(self.cycle, other.cycle), other.value + self.value)
        return other + self.value
    def __rsub__(self, other):
        if isinstance(other, ValueInTime):
            return ValueInTime(max(self.cycle, other.cycle), other.value - self.value)
        return other - self.value
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
        if isinstance(other, ValueInTime):
            self.value += other.value
            self.cycle = max(self.cycle, other.cycle)
        else:
            self.value += other
    def __isub__(self, other):
        if isinstance(other, ValueInTime):
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
    def __lshift__(self, other):
        return self.value << other
    def __rshift__(self, other):
        return self.value >> other
    def __ilshift__(self, other):
        self.value <<= other
    def __irshift__(self, other):
        self.value >>= other




