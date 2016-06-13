

/*
 * Oregano driver IRP MJ functions
 * defines all the IRP MJ functions needed for file access like.
 *
 * Written by Assaf Nativ
 */

/* Includes */
#include <ntifs.h>
#define NTSTRSAFE_LIB
#include <ntstrsafe.h>

#include "GlobalDefines.h"
#include "driver.h"
#include "interrupt.h"
#include "trapInterrupt.h"
#include "interruptsHooks.h"
#include "controlThreadContext.h"
#include "windowsInternals.h"
#include "offsets.h"

/* Set the functions types */
void stopTracing();
NTSTATUS allocBuffersPoll();
void deallocBuffersPoll();

/* Functions definitions */

/* Private functions */
NTSTATUS find_SystemServiceTable(ADDRESS * KeServiceDescriptorTable_ptr);
void newThreadHandler(
        IN HANDLE processId,
        IN HANDLE threadId,
        IN BOOLEAN create );

/*
 * All functions are PAGE type,
 * because they are all used more then once or used for unloading.
 */
#pragma alloc_text( PAGE, allocBuffersPoll )
#pragma alloc_text( PAGE, deallocBuffersPoll )
#pragma alloc_text( PAGE, default_irp_handler )
#pragma alloc_text( PAGE, stopTracing )
#pragma alloc_text( PAGE, onClose )
#pragma alloc_text( PAGE, onCreate )
#pragma alloc_text( PAGE, onDeviceControl )
#pragma alloc_text( PAGE, find_SystemServiceTable )
#pragma alloc_text( PAGE, newThreadHandler )

/* Private globals */
static ADDRESS       targetEProcess = NULL;
static BOOLEAN       is_new_thread_handler_installed = FALSE;
/* NTOS loading address */
static ADDRESS ntos_base = NULL;

/*
 * new_thread_handler
 *
 * Arguments:
 *  IN HANDLE processId
 *  IN HANDLE threadId
 *  IN HANDLE BOOLEAN create
 */
void newThreadHandler(
        IN HANDLE processId,
        IN HANDLE threadId,
        IN BOOLEAN create )
{
    PAGED_CODE();

    /* Do we have a target to log */
    if (0 == targetProcessId) {
        return;
    }
    if (targetProcessId != processId) {
        /* Not our target process */
        return;
    }
    if (FALSE == create) {
        /* We only care about new threads */
        return;
    }

    /* Set TRACE flag for the new thread */
    KdPrint(( "Oregano: new_thread_handler: Found new thread to log\r\n" ));
    setTrapFlagForThread(processId, threadId);

    return;
}

/*
 * allocBuffersPoll
 *
 *  Arguments:
 *      None
 */
NTSTATUS allocBuffersPoll()
{
    PAGED_CODE();

    /* Initialize output buffers vars */
    unsigned int        i = 0;
    void *              new_log_buffer = NULL;

    /* Initialize the buffers list */
    KdPrint(( "Oregano: allocBuffersPool: Allocating buffers poll\r\n" ));
    for( i = 0; LOG_BUFFER_NUM_OF_BUFFERS > i; ++i ) {
        if( NULL != log_buffer_item[i] ) {
            KdPrint(( "! Oregano: allocBuffersPoll: log buffer is already allocated!\r\n" ));
            break;
        }
        new_log_buffer = ExAllocatePoolWithTag( NonPagedPool, LOG_BUFFER_SIZE, OREGANO_MEMORY_TAG );
        //KdPrint(( "Oregano: on_create: Create buffer %x at %p\r\n", i, new_log_buffer ));
        if( NULL == new_log_buffer ) {
            KdPrint(( "! Oregano: allocBuffersPoll: Failed to allocate memory for log buffer %x\r\n", i ));
            return STATUS_INSUFFICIENT_RESOURCES;
        }
        RtlZeroMemory( new_log_buffer, LOG_BUFFER_SIZE );
        log_buffer_item[i] = new_log_buffer;
    } /* for */

    return STATUS_SUCCESS;
} /* allocBuffersPoll */

/*
 * deallocBuffersPoll
 *
 *  Arguments:
 *      None
 */
void deallocBuffersPoll()
{
    PAGED_CODE();

    /* Iterator for deallocating of log buffers. */
    unsigned int    i = 0;
    void *          buffer_to_free = NULL;

    KdPrint(( "Oregano: deallocBuffersPoll: Freeing memory\r\n" ));
    /* No more active log buffers */
    log_buffer = NULL;
    for( i = 0; LOG_BUFFER_NUM_OF_BUFFERS > i; ++i ) {
        buffer_to_free = log_buffer_item[i];
        if( NULL != buffer_to_free ) {
            //KdPrint(( "Oregano: deallocBuffersPoll: Freeing buffer %x (%p)\r\n", i, buffer_to_free ));
            ExFreePoolWithTag( buffer_to_free, OREGANO_MEMORY_TAG );
            log_buffer_item[i] = NULL;
        }
    } /* for */

    return;
} /* deallocBuffersPoll */

