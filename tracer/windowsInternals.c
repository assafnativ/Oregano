
#include "windowsInternals.h"

#pragma warning( disable : 4055 )

unexportedSystemServices systemServices = {0};

NTSTATUS mySuspendProcess( HANDLE processId )
{
    HANDLE process = 0;
    OBJECT_ATTRIBUTES objectAttributes = {0};
    NTSTATUS functionResult = STATUS_SUCCESS;
    CLIENT_ID clientId = {0};

    if (0 == systemServices.NtSuspendProcess.index) {
        return STATUS_INTERNAL_ERROR;
    }
    
    /* TODO: Find out which AccessMask is realy needed */
    clientId.UniqueProcess = processId;
    functionResult = ZwOpenProcess( &process, PROCESS_ALL_ACCESS, &objectAttributes, &clientId );
    if (FALSE == NT_SUCCESS(functionResult)) {
        KdPrint(( "Oregano: mySuspendProcess: Failed to open target process to ge a handle\r\n" ));
        return functionResult;
    }
    functionResult = ((NtSuspendProcessPtr)(systemServices.NtSuspendProcess.ptr))(process);
    if (FALSE == NT_SUCCESS(functionResult)) {
        KdPrint(( "Oregano: mySuspendProcess: Failed to suspend process\r\n" ));
        ZwClose(process);
        return functionResult;
    }

    return ZwClose(process);
} 

NTSTATUS myResumeProcess( HANDLE processId )
{
    HANDLE process = 0;
    OBJECT_ATTRIBUTES objectAttributes = {0};
    NTSTATUS functionResult = STATUS_SUCCESS;
    CLIENT_ID clientId = {0};

    if (0 == systemServices.NtResumeProcess.index) {
        return STATUS_INTERNAL_ERROR;
    }
    
    /* TODO: Find out which AccessMask is realy needed */
    clientId.UniqueProcess = processId;
    /* Maybe use THREAD_SUSPEND_RESUME with ObReferenceObjectByHandle Look at the code of psquery.c Line 2975 */
    functionResult = ZwOpenProcess( &process, PROCESS_ALL_ACCESS, &objectAttributes, &clientId );
    if (FALSE == NT_SUCCESS(functionResult)) {
        KdPrint(( "Oregano: myResumeProcess: Failed to open target process to ge a handle\r\n" ));
        return functionResult;
    }
    functionResult = ((NtResumeProcessPtr)(systemServices.NtResumeProcess.ptr))(process);
    if (FALSE == NT_SUCCESS(functionResult)) {
        KdPrint(( "Oregano: myResumeProcess: Failed to resume process\r\n" ));
        ZwClose(process);
        return functionResult;
    }

    return ZwClose(process);
}

