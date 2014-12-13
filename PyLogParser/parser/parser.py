
import struct
import io
import time
import sys

import distorm3

from NativDebugging.Utile import *
from NativDebugging.MemReaderBase import *
from NativDebugging.DebuggerBase import *
from NativDebugging.GUIDisplayBase import *
from .parserAPI import API
from .parserDefines import *
from .address import *
from .regValue import *
from .regIter import *
from .valueInTime import *
from .breakPoint import *
from .moduleInfo import *

def parseLog(fileName, timeIt=False, maxCycle=0x7fffffff, isVerbose=False):
    if timeIt:
        startTime = time.time()
    log = Log(fileName, maxCycle=maxCycle, isVerbose=isVerbose)
    if timeIt:
        print("It took {0:d} seconds to parse the file".format(int(time.time() - startTime)))
    return log

class Log(MemReaderBase, DebuggerBase, GUIDisplayBase):
    def __init__(self, logFile=None, maxCycle=0x7fffffff, isVerbose=False):
        self._is64Bit = '64 bit' in sys.version
        self.API = API(not self._is64Bit)
        self.DEFAULT_DATA_SIZE = 4
        MemReaderBase.__init__(self)
        self.isVerbose = isVerbose
        # Set the debugger interface
        DebuggerBase.__init__(self)
        class DisassemblerWrapper(object):
            def __init__(wrapper, log):
                wrapper._log = log
            def __call__(wrapper, addr=None, lines=None):
                wrapper._log.disassemble(addr, lines)
            def __repr__(wrapper):
                return wrapper._log._disassemble()
        self.u = DisassemblerWrapper(self)
        class SingleStepWrapper(object):
            def __init__(wrapper, log):
                wrapper._log = log
            def __repr__(wrapper):
                wrapper._log.singleStep(isVerbose=False)
                return wrapper._log._contextShow()
        self.t = SingleStepWrapper(self)
        self._breakpoints = {}
        self._log = self.API.createLogParser()
        if None == self._log:
            raise Exception("Failed to create log parser")
        if None != logFile:
            self.parseLog(logFile, maxCycle=maxCycle)

    def __del__(self):
        self.API.deleteLogParserObject(self._log)
        self._log = None

    def __repr__(self):
        result = self._contextShow()
        result += '\nLast cycle: {0:08X}\n'.format(self.lastCycle, )
        return result

    def _printIfVerbose(self, text):
        if self.isVerbose:
            print(text)

    def attach(self, logFile, maxCycle=0x7fffffff):
        return self.parseLog(logFile, maxCycle=maxCycle)

    def detach(self):
        del self

    def parseLog(self, logFile, maxCycle=0x7fffffff):
        self.API.parseLog(self._log, logFile, maxCycle)
        self._processor = self.API.getProcessorType(self._log)
        if self.API.PROCESSOR_TYPE_x86 == self._processor:
            self.POINTER_SIZE = 4
        elif self.API.PROCESSOR_TYPE_AMD64 == self._processor:
            self.POINTER_SIZE = 8
        else:
            raise Exception("Unknown CPU type")
        self.lastCycle = self.API.getLastCycle(self._log)
        self.cycle = self.lastCycle

    def setCycle(self, cycle):
        """
        Set the current context
        Use -1 to set to lastCycle
        """
        if not isinstance(cycle, (int, long)):
            cycle = cycle.cycle
        if -1 == cycle:
            cycle = self.lastCycle
        self.cycle = cycle
    
    def _contextShow(self, cycle=None):
        cycle = self._getCycleFromObj(cycle)
        if self.API.PROCESSOR_TYPE_x86 == self._processor:
            output = '\n' +\
                     'EAX {0:08X}\tECX {1:08X}\tEDX {2:08X}\tEBX {3:08X}\n' +\
                     'EDI {4:08X}\tESI {5:08X}\tEBP {6:08X}\tEIP {7:08X}\n' +\
                     'EFlags {8:08X}\tESP {9:08X}\n' +\
                     'Thread: {10:08X}\tCycle: {11:08X}'
            output = output.format( \
                    self._getRegValueOnly(REG_ID_EAX, cycle), \
                    self._getRegValueOnly(REG_ID_ECX, cycle), \
                    self._getRegValueOnly(REG_ID_EDX, cycle), \
                    self._getRegValueOnly(REG_ID_EBX, cycle), \
                    self._getRegValueOnly(REG_ID_EDI, cycle), \
                    self._getRegValueOnly(REG_ID_ESI, cycle), \
                    self._getRegValueOnly(REG_ID_EBP, cycle), \
                    self._getRegValueOnly(REG_ID_EIP, cycle), \
                    self._getRegValueOnly(REG_ID_EFLAGS, cycle), \
                    self._getRegValueOnly(REG_ID_ESP, cycle), \
                    self._getRegValueOnly(THREAD_ID, cycle), \
                    cycle )
            return output
        elif self.API.PROCESSOR_TYPE_AMD64 == self._processor:
            raise Exception("Not implemented yet")

    def contextShow(self, cycle=None):
        print self._contextShow(cycle=cycle)

    def breakpointRemove(self, index):
        if '*' == index:
            self._breakpoints = {}
        elif index in self._breakpoints.keys():
            del(self._breakpoints[index])

    def breakpointSetState(self, index, state):
        if '*' == index:
            for index in self._breakpoints.keys():
                self._breakpoints[index].isEnabled = state
        elif index in self._breakpoints.keys():
            self._breakpoints[index].isEnabled = state

    def breakpointDisable(self, index):
        self.breakpointSetState(index, False)

    def breakpointEnable(self, index):
        self.breakpointSetState(index, True)

    def breakpointSet(self, addr):
        for index in range(0x1000):
            if index not in self._breakpoints:
                break
        else:
            raise Exception("Too many breakpoints")
        self._breakpoints[index] = BreakPoint(addr)

    def breakpointsList(self):
        output = ''
        for index, breakPoint in self._breakpoints.iteritems():
            output += str(index)
            output += repr(breakPoint)
            output += '\n'
        return output

    def run(self):
        self._runInDirection(True)

    def runBack(self):
        self._runInDirection(False)

    def _runInDirection(self, isForward=True):
        breakPoints = []
        breakPoints.append(BreakPoint(0))
        breakPoints.append(BreakPoint(self.lastCycle))
        for breakPoint in self._breakpoints:
            if breakPoint.isEnabled:
                breakPoints.append(breakPoint.addr)
        while True:
            if isForward:
                self.singleStep(isVerbose=False)
            else:
                self.singleStepBack(isVerbose=False)
            if self.eip() in breakPoints:
                for key in self._breakpoints.keys():
                    if self.eip() == self._breakpoints[key].addr:
                        return key
                return None

    def singleStep(self, isVerbose=True):
        if self.cycle < self.lastCycle:
            self.cycle += 1
        if isVerbose:
            self.contextShow()

    def singleStepBack(self, isVerbose=True):
        if self.cycle > 0:
            self.cycle -= 1
        if isVerbose:
            self.contextShow()

    def step(self, numCycles):
        newCycle = self.cycle + numCycles
        if newCycle < 0:
            self.cycle = 0
        if newCycle >= self.lastCycle:
            self.cycle = self.lastCycle - 1

    def _getRegValueOnly(self, regId, cycle):
        cycle = self._getCycleFromObj(cycle)
        value = self.API.getRegValue(self._log, regId, cycle)
        return value

    def _getRegValue(self, regId, cycle):
        # Assume regId is valid
        cycle = self._getCycleFromObj(cycle)
        return RegIter(self, regId, cycle)

    def getRegValue(self, regId, cycle=None):
        if REG_ID_EIP > regId or NUMBER_OF_REGS <= regId:
            return None
        return _getRegValue(regId, cycle)

    def _thread(self, cycle):
        return self._getRegValueOnly(THREAD_ID, cycle)
        
    def thread(self, cycle=None):
        cycle = self._getCycleFromObj(cycle)
        return RegIter(self, self.threadId, cycle)

    def eip(self, cycle=None):
        return self._getRegValue(REG_ID_EIP, cycle)
    def edi(self, cycle=None):
        return self._getRegValue(REG_ID_EDI, cycle)
    def esi(self, cycle=None):
        return self._getRegValue(REG_ID_ESI, cycle)
    def ebp(self, cycle=None):
        return self._getRegValue(REG_ID_EBP, cycle)
    def ebx(self, cycle=None):
        return self._getRegValue(REG_ID_EBX, cycle)
    def edx(self, cycle=None):
        return self._getRegValue(REG_ID_EDX, cycle)
    def ecx(self, cycle=None):
        return self._getRegValue(REG_ID_ECX, cycle)
    def eax(self, cycle=None):
        return self._getRegValue(REG_ID_EAX, cycle)
    def eflags(self, cycle=None):
        return self._getRegValue(REG_ID_EFLAGS, cycle)
    def esp(self, cycle=None):
        return self._getRegValue(REG_ID_ESP, cycle)

    def findChangingCycles(self, addr, startCycle=0, endCycle=None):
        if None == endCycle:
            endCycle = self.API.INVALID_CYCLE
        else:
            endCycle = self._getCycleFromObj(endCycle)
        startCycle = self._getCycleFromObj(startCycle)
        addr = self._getValFromObj(addr)
        ctx = self.API.findChangingCycles(self._log, addr, startCycle, endCycle)
        val = self.API.findChangingCyclesCurrent(ctx)
        while val < endCycle and self.API.INVALID_CYCLE != val:
            yield val
            self.API.findChangingCyclesNext(ctx)
            val = self.API.findChangingCyclesCurrent(ctx)
        self.API.findChangingCyclesDelete(ctx)

    def getAllChangingCycles(self, addr, startCycle=0, endCycle=None):
        return [self.eip(x) for x in self.findChangingCycles(addr, startCycle, endCycle)]

    def searchForData(self, data, startCycle=0, endCycle=None):
        if None == endCycle:
            endCycle = self.API.INVALID_CYCLE
        ctx = self.API.findData( self._log, data, len(data), startCycle, endCycle )
        itemPtr = self.API.findDataCurrent(ctx)
        while None != itemPtr:
            item = self.API.Address.from_address(itemPtr)
            if self.API.INVALID_CYCLE == item.cycle:
                break
            yield Address(item.cycle, item.addr)
            self.API.findDataNext(ctx)
            itemPtr = self.API.findDataCurrent(ctx)
        self.API.findDataDelete(ctx)

    def findNextCycleWithEipValue(self, targetEip, startCycle=None, endCycle=None):
        if None == endCycle:
            endCycle = self.lastCycle
        else:
            endCycle = self._getCycleFromObj(endCycle)
        startCycle = self._getCycleFromObj(startCycle)
        ctx = self.API.findCycleWithEipValue(self._log, targetEip, startCycle, endCycle)
        result = self.API.findCycleWithEipValueObjectCurrent(ctx)
        while result != self.API.INVALID_CYCLE:
            yield result
            self.API.findCycleWithEipValueObjectNext(ctx)
            result = self.API.findCycleWithEipValueObjectCurrent(ctx)
        self.API.findCycleWithEipValueDelete(ctx)

    def findPrevCycleWithEipValue(self, targetEip, startCycle=None, endCycle=0):
        if None == startCycle:
            startCycle = self.cycle
        else:
            startCycle = self._getCycleFromObj(startCycle)
        endCycle = self._getCycleFromObj(endCycle)
        ctx = self.API.findCycleWithEipValueReverse(self._log, targetEip, startCycle, endCycle)
        result = self.API.findCycleWithEipValueObjectCurrent(ctx)
        while result != self.API.INVALID_CYCLE:
            yield result
            self.API.findCycleWithEipValueObjectPrev(ctx)
            result = self.API.findCycleWithEipValueObjectCurrent(ctx)
        self.API.findCycleWithEipValueDelete(ctx)

    def _findCycleWithRegValue(self, regId, targetValue, startCycle=0, endCycle=None):
        startCycle  = self._getCycleFromObj(startCycle)
        endCycle    = self._getCycleFromObj(endCycle)
        raise Exception("Not implemented")

    def findNextCycleWithRegValue(self, regId, targetValue, startCycle=None, endCycle=None):
        if None == endCycle:
            endCycle = self.lastCycle
        else:
            endCycle = self._getCycleFromObj(endCycle)
        startCycle = self._getCycleFromObj(startCycle)
        ctx = self.API.regLogIter(self._log, regId, startCycle)
        cycle = self.API.regLogIterGetCycle
        while (cycle != INVALID_CYCLE) and (cycle < endCycle):
            val = self.API.regLogIterGetValue(ctx)
            if val == targetValue:
                yield cycle
            self.API.regLogIterNext(ctx)
            cycle = self.API.regLogIterGetCycle(ctx)
        self.API.regLogIterDelete(ctx)

    def findPrevCycleWithRegValue(self, regId, targetValue, startCycle=None, endCycle=0):
        startCycle  = self._getCycleFromObj(startCycle)
        endCycle    = self._getCycleFromObj(endCycle)
        ctx = self.API.regLogIter(self._log, regId, startCycle)
        cycle = self.API.regLogIterGetCycle
        while (cycle != INVALID_CYCLE) and (cycle < endCycle):
            val = self.API.regLogIterGetValue(ctx)
            if val == targetValue:
                yield cycle
            self.API.regLogIterPrev(ctx)
            cycle = self.API.regLogIterGetCycle(ctx)
        self.API.regLogIterDelete(ctx)

    def _getAddrAndCycle(self, x):
        if isinstance(x, (int, long)):
            cycle = self.cycle
            addr  = x
        elif isinstance(x, Address):
            cycle   = x.cycle
            addr    = x.address
        elif isinstance(x, tuple):
            cycle   = x[0]
            addr    = x[1]
        else:
            cycle   = x.cycle
            addr    = x.value
        return (cycle, addr)

    def _getCycleFromObj(self, cycle):
        if None == cycle:
            cycle = self.cycle
        elif isinstance(cycle, (Address, RegIter, RegValue, ValueInTime)):
            cycle = cycle.cycle
        if cycle >= self.lastCycle:
            cycle = self.lastCycle
        return cycle

    def _getValFromObj(self, x):
        if isinstance(x, Address):
            return x.address
        elif isinstance(x, (RegIter, RegValue, ValueInTime)):
            return x.value
        return x

    def findData(self, data, startCycle=0, endCycle=None):
        for res in self.searchForData(data, startCycle, endCycle):
            yield res

    def readMemory(self, addr, length):
        cycle, addr = self._getAddrAndCycle(addr)
        result = ''
        for offset in xrange(length):
            result += chr(self.API.getByte(self._log, cycle, addr + offset))
        return result

    def readAddr(self, addr):
        cycle, addr = self._getAddrAndCycle(addr)
        return Address( \
            cycle, \
            self.readDword((cycle, addr)))

    def readQword(self, addr):
        cycle, addr = self._getAddrAndCycle(addr)
        return \
                self.readByte(addr    ) + \
                self.readByte(addr + 1) * 0x100 + \
                self.readByte(addr + 2) * 0x10000 + \
                self.readByte(addr + 3) * 0x1000000 + \
                self.readByte(addr + 4) * 0x100000000 + \
                self.readByte(addr + 5) * 0x10000000000 + \
                self.readByte(addr + 6) * 0x1000000000000

    def readDword(self, addr):
        cycle, addr = self._getAddrAndCycle(addr)
        return self.API.getDword(self._log, cycle, addr)

    def readWord(self, addr):
        cycle, addr = self._getAddrAndCycle(addr)
        return self.API.getWord(self._log, cycle, addr)

    def readByte(self, addr):
        cycle, addr = self._getAddrAndCycle(addr)
        return self.API.getByte(self._log, cycle, addr)

    def readString(self, addr, maxSize=0x1000000, isUnicode=False):
        cycle, addr = self._getAddrAndCycle(addr)
        result = ''

        if isUnicode:
            for offset in xrange(0, maxSize, 2):
                char = self.readWord(addr + offset)
                if 0 == char or 0x100 < char:
                    break
                else:
                    result += chr(char)
        else:
            for offset in xrange(0, maxSize):
                char = self.readByte(addr + offset)
                if 0 == char:
                    break
                else:
                    result += chr(char)
        return result

    def disassemble(self, addr=None, lines=None):
        print self._disassemble(addr, lines)

    def _disassemble(self, addr=None, lines=None):
        if None == addr:
            addr = Address(self.cycle, self.eip(self.cycle).value)
        elif isinstance(addr, (int, long)):
            addr = Address(self.cycle, addr)
        elif not isinstance(addr, Address):
            addr = Address(addr)
        if None != lines:
            bytes_to_read = min(lines * 8, 0x100)
        else:
            bytes_to_read = 0x180
            lines = 0x20
        
        for module in self.modules:
            if module.isInRange(addr.address):
                data = module.getData(addr.address, bytes_to_read)
                break
        else:
            data = self.readMemory(addr, bytes_to_read)
        data = distorm3.Decode(addr, data, distorm3.Decode32Bits)
        output = ''
        for opcode in data[:lines]:
            output += "{0:08X} ({1:02X}) {2:<20s} {3:s}\n".format(opcode[0], opcode[1], opcode[3], opcode[2])
        return output

    def isAddressValid(self, addr):
        if not isinstance(addr, (int, long)):
            addr = addr.address
        if (addr >= 0x80000000) or (0x3f3f3f3f == addr):
            return False
        return True

    def getPointerSize(self):
        return self.POINTER_SIZE

    def getDefaultDataSize(self):
        return self.DEFAULT_DATA_SIZE

    def getEndianity(self):
        return "<"