/*
 * io_control_debug_print
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_debug_print(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    unsigned long output_buffer_length = io_stack_irp->Parameters.DeviceIoControl.OutputBufferLength;
    NTSTATUS    function_result = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER(input_buffer);

    try {
        ProbeForWrite(
                (NTSTRSAFE_PSTR)output_buffer,
                output_buffer_length,
                sizeof(char) );
#ifdef DEBUG
        function_result = RtlStringCchPrintfA(
                (NTSTRSAFE_PSTR)output_buffer, output_buffer_length,
                "Oregano: Debug vars (0x%08X): %x %x %x %x %x %x %x %x\r\n",
                &DebugVar0, DebugVar0, DebugVar1, DebugVar2, DebugVar3, DebugVar4, DebugVar5, DebugVar6, DebugVar7);
#else
        function_result = RtlStringCchPrintfA(
                (NTSTRSAFE_PSTR)output_buffer, output_buffer_length,
                "Oregano: Debug" );
#endif
        if( FALSE == NT_SUCCESS(function_result) ) {
            goto IO_CONTROL_DEBUG_PRINT_RETURN;
        }
        KdPrint(( "%s", output_buffer ));
    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_debug_print: Failed to read buffer\r\n" ));
    }

IO_CONTROL_DEBUG_PRINT_RETURN:
    irp->IoStatus.Information   = output_buffer_length;
    return function_result;
}

/*
 */
NTSTATUS find_SystemServiceTable(ADDRESS * KeServiceDescriptorTable_ptr)
{
    PAGED_CODE();

#ifdef AMD64
    /* A anchor function that would use me to find both the NTOS base address and the offset to
     * the KeServuceDescriptorTabke
     */
    ADDRESS KeAddSystemServiceTable = NULL;
    ADDRESS mem_scan_ptr = 0;
    unsigned int byte_offset = 0;
    unsigned int keServiceDescriptorTable_offset = 0;
    UNICODE_STRING KeAddSystemServiceTable_str;
    WCHAR stringBuffer[0x100] = {0};
#elif i386
    UNICODE_STRING keServiceDescriptorTableStr;
    WCHAR stringBuffer[0x100] = {0};
#endif

#ifdef AMD64
    /* On Win64 the KeServiceDescriptorTable is no longer exported,
     * therefor MmGetSystemRoutineAddress won't work for it.
     * So I search it I first find the offset to it. This is done by
     * parsing the opcode that access the table at the
     * KeAddSystemServiceTable function. */
    KeAddSystemServiceTable_str.Buffer = stringBuffer;
    KeAddSystemServiceTable_str.Length = 0;
    KeAddSystemServiceTable_str.MaximumLength = 0x100;
    RtlAppendUnicodeToString(&KeAddSystemServiceTable_str, L"KeAddSystemServiceTable");
    KeAddSystemServiceTable = (ADDRESS)MmGetSystemRoutineAddress(&KeAddSystemServiceTable_str);
    KdPrint(( "Oregano: find_SystemServiceTable: KeAddSystemServiceTable address is %p\r\n", KeAddSystemServiceTable ));

    mem_scan_ptr = (ADDRESS)((MACHINE_LONG)KeAddSystemServiceTable & (~0xfff));   /* Aligen to page size */
    if (0 == mem_scan_ptr) {
        KdPrint(( "Oregano: find_SystemServiceTable: Can't find KeAddSystemServiceTable\r\n" ));
        return STATUS_INVALID_DEVICE_STATE;
    }
    /* Find NTOS base */
    while (0x5a4d != *(unsigned short *)mem_scan_ptr) {       /* MZ signature */
        mem_scan_ptr -= 0x1000;
        if (0 == mem_scan_ptr) {
            KdPrint(( "Oregano: find_SystemServiceTable: Can't find ntos start\r\n" ));
            return STATUS_INVALID_DEVICE_STATE;
        }
    }
    ntos_base = (ADDRESS)mem_scan_ptr;
    KdPrint(( "Oregano: find_SystemServiceTable: Found NTOS at %p\r\n", ntos_base ));

    /* Find offset to service descriptor table */
    mem_scan_ptr = KeAddSystemServiceTable;
    for (byte_offset = 0; byte_offset < 0x100; ++byte_offset) {
        /*
         *   4A 83 BC 18
         *   4B 83 BC 1A
         */
        if ( (
                (0x4a == *(mem_scan_ptr + byte_offset)) &&
                (0x83 == *(mem_scan_ptr + byte_offset + 1)) &&
                (0xbc == *(mem_scan_ptr + byte_offset + 2)) ) ||
             (
                (0x4b == *(mem_scan_ptr + byte_offset)) &&
                (0x83 == *(mem_scan_ptr + byte_offset + 1)) &&
                (0xbc == *(mem_scan_ptr + byte_offset + 2)) ) ) {
            /* Found the "cmp qword ptr" opcode */
            KdPrint(( "Oregano: find_SystemServiceTable: Found\r\n" ));
            mem_scan_ptr += byte_offset + 4;
            keServiceDescriptorTable_offset = *(unsigned long *)mem_scan_ptr;
            *KeServiceDescriptorTable_ptr = ntos_base + keServiceDescriptorTable_offset;
            break;
        }
    }
    if (0 == keServiceDescriptorTable_offset) {
        KdPrint(( "Oregano: find_SystemServiceTable: Can't find  offset to keServiceDescriptorTable\r\n" ));
        return STATUS_INVALID_DEVICE_STATE;
    }

#elif i386
    keServiceDescriptorTableStr.Buffer = stringBuffer;
    keServiceDescriptorTableStr.Length = 0;
    keServiceDescriptorTableStr.MaximumLength = 0x100;

    RtlAppendUnicodeToString(&keServiceDescriptorTableStr, L"Ke"); //KeServiceDescriptorTable
    RtlAppendUnicodeToString(&keServiceDescriptorTableStr, L"Service");
    RtlAppendUnicodeToString(&keServiceDescriptorTableStr, L"Descriptor");
    RtlAppendUnicodeToString(&keServiceDescriptorTableStr, L"Table");

    *KeServiceDescriptorTable_ptr = (ADDRESS)MmGetSystemRoutineAddress(&keServiceDescriptorTableStr);
    /* Now find the real address of the APIs */
    if (NULL == *KeServiceDescriptorTable_ptr) {
        KdPrint(( "Oregano: find_SystemServiceTable: Can't find KeServiceDescriptorTable\r\n" ));
        return STATUS_INVALID_DEVICE_STATE;
    }
#endif
    return STATUS_SUCCESS;
}


