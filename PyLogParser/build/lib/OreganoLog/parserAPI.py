
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64, c_void_p, c_char_p, Structure, cdll, POINTER
from os import sep as osSep

class CAddress(Structure):
    _fields_ = [
            ('addr',    c_void_p),
            ('cycle',   c_uint32) ]

class API(object):
    INVALID_CYCLE = 0xffffffffl
    INVALID_VALUE = 0xffffffffl
    UNKNOWN_QWORD = 0x3f3f3f3f3f3f3f3fl
    UNKNOWN_DWORD = 0x3f3f3f3fl
    UNKNOWN_WORD  = 0x3f3f
    UNKNOWN_BYTE  = 0x3f
    PROCESSOR_TYPE_x86      = 0
    PROCESSOR_TYPE_AMD64    = 1

    class Address( Structure ):
        _fields_ = [
                ('addr',    c_void_p),
                ('cycle',   c_uint32) ]

    class ByteInTime( Structure ):
        _fields_ = [
                ('addr',    c_void_p),
                ('cycle',   c_uint32),
                ('value',   c_uint8) ]

    def defineFunction(self, functionName, args, resType):
        target = getattr(self._logParserDll, functionName)
        target.args = args
        target.restype = resType
        setattr(self, functionName, target)

    def __init__(self, is32Bit):
        self.is32Bit = is32Bit
        dllPath = __file__.split(osSep)[:-1]
        if is32Bit:
            self._dllName = 'LogParserx86.dll'
        else:
            self._dllName = 'LogParserx64.dll'
        logParserDllFileName = osSep.join(dllPath + [self._dllName])
        self._logParserDll = cdll.LoadLibrary(logParserDllFileName)
        self.defineFunction('createLogParser',  [], c_void_p)
        self.defineFunction('parseLog',         [c_void_p, c_char_p], None)
        self.defineFunction('getLastCycle',     [c_void_p], c_uint32)
        self.defineFunction('getProcessorType', [c_void_p], c_uint32)

        self.defineFunction('getByte',          [c_void_p, c_uint32, c_uint32], c_uint8)
        self.defineFunction('getWord',          [c_void_p, c_uint32, c_uint32], c_uint16)
        self.defineFunction('getDword',         [c_void_p, c_uint32, c_uint32], c_uint32)
        self.defineFunction('getQword',         [c_void_p, c_uint32, c_uint32], c_uint64)
        self.defineFunction('deleteLogParserObject',                    [c_void_p], None)
        self.defineFunction('findCycleWithEipValue',                    [c_void_p, c_uint32, c_uint32, c_uint32], c_void_p)
        self.defineFunction('findCycleWithEipValueObjectNext',          [c_void_p], None)
        self.defineFunction('findCycleWithEipValueObjectCurrent',       [c_void_p], c_uint32)
        self.defineFunction('findCycleWithEipValueObjectRestartSearch', [c_void_p], None)
        self.defineFunction('findCycleWithEipValueDelete',              [c_void_p], None)
        self.defineFunction('findChangingCycles',                       [c_void_p, c_uint32, c_uint32, c_uint32], c_void_p)
        self.defineFunction('findChangingCyclesNext',                   [c_void_p], None)
        self.defineFunction('findChangingCyclesCurrent',                [c_void_p], c_uint32)
        self.defineFunction('findChangingCyclesRestartSearch',          [c_void_p], None)
        self.defineFunction('findChangingCyclesDelete',                 [c_void_p], None)
        self.defineFunction('findData',                                 [c_void_p, c_void_p, c_uint32, c_uint32, c_uint32], c_void_p)
        self.defineFunction('findDataNext',                             [c_void_p], None)
        self.defineFunction('findDataCurrent',                          [c_void_p], c_void_p)
        self.defineFunction('findDataRestartSearch',                    [c_void_p], None)
        self.defineFunction('findDataDelete',                           [c_void_p], None)
        self.defineFunction('regLogIter',                               [c_void_p, c_uint32, c_uint32], c_void_p)
        self.defineFunction('regLogIterGetValue',                       [c_void_p], c_uint32)
        self.defineFunction('regLogIterGetCycle',                       [c_void_p], c_uint32)
        self.defineFunction('regLogIterNext',                           [c_void_p], None)
        self.defineFunction('regLogIterPrev',                           [c_void_p], None)
        self.defineFunction('regLogIterIsLastCycle',                    [c_void_p], c_uint32)
        self.defineFunction('regLogIterDelete',                         [c_void_p], None)
        if self.is32Bit:
            self.defineFunction('getEip',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEdi',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEsi',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEbp',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEbx',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEdx',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEcx',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEax',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEflags',          [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getEsp',             [c_void_p, c_uint32], c_uint32)
            self.defineFunction('getThreadId',        [c_void_p, c_uint32], c_uint32)
            self.defineFunction('findEffectiveCycle', [c_void_p, c_uint32, c_uint32], c_uint32)
            self.defineFunction('getRegValue',        [c_void_p, c_uint32, c_uint32], c_uint32)
        else:
            self.defineFunction('getRip',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRdi',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRsi',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRbp',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRbx',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRdx',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRcx',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRax',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR8',     [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR9',     [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR10',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR11',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR12',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR13',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR14',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getR15',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRcs',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRflags', [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRsp',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRss',    [c_void_p, c_uint32], c_uint64)
            self.defineFunction('getRegValue',        [c_void_p, c_uint32, c_uint32], c_uint64)
        try:
            self.defineFunction('obtainPage', [c_void_p, c_uint32], c_void_p)
            self.defineFunction('obtainConsecutivePage', [c_void_p, c_uint32], c_void_p)
            self.defineFunction('releasePage', [c_void_p, c_uint32], None)
            self.defineFunction('statisticsEip', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEdi', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEsi', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEbp', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEbx', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEdx', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEcx', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEax', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEflags', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsEsp', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsThreadId', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('statisticsMemory', [c_void_p, c_void_p, c_void_p], None)
            self.defineFunction('getDataContainer', [c_void_p], c_void_p)
        except AttributeError, e:
            # No debug functions
            pass


