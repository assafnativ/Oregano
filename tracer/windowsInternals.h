
#ifndef _WINDOWS_INTERNALS_H_
#define _WINDOWS_INTERNALS_H_

#include <ntddk.h>
#include "GlobalDefines.h"

typedef struct ServiceTableEntry
{
    UINT32 *TableBase;
    UINT32 *CounterTableBase;
    UINT32 NumberOfServices;
    UINT8 *ParamTableBase;
} t_ServiceTableEntry;

typedef struct ServiceDescriptorTable
{
    t_ServiceTableEntry ServiceTable[4];
} t_ServiceDescriptorTable;
t_ServiceDescriptorTable * KeServiceDescriptorTable;

typedef struct _systemServiceInfo {
    UINT32      index;
    ADDRESS     ptr;
} systemServiceInfo;

/* Global:
 *  Unexported Services Infromation
 */
typedef struct _unexportedSystemServices {
    systemServiceInfo       NtSuspendProcess;
    systemServiceInfo       NtResumeProcess;
    systemServiceInfo       NtSuspendThread;
    systemServiceInfo       NtResumeThread;
} unexportedSystemServices;
extern unexportedSystemServices systemServices;

typedef NTSTATUS (*NtSuspendProcessPtr) (IN HANDLE ProcessHandle);
typedef NTSTATUS (*NtResumeProcessPtr)  (IN HANDLE ProcessHandle);
typedef NTSTATUS (*NtSuspendThreadPtr)  (IN HANDLE ThreadHandle);
typedef NTSTATUS (*NtResumeThreadPtr)   (IN HANDLE ThreadHandle);

NTSTATUS mySuspendProcess( HANDLE processId );
NTSTATUS myResumeProcess(  HANDLE processId );

typedef enum _KAPC_ENVIRONMENT {
    OriginalApcEnvironment,
    AttachedApcEnvironment,
    CurrentApcEnvironment,
    InsertApcEnvironment
} KAPC_ENVIRONMENT;

typedef
    VOID
    (*PKRUNDOWN_ROUTINE) (
    IN struct _KAPC *Apc );

typedef
    VOID
    (*PKNORMAL_ROUTINE) (
    IN PVOID NormalContext,
    IN PVOID SystemArgument1,
    IN PVOID SystemArgument2 );

typedef
    VOID
    (*PKKERNEL_ROUTINE) (
    IN struct _KAPC *Apc,
    IN OUT PKNORMAL_ROUTINE *NormalRoutine,
    IN OUT PVOID *NormalContext,
    IN OUT PVOID *SystemArgument1,
    IN OUT PVOID *SystemArgument2 );

NTKERNELAPI
    VOID
    KeInitializeApc (
        __out PRKAPC Apc,
        __in PRKTHREAD Thread,
        __in KAPC_ENVIRONMENT Environment,
        __in PKKERNEL_ROUTINE KernelRoutine,
        __in_opt PKRUNDOWN_ROUTINE RundownRoutine,
        __in_opt PKNORMAL_ROUTINE NormalRoutine,
        __in_opt KPROCESSOR_MODE ProcessorMode,
        __in_opt PVOID NormalContext );

NTKERNELAPI
    BOOLEAN
    KeInsertQueueApc (
        __inout PRKAPC Apc,
        __in_opt PVOID SystemArgument1,
        __in_opt PVOID SystemArgument2,
        __in KPRIORITY Increment );

#endif /* _WINDOWS_INTERNALS_H_ */