/*
 * io_control_init_oregano
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *          Some unexported system services indexes in the KeServiceDescriptorTable
 *      output_buffer
 */
NTSTATUS io_control_init_oregano(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    NTSTATUS    function_result = STATUS_SUCCESS;
    unsigned int * APIsInfo = (unsigned int *)input_buffer;
    unsigned int numberOfAPIs = 0;

    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(output_buffer);

    try {
        ProbeForRead(
                input_buffer,
                io_stack_irp->Parameters.DeviceIoControl.InputBufferLength,
                sizeof( char ) );
    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_init_oregano: Failed to read buffer\r\n" ));
        return STATUS_DATA_ERROR;
    }

    function_result = find_SystemServiceTable((ADDRESS *)(&KeServiceDescriptorTable));
    if (FALSE == NT_SUCCESS(function_result)) {
        KdPrint(( "Oregano: io_control_init_oregano: find_SystemServiceTable failed\r\n" ));
        return function_result;
    }
    numberOfAPIs = *APIsInfo;
    if (numberOfAPIs != (sizeof(systemServices) / sizeof(systemServiceInfo))) {
        KdPrint(( "Oregano: io_control_init_oregano: Not enough APIs info\r\n" ));
        return STATUS_DATA_NOT_ACCEPTED;
    }
    systemServices.NtSuspendProcess.index   = *(APIsInfo + 1);
    systemServices.NtResumeProcess.index    = *(APIsInfo + 2);
    systemServices.NtSuspendThread.index    = *(APIsInfo + 3);
    systemServices.NtResumeThread.index     = *(APIsInfo + 4);

    KdPrint(( "Oregano: io_control_init_oregano: keServiceDescriptorTable address is %p\r\n", &KeServiceDescriptorTable ));
    systemServices.NtSuspendProcess.ptr = ((ADDRESS *)KeServiceDescriptorTable->ServiceTable[0].TableBase)[
                                                    systemServices.NtSuspendProcess.index];
    systemServices.NtResumeProcess.ptr  = ((ADDRESS *)KeServiceDescriptorTable->ServiceTable[0].TableBase)[
                                                    systemServices.NtResumeProcess.index];
    systemServices.NtSuspendThread.ptr  = ((ADDRESS *)KeServiceDescriptorTable->ServiceTable[0].TableBase)[
                                                    systemServices.NtSuspendThread.index];
    systemServices.NtResumeThread.ptr   = ((ADDRESS *)KeServiceDescriptorTable->ServiceTable[0].TableBase)[
                                                    systemServices.NtResumeThread.index];
    KdPrint(( "Oregano: io_control_init_oregano: Set \r\n\tNtSuspendProcess to 0x%p\r\n\tNtResumeProcess  to 0x%p\r\n\tNtSuspendThread  to 0x%p\r\n\tNtResuemThread   to 0x%p\r\n",
        systemServices.NtSuspendProcess.ptr,
        systemServices.NtResumeProcess.ptr,
        systemServices.NtSuspendThread.ptr,
        systemServices.NtResumeThread.ptr ));

    return function_result;
}


/*
 * io_control_add_trace_range
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *          addTraceRangeInfo
 *      output_buffer
 */
