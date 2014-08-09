
import win32con
from ctypes import *


def ErrorIfZero(handle):
    if handle == 0:
        raise WinError()
    else:
        return handle

TRUE = c_char( 	chr( int( True  ) ) )
FALSE = c_char( chr( int( False ) ) )
void_NULL = c_void_p( win32con.NULL )
pchar_NULL = c_char_p( win32con.NULL )

GetCurrentThread = windll.kernel32.GetCurrentThread
GetCurrentThread.argtypes = []
GetCurrentThread.restype = c_uint

SetThreadPriority = windll.kernel32.SetThreadPriority
SetThreadPriority.argtypes = [
        c_uint,     # HANDLE
        c_uint ]    # New priority
SetThreadPriority.restype = ErrorIfZero

OpenSCManager = windll.advapi32.OpenSCManagerA
OpenSCManager.argtypes = [
	c_char_p,	# lpMachineName
	c_char_p,	# lpDatabaseName
	c_uint ]	# dwDesiredAccess
OpenSCManager.restype = ErrorIfZero


CreateService = windll.advapi32.CreateServiceA
CreateService.argtypes = [
	c_uint,		# hSCManager
	c_char_p,	# lpServiceName
	c_char_p,	# lpDisplayName
	c_uint,		# dwDesiredAccess
	c_uint,		# dwServiceType
	c_uint,		# dwStartType
	c_uint,		# dwErrorControl
	c_char_p,	# lpBinaryPathName
	c_char_p,	# lpLoadOrderGroup
	c_void_p,	# lpdwTagId
	c_char_p,	# lpDependencies
	c_char_p,	# lpServiceStartName
	c_char_p ]	# lpPassword
CreateService.restype = ErrorIfZero


StartService = windll.advapi32.StartServiceA
StartService.argtypes = [
	c_uint,		# hService,
	c_uint,		# dwNumServiceArgs
	c_void_p ]	# lpServiceArgVectors
StartService.restype = c_uint


OpenService = windll.advapi32.OpenServiceA
OpenService.argtypes = [
	c_uint,		# hSCManager
	c_char_p,	# lpServiceName
	c_uint ]	# dwDesiredAccess
OpenService.restype = c_uint


CreateFile = windll.kernel32.CreateFileA
CreateFile.argtypes = [
	c_char_p,	# lpFileName
	c_uint,		# dwDesiredAccess
	c_uint,		# dwShareMode
	c_void_p,	# lpSecurityAttributes
	c_uint,		# dwCreationDisposition
	c_uint,		# dwFlagsAndAttributes
	c_uint ]	# hTemplateFile
CreateFile.restype = c_uint


DeviceIoControl = windll.kernel32.DeviceIoControl
DeviceIoControl.argtypes = [
	c_uint,		# hDevice
	c_uint,		# dwIoControlCode
	c_void_p,	# lpInBuffer
	c_uint,		# nInBufferSize
	c_void_p,	# lpOutBuffer
	c_uint,		# nOutBufferSize
	c_void_p,	# lpBytesReturned
	c_void_p ]	# lpOverlapped
DeviceIoControl.restype = c_uint


CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [ c_uint ] # hObject
CloseHandle.restype = ErrorIfZero


class SERVICE_STATUS( Structure ):
	_fields_ = [
		('dwServiceType',		c_uint),
		('dwCurrentState',		c_uint),
		('dwControlsAccepted',	c_uint),
		('dwWin32ExitCode',		c_uint),
		('dwServiceSpecificExitCode',	c_uint),
		('dwCheckPoint',		c_uint),
		('dwWaitHint',			c_uint) ]


ControlService = windll.advapi32.ControlService
ControlService.argtypes = [
	c_uint,		# hService
	c_uint,		# dwControl
	c_void_p ]	# lpServiceStatus
ControlService.restype = ErrorIfZero


CloseServiceHandle = windll.advapi32.CloseServiceHandle
CloseServiceHandle.argtypes = [ c_uint ] # hSCObject
CloseServiceHandle.restype = ErrorIfZero


DeleteService = windll.advapi32.DeleteService
DeleteService.argtypes = [ c_uint ] # hService
DeleteService.restype = ErrorIfZero

SetProcessAffinityMask = windll.kernel32.SetProcessAffinityMask
SetProcessAffinityMask.argtypes = [
        c_uint,     # HANDLE hProcess
        c_uint ]    # DWORD_PTR dwProcessAffinityMask - It's not really DWORD_PTR, it's DWORD. None understand the MSDN.
SetProcessAffinityMask.restype = ErrorIfZero

GetProcessAffinityMask = windll.kernel32.GetProcessAffinityMask
GetProcessAffinityMask.argtypes = [
        c_uint,     # HANDLE hProcess
        c_void_p,   # PDWORD_PTR lpProcessAffinityMask
        c_void_p ]  # PDWORD_PTR lpSystemAffinityMask
GetProcessAffinityMask.restype = ErrorIfZero

# Add some win32 const, that are forgatten in the win32con module
win32con.SC_MANAGER_CREATE_SERVICE		= 0x0002
win32con.SERVICE_START					= 0x0010
win32con.SERVICE_STOP					= 0x0020
win32con.SERVICE_CONTROL_STOP			= 0x00000001


