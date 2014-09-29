
from .valueInTime import *

class RegValue(ValueInTime):
    def __repr__(self):
        return 'REG:{0:x}:{1:x}'.format(self.cycle, self.value)