NTSTATUS io_control_add_trace_range(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    NTSTATUS    function_result = STATUS_SUCCESS;
    /* Will use us to set a new logging range */
    ADDRESS rangeStart;
    ADDRESS rangeEnd;
    ADDRESS tempBottom;
    ADDRESS tempTop;
    unsigned int i = 0;

    addTraceRangeInfo * traceRangeInfo = (addTraceRangeInfo *)input_buffer;

    UNREFERENCED_PARAMETER(output_buffer);

    /* TBD - Need to find a way to stop logging when we change this vars...
     * Maybe unhook the interrupt. */
    try {
        ProbeForRead(
                input_buffer,
                io_stack_irp->Parameters.DeviceIoControl.InputBufferLength,
                sizeof( char ) );
    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_add_trace_range: Failed to read buffer\r\n" ));
        function_result = STATUS_DATA_ERROR;
        goto IO_CONTROL_ADD_TRACE_RANGE_INVALID_ARG;
    }

    stopAddress         = (ADDRESS)traceRangeInfo->stopAddress;
    rangeStart          = (ADDRESS)traceRangeInfo->rangeStart;
    rangeEnd            = (ADDRESS)traceRangeInfo->rangeEnd;
    KdPrint(( "Oregano: io_control_add_trace_range: stopAddress = %p range (%p - %p)\r\n",
            stopAddress, rangeStart, rangeEnd ));
    /* Validate arguments */
    if (NULL == rangeStart) {
        KdPrint( ("Oregano: io_control_add_trace_range: Logging from address zero is not allowed\r\n"));
        function_result = STATUS_INVALID_PARAMETER_2;
        goto IO_CONTROL_ADD_TRACE_RANGE_INVALID_ARG;
    }
    if (rangeStart >= rangeEnd) {
        KdPrint( ("Oregano: io_control_add_trace_range: Start of range must be smaller then end of range\r\n") );
        function_result = STATUS_INVALID_PARAMETER_3;
        goto IO_CONTROL_ADD_TRACE_RANGE_INVALID_ARG;
    }
    if (    (NULL != (ADDRESS)stopAddress) &&
            (((ADDRESS)stopAddress < rangeStart) ||
             ((ADDRESS)stopAddress > rangeEnd)) ) {
        KdPrint( ("Oregano: io_control_add_trace_range: Stop address must be in range\r\n") );
        function_result = STATUS_INVALID_PARAMETER_1;
        goto IO_CONTROL_ADD_TRACE_RANGE_INVALID_ARG;
    }

    /* Put the new range in the right place */
    for (i = 0; MAX_LOG_RANGES > i; ++i) {
        if (    (loggingRanges[i].BOTTOM_BOUND ==   NULL) ||
                (loggingRanges[i].BOTTOM_BOUND <    rangeStart) )
        {
            tempBottom          = loggingRanges[i].BOTTOM_BOUND;
            tempTop             = loggingRanges[i].TOP_BOUND;
            loggingRanges[i].BOTTOM_BOUND = rangeStart;
            loggingRanges[i].TOP_BOUND    = rangeEnd;
            rangeStart          = tempBottom;
            rangeEnd            = tempTop;
        }
        if (NULL == rangeStart) {
            break;
        }
    }

    irp->IoStatus.Information   = sizeof(addTraceRangeInfo);
    KdPrint(( "Oregano: io_control_add_trace_range: All done (%x)\r\n", function_result ));
IO_CONTROL_ADD_TRACE_RANGE_INVALID_ARG:

    return function_result;
}

/*
 * io_control_set_process_info
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *          setProcessInfo
 *      output_buffer
 */
NTSTATUS io_control_set_process_info(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    NTSTATUS        function_result = STATUS_SUCCESS;
    setProcessInfo *   processInfo = (setProcessInfo *)input_buffer;

    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(output_buffer);

    try {
        ProbeForRead(
                input_buffer,
                io_stack_irp->Parameters.DeviceIoControl.InputBufferLength,
                sizeof( char ) );
    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_set_process_info: Failed to read buffer\r\n" ));
        function_result = STATUS_DATA_ERROR;
        goto IO_CONTROL_SET_PROCESS_ID_INVALID_ARG;
    }

    if (0 != targetProcessId) {
        if (0 == processInfo->processId) {
            /* Clearing the target process */
            KdPrint( ("Oregano: io_control_set_process_info: Clearing process info\r\n") );
            stopTracing();
            goto IO_CONTROL_SET_PROCESS_ID_DONE;
        }
        else if (targetProcessId != (HANDLE)processInfo->processId) {
            /* Currently I can log only one process at a time */
            KdPrint( ("Oregano: io_control_set_process_info: You must stop tracing befor setting a new target process!\r\n") );
            function_result = STATUS_INVALID_PARAMETER_1;
            goto IO_CONTROL_SET_PROCESS_ID_INVALID_ARG;
        }
    }

    targetProcessId = (HANDLE)processInfo->processId;
    targetThreadId  = (HANDLE)processInfo->threadId;

    targetEProcess = NULL;
    target_process = NULL;
    function_result = PsLookupProcessByProcessId( targetProcessId, (PEPROCESS *)(&targetEProcess) );
    if (NT_SUCCESS(function_result) && (NULL != targetEProcess))
    {
        target_process = *(void **)(targetEProcess + offsets->eprocess.DirectoryTableBase);
    }
    else
    {
        KdPrint(("Oregano: io_control_set_process_info: Failed to query target process %p\r\n", targetProcessId));
    }

IO_CONTROL_SET_PROCESS_ID_INVALID_ARG:
IO_CONTROL_SET_PROCESS_ID_DONE:
    return function_result;
}

