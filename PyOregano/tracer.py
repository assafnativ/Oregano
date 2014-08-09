

from NativDebugging.Win32.MemoryReader import *
from NativDebugging.Win32.MemoryMap import *

from .tracerException import tracerException
from .win32Structs import *
from .oreganoIoCtl import *

import platform
import time
from struct import pack, unpack
import thread
import sys
import traceback
import exceptions

def attach(target_process, target_thread=0, outputPath='C:\\Debugging'):
    if int == type(target_process) or long == type(target_process):
        return PyOregano(target_process, target_thread, outputPath=outputPath)
    elif str == type(target_process):
        processes = findProcessId(target_process)
        if 0 == len(processes):
            raise ValueError("Can't find process with that name")
        elif 1 < len(processes):
            raise ValueError("More then one process with that name")
        return PyOregano(processes[0][1], target_thread, outputPath=outputPath)
    else:
        raise ValueError("Target must be either process id or process name")

class PyOregano( MemoryReader ):
    OREGANO_VERSION = 1
    # Versions names are taken from http://msdn.microsoft.com/en-us/library/ms724832(v=vs.85).aspx
    if 'AMD64' in platform.machine():
        OREGANO_FILE = "Oregano64.sys"
        POINTER_PACK = 'Q'
        IS_WIN64 = True
    elif 'x86' in platform.machine():
        OREGANO_FILE = "Oregano.sys"
        POINTER_PACK = 'L'
        IS_WIN64 = False
    else:
        raise Exception("Unsupported platform {0}".format(platform.machine()))

    MOV_EAX_OPCODE = 0xb8
    MOV_EDX_OPCODE = 0xba
    REX_PREFIX     = 0x4c

    ONE_BUFFER_SIZE = 0x40000
    NUM_OF_BUFFERS = 0x1000

    START_SERVICE_TIMEOUT = 10

    def __init__( self, target_process_id, target_thread_id=0, outputPath='C:\\Debugging'):

        self._targetThreadId = target_thread_id
        self._oregano_handle = None
        self.keepReading = False
        if None == outputPath:
            outputPath = os.getcwd()
        self.outputPath = outputPath

        # Currently Oregano supports only one processor at this time
        MemoryReader.__init__(self, target_process_id)
        self._lastAffinityMask = c_uint32(0)
        systemAffinityMask = c_uint32(0)
        GetProcessAffinityMask( \
                self._process, \
                byref(self._lastAffinityMask), \
                byref(systemAffinityMask) )
        SetProcessAffinityMask(self._process, 1)

        try:
            self._isDriverLoaded = False

            # Firest we try to load the driver, if needed
            SCManager = OpenSCManager( None, None, win32con.SC_MANAGER_CREATE_SERVICE )

            winver =  sys.getwindowsversion().major * 0x100
            winver += sys.getwindowsversion().minor
            print("Running on Windows version: 0x{0}".format(winver))
            oreganoDriverFile = os.path.sep.join(__file__.split(os.path.sep)[:-1])
            oreganoDriverFile = os.path.sep.join([oreganoDriverFile, self.OREGANO_FILE])
            print("Using oregano driver file {0}".format(oreganoDriverFile))
            oreganoService = self.OREGANO_FILE
            oreganoService = oreganoService[:oreganoService.find('.')]
            oreganoDisplayName = oreganoService + ' Driver'
            print('Loading driver {0} (Display name: {1})'.format(oreganoDriverFile, oreganoDisplayName))
            service = OpenService(
                        SCManager,
                        oreganoService,
                        win32con.SERVICE_START | win32con.DELETE | win32con.SERVICE_STOP )

            self._service = service
            self._isDriverLoaded = True

            print('Starting service {0:d}'.format(service))
            startServiceRC = StartService( service, 0, None )
            e = WinError()
            # 1056 is the service is already running error
            if 0 == startServiceRC and 1056 != e.winerror:
                raise e
            print('Service started 0x%x' % startServiceRC)
            
            print('Driver is loaded')

            print('Opening device')
            startAttempStart = time.time()
            while time.time() - startAttempStart < self.START_SERVICE_TIMEOUT:
                oregano_handle = CreateFile(
                        '\\\\.\\Oregano',
                        win32con.GENERIC_READ | win32con.GENERIC_WRITE,
                        0,
                        None,
                        win32con.OPEN_EXISTING,
                        0,
                        0 )
                if( 0xffffffff != oregano_handle ):
                    break
            if( 0xffffffff == oregano_handle ):
                print('Open device timeout!')
                raise WinError()
            print('Device is open handle = {0:08X}'.format(oregano_handle))
            self._oregano_handle = oregano_handle
        
            self.initOregano()
            self.performDebugIOCTL()

            self._lastBufferRead = 0
            self._lastBufferUsed = 0 
        except:
            print('Failed to create Oregano instance')
            self.unloadDriver()
            traceback.print_exc( sys.exc_info )

    def getSyscallIndex( self, procAddr ):
        firstByte = c_uint8.from_address(procAddr).value
        if firstByte == self.REX_PREFIX:
            procAddr += 3
            firstByte = c_uint8.from_address(procAddr).value
        if firstByte in [self.MOV_EAX_OPCODE, self.MOV_EDX_OPCODE]:
            procIndex   = c_uint32.from_address(procAddr + 1).value
        else:
            raise tracerException("Failed to find sysgate for 0x%x" % procAddr)
        return procIndex

    def initOregano( self ):
        # Find the system services index of NtSuspendProcess and NtResumeProcess
        ntdll = windll.kernel32.LoadLibraryA('ntdll.dll')
        try:
            NtSuspendProcess    = windll.kernel32.GetProcAddress(ntdll, 'NtSuspendProcess')
            NtResumeProcess     = windll.kernel32.GetProcAddress(ntdll, 'NtResumeProcess')
            NtSuspendThread     = windll.kernel32.GetProcAddress(ntdll, 'NtSuspendThread')
            NtResumeThread      = windll.kernel32.GetProcAddress(ntdll, 'NtResumeThread')
        except exceptions.WindowsError, e:
            # Sometimes the function is prefixed by Zw and not Nt, god knows what goes inside the
            # the head of the common MS developer.
            if 126 == e.winerror:
                NtSuspendProcess    = windll.kernel32.GetProcAddress(ntdll, 'ZwSuspendProcess')
                NtResumeProcess     = windll.kernel32.GetProcAddress(ntdll, 'ZwResumeProcess')
                NtSuspendThread     = windll.kernel32.GetProcAddress(ntdll, 'ZwSuspendThread')
                NtResumeThread      = windll.kernel32.GetProcAddress(ntdll, 'ZwResumeThread')
            else:
                raise e

        apisInfo  = pack('=L', 4)
        apisInfo += pack('=L', self.getSyscallIndex(NtSuspendProcess))
        apisInfo += pack('=L', self.getSyscallIndex(NtResumeProcess))
        apisInfo += pack('=L', self.getSyscallIndex(NtSuspendThread))
        apisInfo += pack('=L', self.getSyscallIndex(NtResumeThread))

        outputBuffer = '\x00' * 1000
        bytesWritten = c_uint32(0)
        DeviceIoControl(
                self._oregano_handle,
                IOCTL_INIT_OREGANO,
                apisInfo,
                len(apisInfo),
                outputBuffer,
                len(outputBuffer),
                addressof( bytesWritten ),
                None )

    def performDebugIOCTL( self ):
        test_string = "I/O Control test"
        outputBuffer = '\x00' * 1000
        bytesWritten = c_uint32(0)
        DeviceIoControl(
                self._oregano_handle,
                IOCTL_DEBUG_PRINT,
                test_string,
                len(test_string),
                outputBuffer,
                len(outputBuffer),
                addressof( bytesWritten ),
                None )

    def unloadDriver( self ):
        if None != self._oregano_handle:
            CloseHandle( self._oregano_handle )
        if None != self._service:
            ss = SERVICE_STATUS()
            try:
                ControlService( self._service, win32con.SERVICE_CONTROL_STOP, addressof(ss) )
            except:
                pass
            CloseServiceHandle( self._service )

    def probeInfoAndRead( self ):
        # TODO:
        # I think the strategy here should be to raise the prioraty of this python script
        # but keep it sleepy most of the time
        outputBuffer   = '\x00' * 28
        bytesWritten   = c_uint32(0)
        input_buffer    = '\x00' * 0x100

        DeviceIoControl(
                self._oregano_handle,
                IOCTL_PROBE_TRACE,
                input_buffer,
                len(input_buffer),
                outputBuffer,
                len(outputBuffer),
                addressof(bytesWritten),
                None )
        buffer_pos, trace_counter, buffer_address, self._lastBufferUsed, used_buffers, is_trace_stopped = \
                    unpack('=LLLLLL', outputBuffer[:24])
        if PyOregano.NUM_OF_BUFFERS <= used_buffers:
            raise tracerException("Failed to keep up on the reading job")
        while self._lastBufferUsed != self._lastBufferRead:
            self.readBuffer(self._lastBufferRead)
            self._lastBufferRead += 1
            self._lastBufferRead %= PyOregano.NUM_OF_BUFFERS
    
    def readBuffer( self, x ):
        buffer_number = pack('=L', x) + ('\x00' * 12)
        outputBuffer = '\x00' * PyOregano.ONE_BUFFER_SIZE
        bytesWritten = c_uint32(0)
        #print 'Reading buffer %x' % x
        DeviceIoControl(
                    self._oregano_handle,
                    IOCTL_READ_BUFFER,
                    buffer_number,
                    len(buffer_number),
                    outputBuffer,
                    PyOregano.ONE_BUFFER_SIZE,
                    addressof( bytesWritten ),
                    None )
        bytesWritten = bytesWritten.value
        if 0 == bytesWritten:
            print "Failed to read log buffer %x" % x
            return
        #print 'Read %x bytes' % bytesWritten
        bufferEndPoint = unpack('=L', outputBuffer[:4])[0]
        if 4 > bufferEndPoint or bufferEndPoint > bytesWritten:
            raise tracerException('Invalid buffer size 0x%x (%s) (Bytes written 0x%x, buffer size 0x%x)' % 
                    (bufferEndPoint, outputBuffer.encode('hex'), bytesWritten, len(outputBuffer)))
        self.traceFile.write(outputBuffer[4:bufferEndPoint])
    
    def readingBuffersLoop( self, *argv ):
        print("Starting the reading loop")
        self.keepReading = True
        # On win64 I get the invalid handle error... Need to fix it.
        #if not self.IS_WIN64:
        #    SetThreadPriority( GetCurrentThread(), win32con.THREAD_PRIORITY_ABOVE_NORMAL )

        try:
            # TODO:
            # I think the strategy here should be to raise the prioraty of this python script
            # but keep it a sleep most of the time
            outputBuffer   = '\x00' * 28
            bytesWritten   = c_uint32(0)

            while self.keepReading:
                while self.keepReading and (self._lastBufferUsed == self._lastBufferRead):
                    DeviceIoControl(
                            self._oregano_handle,
                            IOCTL_PROBE_TRACE,
                            None,
                            0,
                            outputBuffer,
                            len(outputBuffer),
                            byref(bytesWritten),
                            None )
                    buffer_pos, trace_counter, buffer_address, self._lastBufferUsed, used_buffers, isTraceStop = \
                                    unpack('=LL' + self.POINTER_PACK + 'LLL', outputBuffer[:20+[4,8][self.IS_WIN64]])
                    if PyOregano.NUM_OF_BUFFERS <= self._lastBufferUsed:
                        raise tracerException( "Invalid buffer id! ({0:d}, {1:d})".format(
                                self._lastBufferUsed, PyOregano.NUM_OF_BUFFERS) )
                        break
                    if PyOregano.NUM_OF_BUFFERS <= used_buffers:
                        raise tracerException("Failed to keep up on the reading job (Used buffers = 0x{0:x})".format(used_buffers))
                    if 0 == used_buffers:
                        time.sleep(0.01)
                #print 'BufferPos: 0x%x, traceCounter: 0x%x, bufferAddress: 0x%x, lastBufferUsed: 0x%x' % (buffer_pos, trace_counter, buffer_address, self._lastBufferUsed)
                while self.keepReading and (self._lastBufferUsed != self._lastBufferRead):
                    self.readBuffer(self._lastBufferRead)
                    self._lastBufferRead += 1
                    self._lastBufferRead %= PyOregano.NUM_OF_BUFFERS
                if 0 != isTraceStop:
                    print( "Trace stopped" )
                    break
        except:
            print('Got some kind of exception')
            traceback.print_exc( sys.exc_info )
        # Read the leaft overs
        if self._lastBufferRead == self._lastBufferRead:
            self.readBuffer(self._lastBufferRead)
        self.traceFile.flush()
        self.traceFile.close()
        print("Exiting the reading loop")

    def _makeAtom(self, name, data):
        return pack('=L', len(data)) + name + data

    def _writeAtom(self, name, data):
        self.traceFile.write(self._makeAtom(name, data))
    
    def setNewLogFile( self, logRanges ):
        self.traceFile = file(
                os.path.sep.join(
                    [self.outputPath, 'trace{0:s}.bin'.format(time.strftime('%Y_%m_%d__%H_%M'))]),
                'wb')
        logInfo = pack('=L', self.OREGANO_VERSION)
        if self.IS_WIN64:
            logInfo += pack('=L', 1)
        else:
            logInfo += pack('=L', 0)
        logInfo += pack('=L', 1) # Old mem log flag
        self._writeAtom("OREG", logInfo)
        modules = self.enumModules()
        modulesInfo = ''
        loggedModules = []
        for module in modules:
            for logRange in logRanges:
                if logRange[0] > (module[0] + module[2]):
                    continue
                if logRange[1] <= module[0]:
                    continue
                loggedModules.append(module)
        for module in loggedModules:
            modulesInfo += self._makeAtom('MODL', \
                    module[1] + '\x00' + \
                    pack('=L', module[0]) + \
                    pack('=L', module[2]) + \
                    self.readMemory(module[0], module[2]) )
        self._writeAtom('MDLS', pack('=L', len(loggedModules)) + modulesInfo)
        rangesInfo = ''
        for logRange in logRanges:
            rangesInfo += self._makeAtom('RNGE', pack('=' + (self.POINTER_PACK * 2), *logRange))
        self._writeAtom("RNGS", pack('=L', len(logRanges)) + rangesInfo)

        self.traceFile.write("\xff" * 4)
        self.traceFile.write("TRCE")
        self.traceFile.flush()

    def setTraceInfo( self, logRanges, stopAddress=0 ):
        if isinstance(logRanges, tuple):
            logRanges = [logRanges]

        logRanges.sort()
        print('Setting the following ranges:')
        for logRange in logRanges:
            print('0x{0:x}:0x{1:x}'.format(logRange[0], logRange[1]))

        self.setNewLogFile(logRanges)

        for logRange in logRanges:
            rangeStart, rangeEnd = logRange
            if (0,0) != logRange:
                if rangeStart >= rangeEnd:
                    raise tracerException("Start of range must be smaller than end of range")
                if 0 != stopAddress and (stopAddress < rangeStart or stopAddress > rangeEnd):
                    raise tracerException("Stop address must be in range")
                trace_info = pack('=' + (self.POINTER_PACK * 3), stopAddress, rangeStart, rangeEnd)
            else:
                rnageEnd = [0x7fffffff, 0x7fffffffffffffff][self.IS_WIN64]
                trace_info = pack('=' + (self.POINTER_PACK * 3), 0, 0, rangeEnd)
            bytesWritten = c_uint32(0)
            DeviceIoControl(
                    self._oregano_handle,
                    IOCTL_ADD_TRACE_RANGE,
                    trace_info,
                    len(trace_info),
                    None,
                    0,
                    byref(bytesWritten),
                    None )

        print("Setting process id to {0:d}".format(self._processId))
        trace_info = pack('=LL', self._processId, self._targetThreadId)
        DeviceIoControl(
                self._oregano_handle,
                IOCTL_SET_PROCESS_INFO,
                trace_info,
                len(trace_info),
                None,
                0,
                byref(bytesWritten),
                None )

        print("Starting the trace")
        DeviceIoControl(
                self._oregano_handle,
                IOCTL_START_TRACE,
                '',
                0,
                None,
                0,
                byref(bytesWritten),
                None )

        print("Start reader thread")
        if False == self.keepReading:
            readingThread = thread.start_new_thread(self.readingBuffersLoop, ())

    def _mergeRanges(self, ranges):
        THRESHOLD = 0x100
        newRanges = []
        while 0 < len(ranges):
            currentStart, currentEnd = ranges[0]
            ranges = ranges[1:]
            tempRanges = ranges[:]
            for start, end in ranges:
                if currentStart < start and currentEnd > (start - THRESHOLD):
                    currentEnd = end
                    tempRanges.remove((start, end))
                    continue
                if currentEnd > end and currentStart < (end + THRESHOLD):
                    currentStart = start
                    tempRanges.remove((start, end))
                    continue
            ranges = tempRanges
            newRanges.append((currentStart, currentEnd))
        return newRanges

    def setTraceOnModule( self, moduleNameStartsWith, stopAddress=0 ):
        ranges = []
        if not isinstance(moduleNameStartsWith, (list, tuple)):
            moduleNameStartsWith = [moduleNameStartsWith]
        moduleNameStartsWith = [x.lower() for x in moduleNameStartsWith]
        for moduleBase, moduleName, moduleSize in self.enumModules(isVerbose=True):
            moduleName = moduleName.lower()
            needToLog = False
            for prefix in moduleNameStartsWith:
                if moduleName.startswith(prefix):
                    needToLog = True
                    break
            if needToLog:
                moduleEnd = moduleBase + moduleSize
                print('Adding module {0:s} ({1:x}-{2:x})'.format(moduleName, moduleBase, moduleEnd))
                ranges.append((moduleBase, moduleEnd))
        if 0 == len(ranges):
            print('No range to log')
            return
        ranges = self._mergeRanges(ranges)
        self.setTraceInfo(ranges, stopAddress)

    def setTraceInteractiveSetTrace( self ):
        stopAddress = raw_input('Set stop address (0 for default)')
        if '' == stopAddress:
            stopAddress = 0
        else:
            stopAddress = int(stopAddress)
        ranges = []
        for moduleBase, moduleName, moduleSize in self.enumModules(isVerbose=True):
            answer = raw_input('Add module? Yes/No/Cancel')
            if answer.lower().startswith('y'):
                ranges.append((moduleBase, moduleBase+moduleSize))
            elif answer.lower().startswith('c'):
                return
        if 0 == len(ranges):
            print('No range to log')
            return
        ranges = self._mergeRanges(ranges)
        self.setTraceInfo(ranges, stopAddress)

    def stop(self):
        print("Stopping the trace")
        bytesWritten = c_uint32(0)
        DeviceIoControl(
                self._oregano_handle,
                IOCTL_STOP_TRACE,
                '',
                0,
                None,
                0,
                byref(bytesWritten),
                None )
        self.keepReading = False