/*
 * io_control_start_trace
 *
 * Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_start_trace(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    /* Default return code is success */
    NTSTATUS    return_ntstatus = STATUS_SUCCESS;
    /* Temp thread context */
    static ThreadContext unknownThread = {0};

    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(io_stack_irp);
    UNREFERENCED_PARAMETER(input_buffer);
    UNREFERENCED_PARAMETER(output_buffer);

    /* Is valid process */
    if ((0 == targetProcessId) || (NULL == target_process)) {
        KdPrint( ("Oregano: io_control_start_trace: Can't log process id 0\r\n") );
        return STATUS_DATA_ERROR;
    }

    /* Set the current thread, to unknown */
    lastContext = &unknownThread;

    /* Set the trace flag */
    KdPrint( ("Oregano: io_control_start_trace: setting trace flag for process %p\r\n", targetProcessId) );
    setTrapFlagForAllThreads(targetProcessId);
    /* Set notify routine to install hooks on new threads,
        Iff it is not installed already, and we set the trace all threads */
    if ((FALSE == is_new_thread_handler_installed) && (0 == targetThreadId)) {
        KdPrint(( "Oregano: io_control_start_trace: Setting new thread notifier\r\n" ));
        return_ntstatus = PsSetCreateThreadNotifyRoutine( newThreadHandler );
        if (FALSE != NT_SUCCESS(return_ntstatus)) {
            is_new_thread_handler_installed = TRUE;
        } else {
            KdPrint(( "Oregano: io_control_start_trace: Can't set new thread notifier\r\n" ));
        }
    }

    return return_ntstatus;
}

/*
 * io_control_stop_trace
 *
 * Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_stop_trace(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    /* Default return code is success */
    NTSTATUS    return_ntstatus = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(io_stack_irp);
    UNREFERENCED_PARAMETER(input_buffer);
    UNREFERENCED_PARAMETER(output_buffer);

    stopTracing();

    return return_ntstatus;
}


/*
 * io_control_get_last_break_point_info
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_get_last_break_point_info(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(io_stack_irp);
    UNREFERENCED_PARAMETER(input_buffer);
    UNREFERENCED_PARAMETER(output_buffer);

    return STATUS_SUCCESS;
}


/*
 * io_control_probe_trace
 *
 * Give the user info that would help him write the log data to disk.
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_probe_trace(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    trace_info_t * trace_info = (trace_info_t *)output_buffer;

    UNREFERENCED_PARAMETER(input_buffer);

    try {
        ProbeForWrite(
                output_buffer,
                io_stack_irp->Parameters.DeviceIoControl.OutputBufferLength,
                sizeof( char ) );

        trace_info->buffer_pos          = *(unsigned int *)log_buffer;
        trace_info->trace_counter       = 0; // call_counter;
        trace_info->buffer              = log_buffer;
        trace_info->buffer_index        = active_log_buffer;
        trace_info->used_buffers        = InterlockedExchange((LONG *)&used_buffers, 0);
        trace_info->is_trace_stopped    = 0;
        KdPrint(("Oregano: io_control_probe_trace: Probe info buffer pos: %x buffer %p buffer index %x used buffers %x\r\n", *(unsigned int *)log_buffer, log_buffer, active_log_buffer, trace_info->used_buffers));

        /* Restart the buffers use counting */
        if (trace_info->used_buffers > LOG_BUFFER_NUM_OF_BUFFERS) {
            KdPrint(("Oregano: io_control_probe_trace: Buffer usage overrun!!!\r\n"));
        }

        irp->IoStatus.Information = sizeof(trace_info_t);

    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_probe_trace: Failed to read buffer\r\n" ));
    }


    return STATUS_SUCCESS;
}

/*
 * io_control_read_buffer
 *
 * Copy the log of a buffer to the user buffer
 *
 *  Arguments:
 *      irp
 *      io_stack_irp
 *      input_buffer
 *      output_buffer
 */
NTSTATUS io_control_read_buffer(
        PIRP irp,
        PIO_STACK_LOCATION  io_stack_irp,
        unsigned char * input_buffer,
        unsigned char * output_buffer )
{
    UINT32   buffer_number = 0;
    unsigned char * requested_log_buffer = NULL;

    try {
        ProbeForRead(
                input_buffer,
                io_stack_irp->Parameters.DeviceIoControl.InputBufferLength,
                sizeof( char ) );
        // KdPrint(("Oregano: io_control_read_buffer: Valid input buffer\r\n"));

        ProbeForWrite(
                output_buffer,
                io_stack_irp->Parameters.DeviceIoControl.OutputBufferLength,
                sizeof( char ) );
        // KdPrint(("Oregano: io_control_read_buffer: Valid output buffer\r\n"));

        buffer_number = (*((UINT32 *)input_buffer)) & LOG_BUFFER_NUM_OF_BUFFERS_MASK;
        requested_log_buffer = log_buffer_item[buffer_number];
        KdPrint(("Oregano: io_control_read_buffer: Copying buffer %x (%p) to user buffer\r\n",
                    buffer_number, requested_log_buffer));
        RtlCopyMemory( output_buffer, requested_log_buffer, LOG_BUFFER_SIZE );
        irp->IoStatus.Information   = LOG_BUFFER_SIZE;
        // KdPrint(("Oregano: io_control_read_buffer: Done copying\r\n"));
    } except (EXCEPTION_EXECUTE_HANDLER) {
        KdPrint(( "Oregano: io_control_read_buffer: Failed to read / write buffer\r\n" ));
        return STATUS_DATA_ERROR;
    }

    return STATUS_SUCCESS;
}

/* Public functions */

/* For functions declaration see the header file */

/* See header file for descriptions */
/* TODO: I get this IRP quite a lot, need to find out why */
NTSTATUS default_irp_handler( PDEVICE_OBJECT device_object, PIRP irp )
{
    /* Default return code is STATUS_NOT_SUPPORTED */
    NTSTATUS    return_ntstatus = STATUS_NOT_SUPPORTED;
    //KdBreakPoint();

    UNREFERENCED_PARAMETER(device_object);
#ifndef DEBUG
    UNREFERENCED_PARAMETER(irp);
#endif

    PAGED_CODE();

    KdPrint(( "Oregano: Unhandled IRP MJ function call, type %d\r\n", irp->Type ));

    return( return_ntstatus );
}

/* Stops and cleans any tracing if needed */
void stopTracing()
{
    KIRQL old_irql = 0;

    PAGED_CODE();

    /* Raise the IRQL otherwise new thread could be created while cleaning */
    old_irql = KeGetCurrentIrql();
    if (old_irql < APC_LEVEL) {
        KeRaiseIrql (APC_LEVEL, &old_irql);
    }

    KdPrint( ("Oregano: stopTracing: Got a stop trace command\r\n") );
    if (TRUE == is_new_thread_handler_installed) {
        PsRemoveCreateThreadNotifyRoutine(newThreadHandler);
        is_new_thread_handler_installed = FALSE;
    } else {
        KdPrint(( "Oregano: stopTracing: Not new thread notifier\r\n" ));
    }
    if (0 != targetProcessId) {
        unsetTrapFlagForAllThreads(targetProcessId);
        targetProcessId = 0;
    }
    if (NULL != targetEProcess) {
        ObDereferenceObject( targetEProcess );
        targetEProcess = NULL;
    }
    target_process = NULL;
    RtlZeroMemory( loggingRanges, sizeof(loggingRanges) );

    /* Set back the Irql */
    if (old_irql < APC_LEVEL) {
        KeLowerIrql( old_irql );
    }

    return;
}

NTSTATUS onClose(PDEVICE_OBJECT device_object, PIRP irp)
{
    /* Would hold the return code of the function */
    NTSTATUS    return_ntstatus = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER(device_object);
    UNREFERENCED_PARAMETER(irp);

    PAGED_CODE();

    KdPrint(( "Oregano: on_close: Start\r\n" ));

    /* Stop any active trace */
    stopTracing();

    /* Unhook poor trap interrupt, if needed to... */
    if( 0 != orgTrapInterrupt ) {

        /* Would hold the current IDT address */
        idt_t               idt = {0};
        /* Would hold int1 info, original and new one */
        interrupt_info_t    int1_info = {0};
        /* Used only for setting the int address in the int1 info structure */
        MACHINE_LONG        trap_interrupt_address = 0;

        KdPrint(( "Oregano: on_close: Unhooking trap interrupt\r\n" ));

        /* First get the idt address */
        #ifndef AMD64
        load_idt( &idt );
        #else
        loadIdt64( &idt );
        #endif

        /* Get the current int1 function */
        get_interrupt_info( &idt, 1, &int1_info );

        /* Set back the old int1 */
#ifdef i386
        trap_interrupt_address = (MACHINE_LONG)orgTrapInterrupt;
        int1_info.low_offset    = (unsigned short)trap_interrupt_address;
        trap_interrupt_address >>= 16;
        int1_info.high_offset   = (unsigned short)trap_interrupt_address;
#elif AMD64
        trap_interrupt_address = (MACHINE_LONG)orgTrapInterrupt;
        int1_info.low_offset    = (unsigned short)trap_interrupt_address;
        trap_interrupt_address >>= 16;
        int1_info.middle_offset = (unsigned short)trap_interrupt_address;
        trap_interrupt_address >>= 16;
        int1_info.high_offset   = (unsigned long)trap_interrupt_address;
#endif
        hookAllCPUs( 1, &int1_info );
        orgTrapInterrupt = NULL;
        KdPrint(( "Oregano: on_close: Unhook done.\r\n" ));
    }
    /* Now we can feel free to deallocate memory */
    deallocBuffersPoll();

    return( return_ntstatus );
} /* on_close */


/* Converting function pointer into MACHINE_LONG raise a warning */
#pragma warning( disable : 4054 )
InterruptHookInfo interruptsHooks[] = {
    {0x1, &orgTrapInterrupt, (ADDRESS)trap_interrupt, {0}},
    {0x3, &orgBreakpointInterrupt, NULL, {0}},
    //{0xc, &orgStackFaultInterrupt, (MACHINE_LONG)stackFaultInterrupt, {0}},
    //{0xd, &orgGPFInterrupt, 0, {0}},
    //{0xe, &orgPageFaultInterrupt, 0, {0}},
    {0xffffffff, NULL, NULL, {0}}
};
#pragma warning( default : 4054 )

NTSTATUS onCreate(PDEVICE_OBJECT device_object, PIRP irp)
{
    /* Would hold the return code of the function */
    NTSTATUS    return_ntstatus = STATUS_SUCCESS;

    /* Would hold the current IDT address */
    idt_t               idt = {0};
    /* Used only for setting the int address in the interrupt info struct */
    MACHINE_LONG        interruptAddress = 0;       /* Machine long is ADDRESS which we can manipulate */
    /* For installing hooks */
    InterruptHookInfo * hooksIter = NULL;

    UNREFERENCED_PARAMETER(irp);
    UNREFERENCED_PARAMETER(device_object);

    PAGED_CODE();

    DbgPrint( "Oregano: on_create: I/O Create\r\n" );

    return_ntstatus = allocBuffersPoll();
    if (FALSE == NT_SUCCESS(return_ntstatus)) {
        DbgPrint( "Oregano: on_create: Alloc buffers poll failed\r\n" );
        goto ON_CREATE_ALLOC_ERROR;
    }

    /* Set the current active buffer to the first one */
    log_buffer = log_buffer_item[0];
    /* First DWORD of the buffer is the next writing point,
     * so set it to 4 so we won't overwrite the buffer position */
    *(unsigned int *)log_buffer = sizeof(unsigned int);
    active_log_buffer = 0;
    next_free_log_buffer = 0;

    /* Initialize threads context saving array */
    RtlZeroMemory( threads, sizeof(threads) );
    /* Initialize logging ranges array */
    RtlZeroMemory( loggingRanges, sizeof(loggingRanges) );

    if (0 == orgTrapInterrupt) {
        DbgPrint( "Oregano: on_create: Setting Int1 (Trap interrupt) hook\r\n" );

        /* First get the idt address */
        #ifdef i386
        load_idt( &idt );
        #elif AMD64
        loadIdt64( &idt );
        #endif

        for (hooksIter = interruptsHooks; 0xffffffff != hooksIter->index; ++hooksIter) {
            /* Now get the default interrupts */
            get_interrupt_info( &idt, (unsigned char)hooksIter->index, &hooksIter->intInfo );

#ifdef i386
            *(hooksIter->accessableOrgIntAddress) = (ADDRESS)(
                                            hooksIter->intInfo.high_offset << 16 ) +
                                            hooksIter->intInfo.low_offset;
#elif AMD64
            interruptAddress = hooksIter->intInfo.high_offset;
            interruptAddress <<= 32;
            interruptAddress |= (MACHINE_LONG)hooksIter->intInfo.middle_offset << 16;
            interruptAddress |= hooksIter->intInfo.low_offset;
            *(hooksIter->accessableOrgIntAddress) = (ADDRESS)interruptAddress;
#endif
            DbgPrint( "Oregano: on_create: Interrupt 0x%02x address = %p\r\n",
                        hooksIter->index,
                        *hooksIter->accessableOrgIntAddress );

            if (0 != hooksIter->newInterrupt) {
                /* Set the hook */
#ifdef i386
                interruptAddress = (MACHINE_LONG)hooksIter->newInterrupt;
                hooksIter->intInfo.low_offset   = (unsigned short)interruptAddress;
                interruptAddress >>= 16;
                hooksIter->intInfo.high_offset  = (unsigned short)interruptAddress;
#elif AMD64
                interruptAddress = (MACHINE_LONG)hooksIter->newInterrupt;
                hooksIter->intInfo.low_offset       = (unsigned short)interruptAddress;
                interruptAddress >>= 16;
                hooksIter->intInfo.middle_offset    = (unsigned short)interruptAddress;
                interruptAddress >>= 16;
                hooksIter->intInfo.high_offset      = (unsigned long)interruptAddress;
#endif
                hookAllCPUs( (unsigned char)hooksIter->index, &hooksIter->intInfo );
                DbgPrint( "Oregano: on_create: Hook is set\r\n" );
            } else {
                DbgPrint("Oregano: on_create: No alternative interrupt\r\n");
            }
        }
    } else {
        DbgPrint( "Oregano: on_create: Hook is already set\r\n" );
    }

    /* Well done, bye bye... */
    return( return_ntstatus );

    /* Errors */
ON_CREATE_ALLOC_ERROR:
    stopTracing();
    deallocBuffersPoll();
    return( return_ntstatus );
}



/* See header file driver.h for descriptions */
NTSTATUS onDeviceControl(PDEVICE_OBJECT device_object, PIRP irp)
{
    /* Would hold the return code of the function */
    NTSTATUS        return_ntstatus = STATUS_SUCCESS;

    /* Would point to the current IO IRP stack */
    PIO_STACK_LOCATION  io_stack_irp = NULL;

    /* Used for input output data of the driver */
    unsigned char * input_buffer = NULL;
    unsigned char * output_buffer = NULL;

    UNREFERENCED_PARAMETER(device_object);

    PAGED_CODE();

    KdPrint(( "Oregano: on_device_control: Device I/O Control\r\n"));

    /* First get the current stack irp location,
     * this way certain parameters for the driver are past through the IRP */
    io_stack_irp = IoGetCurrentIrpStackLocation( irp );
    if( NULL == io_stack_irp ) {
        KdPrint(( "Oregano: on_device_control: Error while getting the io irp stack location\r\n" ));
        return_ntstatus = STATUS_SEVERITY_ERROR;
        goto ON_DEVICE_CONTROL_IO_GET_CURRENT_IRP_STACK_LOCATION_ERROR;
    }

    /* Set default value for size read / write */
    irp->IoStatus.Information   = 0;

    /* All of our IoControl messages are type 3 */
    /* We are using type 3 input buffer (Direct access to user space buffer). */
    input_buffer    = (unsigned char *)io_stack_irp->Parameters.DeviceIoControl.Type3InputBuffer;
    output_buffer   = (unsigned char *)irp->UserBuffer;

    unsigned long   io_control_code = 0;

    io_control_code = io_stack_irp->Parameters.DeviceIoControl.IoControlCode;
    KdPrint(( "Oregano: on_device_control: Device io control code: %x\r\n", io_control_code ));
    switch( io_control_code ) {
        case IOCTL_DEBUG_PRINT:
            KdPrint(("Oregano: on_device_control: IOCTL_DEBUG_PRINT\r\n"));
            return_ntstatus = io_control_debug_print(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_DEBUG_PRINT - Done\r\n"));
            break;
        case IOCTL_INIT_OREGANO:
            KdPrint(("Oregano: on_device_control: IOCTL_INIT_OREGANO\r\n"));
            return_ntstatus = io_control_init_oregano(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_INIT_OREGANO - Done\r\n"));
            break;
        case IOCTL_ADD_TRACE_RANGE:
            KdPrint(("Oregano: on_device_control: IOCTL_ADD_TRACE_RANGE\r\n"));
            return_ntstatus = io_control_add_trace_range(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_ADD_TRACE_RANGE - Done\r\n"));
            break;
        case IOCTL_SET_PROCESS_INFO:
            KdPrint(("Oregano: on_device_control: IOCTL_SET_PROCESS_ID\r\n"));
            return_ntstatus = io_control_set_process_info(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_SET_PROCESS_ID - Done\r\n"));
            break;
        case IOCTL_START_TRACE:
            KdPrint(("Oregano: on_device_control: IOCTL_START_TRACE\r\n"));
            return_ntstatus = io_control_start_trace(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_START_TRACE - Done\r\n"));
            break;
        case IOCTL_STOP_TRACE:
            KdPrint(("Oregano: on_device_control: IOCTL_STOP_TRACE\r\n"));
            return_ntstatus = io_control_stop_trace(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_STOP_TRACE - Done\r\n"));
            break;
        case IOCTL_GET_LAST_BREAK_POINT_INFO:
            KdPrint(("Oregano: on_device_control: IOCTL_GET_LAST_BREAK_POINT_INFO\r\n"));
            return_ntstatus = io_control_get_last_break_point_info(
                    irp, io_stack_irp, input_buffer, output_buffer );
            KdPrint(("Oregano: on_device_control: IOCTL_GET_LAST_BREAK_POINT_INFO - Done\r\n"));
            break;
        case IOCTL_PROBE_TRACE:
            //KdPrint(("Oregano: on_device_control: IOCTL_PROBE_TRACE\r\n"));
            return_ntstatus = io_control_probe_trace(
                    irp, io_stack_irp, input_buffer, output_buffer );
            //KdPrint(("Oregano: on_device_control: IOCTL_PROBE_TRACE - Done\r\n"));
            break;
        /*
            * TOBD: Maybe I should let the driver write the log to disk
            */
        case IOCTL_READ_BUFFER:
            // KdPrint(("Oregano: on_device_control: IOCTL_READ_BUFFER\r\n"));
            if( 0 == targetProcessId ) {
                goto ON_DEVICE_CONTROL_IO_BUFFERS_ERROR;
            }
            return_ntstatus = io_control_read_buffer(
                    irp, io_stack_irp, input_buffer, output_buffer );
            // KdPrint(("Oregano: on_device_control: IOCTL_READ_BUFFER - Done\r\n"));
            break;
        default:
            KdPrint(( "Oregano: on_device_control: Unknown io control code %d\r\n", io_control_code ));
    }

    /* Function epilogue */
ON_DEVICE_CONTROL_IO_GET_CURRENT_IRP_STACK_LOCATION_ERROR:
ON_DEVICE_CONTROL_IO_BUFFERS_ERROR:
    irp->IoStatus.Status = return_ntstatus;

    /* We are done with this irp, lets pass it to the I/O manger,
     * The IO_NO_INCREMENT means that we do not mess around with the
     * Scheduler. */
    IoCompleteRequest( irp, IO_NO_INCREMENT );

    return( return_ntstatus );

} /* on_device_control */

