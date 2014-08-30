
/* Used for PsLookupProcessByProcessId */
#include <ntifs.h>

#include "controlThreadContext.h"
#include "trapInterrupt.h"
/* Used for the definition of the undocumented SuspendThread API */
#include "windowsInternals.h"

/* Local functions */
VOID clearTrapFlagAPC( IN PKAPC Apc, IN PKNORMAL_ROUTINE *NormalRoutine, IN PVOID *NormalContext, IN PVOID *SystemArgument1, IN PVOID *SystemArgument2 );
VOID setTrapFlagAPC( IN PKAPC Apc, IN PKNORMAL_ROUTINE *NormalRoutine, IN PVOID *NormalContext, IN PVOID *SystemArgument1, IN PVOID *SystemArgument2 );
void changeTrapFlagForThread( ADDRESS ethread, int setTheFlag );
void changeTrapFlag(ADDRESS ethread, int setTheFlag);
NTSTATUS setProcessForInterfering(HANDLE process_id, ADDRESS * process, PLIST_ENTRY * threadListHead);
NTSTATUS doneInterferingWithProcess( HANDLE process_id, ADDRESS * process );
NTSTATUS setThreadForInterfering( HANDLE process_id, HANDLE thread_id, ADDRESS * thread );
NTSTATUS doneInterferingWithThread( HANDLE process_id, HANDLE thread_id, ADDRESS * thread );
NTSTATUS changeTrapFlagForThreadId( HANDLE process_id, HANDLE thread_id, int setTheFlag );
NTSTATUS changeTrapFlagForAllThreads( HANDLE process_id, int setTheFlag );

#pragma alloc_text( PAGE, clearTrapFlagAPC )
#pragma alloc_text( PAGE, setTrapFlagAPC )
#pragma alloc_text( PAGE, changeTrapFlagForThread )
#pragma alloc_text( PAGE, changeTrapFlag )
#pragma alloc_text( PAGE, setProcessForInterfering )
#pragma alloc_text( PAGE, doneInterferingWithProcess )
#pragma alloc_text( PAGE, setThreadForInterfering )
#pragma alloc_text( PAGE, doneInterferingWithThread )
#pragma alloc_text( PAGE, changeTrapFlagForThreadId )
#pragma alloc_text( PAGE, changeTrapFlagForAllThreads )
#pragma alloc_text( PAGE, setTrapFlagForAllThreads )
#pragma alloc_text( PAGE, unsetTrapFlagForAllThreads )
#pragma alloc_text( PAGE, setTrapFlagForThread )

void changeTrapFlag(ADDRESS ethread, int setTheFlag)
{
    ADDRESS     eflags = NULL;
    ADDRESS     threadKStack = *(ADDRESS *)(ethread + offsets->ethread.InitialStack);

    threadKStack -= offsets->thread_context.ktrap_frame_size;
    DbgPrint("Oregano: clearTrapFlagAPC: Trap frame is %x\r\n", threadKStack);

    /* The kernel stack is unpagable! */

    eflags = threadKStack + offsets->thread_context.eflags;
    DbgPrint("Oregano: changeTrapFlag: EFlags = %x\r\n", *((UINT32 *)eflags));
    if (setTheFlag)
    {
        /* Set the flag */
        *((UINT32 *)eflags) |= TRAP_FLAG;
    }
    else
    {
        /* Clear the flag */
        *((UINT32 *)eflags) &= ~TRAP_FLAG;
    }
    DbgPrint("Oregano: changeTrapFlag: EFlags new value = %x\r\n", *((UINT32 *)eflags));
}

VOID clearTrapFlagAPC(
    IN PKAPC Apc,
    IN PKNORMAL_ROUTINE *NormalRoutine,
    IN PVOID *NormalContext,
    IN PVOID *SystemArgument1,
    IN PVOID *SystemArgument2 )
{
    ADDRESS     ethread = (ADDRESS)Apc->SystemArgument1;
    KEVENT *    operationComplete = (KEVENT *)Apc->SystemArgument2;

    UNREFERENCED_PARAMETER(NormalRoutine);
    UNREFERENCED_PARAMETER(NormalContext);
    UNREFERENCED_PARAMETER(SystemArgument1);
    UNREFERENCED_PARAMETER(SystemArgument2);

    changeTrapFlag(ethread, 0);

	/* Signal operation complete */
	if (NULL != operationComplete)
	{
		KeSetEvent(operationComplete, 0, FALSE);
	}
}

/* Changing the thread context should be done from within the thread */
VOID setTrapFlagAPC(
    IN PKAPC Apc,
    IN PKNORMAL_ROUTINE *NormalRoutine,
    IN PVOID *NormalContext,
    IN PVOID *SystemArgument1,
    IN PVOID *SystemArgument2 )
{
    ADDRESS     ethread = (ADDRESS)Apc->SystemArgument1;
    KEVENT *    operationComplete = (KEVENT *)Apc->SystemArgument2;

    UNREFERENCED_PARAMETER(NormalRoutine);
    UNREFERENCED_PARAMETER(NormalContext);
    UNREFERENCED_PARAMETER(SystemArgument1);
    UNREFERENCED_PARAMETER(SystemArgument2);

    changeTrapFlag(ethread, 1);

    KeSetEvent(operationComplete, 0, FALSE);
}


void changeTrapFlagForThread( ADDRESS ethread, int setTheFlag )
{
    /* Is this a system thread, because if so, I have no interest in it. */
    /* System thread has teb == NULL */
    if (
        (NULL != *(ADDRESS *)(ethread + offsets->ethread.Teb)) &&
        (0 == ((*(UINT32 *)(ethread + offsets->ethread.CrossThreadFlags)) & 0x00000010UL /* PS_CROSS_THREAD_FLAGS_SYSTEM */ )) ) {

        /* This is not a system thread */

        ADDRESS threadKStack = NULL;
        HANDLE thread_id = (HANDLE)(*(UINT32 *)(ethread + offsets->ethread.Cid + sizeof(UINT32)));

        /* Is that the target thread, or are we set to trace all threads */
        if (
            (0 == target_thread_id) ||
            (target_thread_id == thread_id) ) {

            DbgPrint("Oregano: This thread is in target %x\r\n", target_thread_id);
            /* Find the kernel stack of the thread */
            threadKStack = *(ADDRESS *)(ethread + offsets->ethread.InitialStack);
            DbgPrint("Oregano: changeTraceFlagForThread: Initial stack for thread %x is %x\r\n", 
                                ethread, 
                                threadKStack);
            if (NULL != threadKStack) {
                UINT32 hashIndex = 0;
                KAPC apc = {0};
                KEVENT operationComplete = {0};
                KeInitializeEvent(&operationComplete, NotificationEvent, FALSE);

                if (FALSE != setTheFlag)
                {
                    ThreadContext * threadCtx = NULL;
#pragma warning( disable : 4305 )
                    /* Find a free entry in the Hash table */
                    hashIndex = (((UINT32)ethread) & THREAD_ID_MASK) >> THREAD_ID_IGNORED_BITS;
                    DbgPrint("Oregano: setTrapFlagAPC: EThread %x hash id %x\r\n", ethread, hashIndex);
                    while (0 != threads[hashIndex].ID) {
                        hashIndex = (hashIndex + 1) % THREAD_CONTEXT_MAX_THREADS;
                    }
                    threadCtx = &threads[hashIndex];
#pragma warning( default : 4305 )
#ifdef AMD64
                    threadCtx->ID = (UINT64)ethread;
                    threadCtx->RDI = UNKNOWN_QWORD_VALUE;
                    threadCtx->RSI = UNKNOWN_QWORD_VALUE;
                    threadCtx->RBP = UNKNOWN_QWORD_VALUE;
                    threadCtx->RBX = UNKNOWN_QWORD_VALUE;
                    threadCtx->RDX = UNKNOWN_QWORD_VALUE;
                    threadCtx->RCX = UNKNOWN_QWORD_VALUE;
                    threadCtx->RAX = UNKNOWN_QWORD_VALUE;
                    threadCtx->R8 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R9 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R10 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R11 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R12 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R13 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R14 = UNKNOWN_QWORD_VALUE;
                    threadCtx->R15 = UNKNOWN_QWORD_VALUE;
                    threadCtx->RIP = (ADDRESS)0;
                    threadCtx->RCS = UNKNOWN_QWORD_VALUE;
                    threadCtx->RFLAGS = UNKNOWN_QWORD_VALUE;
                    threadCtx->RSP = UNKNOWN_QWORD_VALUE;
#else
                    /* Set the flag */
                    threadCtx->ID = (UINT32)ethread;
                    threadCtx->EDI = UNKNOWN_DWORD_VALUE;
                    threadCtx->ESI = UNKNOWN_DWORD_VALUE;
                    threadCtx->EBP = UNKNOWN_DWORD_VALUE;
                    threadCtx->EBX = UNKNOWN_DWORD_VALUE;
                    threadCtx->EDX = UNKNOWN_DWORD_VALUE;
                    threadCtx->ECX = UNKNOWN_DWORD_VALUE;
                    threadCtx->EAX = UNKNOWN_DWORD_VALUE;
                    threadCtx->EIP = (ADDRESS)0;
                    threadCtx->ECS = UNKNOWN_DWORD_VALUE;
                    threadCtx->EFLAGS = UNKNOWN_DWORD_VALUE;
                    threadCtx->ESP = UNKNOWN_DWORD_VALUE;
#endif
                }
                else
                {
                    /* TODO: Need to remove thread from threads hash table, and reorder the table. */
                }

                /* Setting the trace flag and save context */
				if (ethread == (ADDRESS)PsGetCurrentThread())
				{
					/* We are attached to the right thread, just change the eflags */
					changeTrapFlag(ethread, setTheFlag);
					
					DbgPrint("Oregano: changeTraceFlagForThread: Done thread");
				}
				else {
					/* Not attached to the right thread, invoke an APC to change the eflags */
					if (FALSE == setTheFlag) {
						KeInitializeApc(&apc, (PKTHREAD)ethread, OriginalApcEnvironment, clearTrapFlagAPC, NULL, NULL, KernelMode, NULL);
					}
					else {  /* if (false == setTheFlag) */
						KeInitializeApc(&apc, (PKTHREAD)ethread, OriginalApcEnvironment, setTrapFlagAPC, NULL, NULL, KernelMode, NULL);
					} /* else (false == setTheFlag) */
					if (!KeInsertQueueApc(&apc, (PVOID)ethread, (PVOID)&operationComplete, 2)) {
						DbgPrint("Oregano: changeTraceFlagForThread: APC for setting trap flag failed");
					}
					KeWaitForSingleObject(&operationComplete, Executive, KernelMode, FALSE, NULL);
					DbgPrint("Oregano: changeTraceFlagForThread: Done thread using APC");
				}

            } /* If system thread */
            else {
                DbgPrint("Oregano: changeTraceFlagForThread: Invalid kstack, probebly thread is not set yet\r\n");
            }
        } /* If target thread id */
        else {
            DbgPrint("Oregano: Not a target thread %p\r\n", thread_id);
        }
    } /* If not a system thread */
    else {
        DbgPrint("Oregano: %p (ethread) is a system thread\r\n", ethread);
    }
}

NTSTATUS setProcessForInterfering( HANDLE process_id, ADDRESS * process, PLIST_ENTRY * threadListHead ) 
{
    NTSTATUS functionResult = STATUS_SUCCESS;

    /* Getting the handle to the process from the process id */
    functionResult = PsLookupProcessByProcessId( process_id, (PEPROCESS *)process );
    if( FALSE != NT_SUCCESS(functionResult) ) {
        /* The threads list is build in the following way:
         *  EPROCESS + 0x220 points to ETHREAD + 0x190 
         *  ETHREAD + 0x190 points to another ETHREAD + 0x190 
         *  Last thread on the list + 0x190 points back to EPROCESS + 0x220 */
        *threadListHead = (PLIST_ENTRY)((*process) + offsets->eprocess.ThreadListHead);    
    } else {
        KdPrint(( "Oregano: control_thread_context: Failed to get the process from process id %08x\r\n", 
                    functionResult ));
    }

    return functionResult;
}

NTSTATUS doneInterferingWithProcess( HANDLE process_id, ADDRESS * process )
{
    NTSTATUS functionResult = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER( process_id );

    ObDereferenceObject( (void *)(*process) );

    return functionResult;
}

NTSTATUS setThreadForInterfering( HANDLE process_id, HANDLE thread_id, ADDRESS * thread )
{
    NTSTATUS functionResult = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER( process_id );

    /* Getting the handle to the thread from the thread id */
    functionResult = PsLookupThreadByThreadId( thread_id, (PETHREAD *)thread );
    if( FALSE == NT_SUCCESS(functionResult) ) {
        KdPrint(( "Oregano: control_thread_context: Failed to get the thread by PsLookupThreadByThreadId(0x%08x) (%08x), probebly new thread that is not in the list yet\r\n", 
            thread_id, functionResult ));
    }

    return functionResult;
}

NTSTATUS doneInterferingWithThread( HANDLE process_id, HANDLE thread_id, ADDRESS * thread )
{
    NTSTATUS functionResult = STATUS_SUCCESS;

    UNREFERENCED_PARAMETER( process_id );
    UNREFERENCED_PARAMETER( thread_id );

    ObDereferenceObject( (void *)(*thread) );

    return functionResult;
}

NTSTATUS changeTrapFlagForThreadId( HANDLE process_id, HANDLE thread_id, int setTheFlag )
{
    NTSTATUS        functionResult  = STATUS_SUCCESS;
    ADDRESS         thread = NULL;

    KIRQL           OldIrql = 0;

    // Sanity checks
    if (0 == process_id)
    {
        KdPrint(( "Oregano: changeTraceFlagForThreadId: Error!!! process_id is zero\r\n" ));
        return STATUS_INVALID_PARAMETER_1;
    }
    if (0 == thread_id)
    {
        KdPrint(( "Oregano: changeTraceFlagForThreadId: Error!!! thread_id is zero\r\n" ));
        return STATUS_INVALID_PARAMETER_2;
    }

    OldIrql = KeGetCurrentIrql();
    if (OldIrql < APC_LEVEL) {
        KeRaiseIrql (APC_LEVEL, &OldIrql);
    }

    functionResult = setThreadForInterfering( process_id, thread_id, &thread );
    if (FALSE != NT_SUCCESS(functionResult)) {
        changeTrapFlagForThread( thread, setTheFlag );

        functionResult = doneInterferingWithThread( process_id, thread_id, &thread );
        if (FALSE != NT_SUCCESS(functionResult)) {
            KdPrint(( "Oregano: changeTraceFlagForThreadId: All done OK\r\n" ));
        } else {
            KdPrint(( "Oregano: changeTraceFlagForThreadId: Failed to restore thread state\r\n" ));
        }

    } else {
        KdPrint(( "Oregano: changeTraceFlagForThreadId: Failed to set thread for interfering\r\n" ));
    }

    /* Set back the Irql */
    if (OldIrql < APC_LEVEL) {
        KeLowerIrql (OldIrql);
    }
    return functionResult;
}

/*
 * The following function is either setting the trace flag or clearing it from all threads
 * of a specific process, without debugging it.
 */
#pragma warning (disable:4305)
NTSTATUS changeTrapFlagForAllThreads( HANDLE process_id, int setTheFlag )
{
    NTSTATUS        functionResult  = STATUS_SUCCESS;
    ADDRESS         process         = NULL;

    PLIST_ENTRY     threadListHead  = NULL;
    PLIST_ENTRY     threadsIter     = NULL;
    ADDRESS         ethread         = NULL;

    KIRQL           OldIrql = 0;

    /* I'll try something new.
        Instead of suspending the process and threads, I'll just raise the IRQL */
    OldIrql = KeGetCurrentIrql();
    if (OldIrql < APC_LEVEL) {
        KeRaiseIrql (APC_LEVEL, &OldIrql);
    }

    functionResult = setProcessForInterfering( process_id, &process, &threadListHead );
    if (FALSE != NT_SUCCESS(functionResult)) {

        KdPrint(( "Oregano: changeTraceFlagForAllThreads: Thread head is %x for EProcess %x\r\n", threadListHead, process ));

        /* Try to enum all threads in process.
            We start on pointing to the threadListHead on the EPROCESS (meaning eprocess + 0x180,)
            so after this read of the Flink, we are pointing to the first ethread.
            At the end of the list we get back to an eprocess item. Yes, a strange structure indeed. */
        for (   threadsIter = threadListHead->Flink;
                ( (threadsIter != threadListHead) &&
                  (threadsIter != NULL) );
                threadsIter = threadsIter->Flink )
        {
            ethread = ((ADDRESS)threadsIter - offsets->ethread.ThreadListEntry);
            KdPrint(( "Oregano: changeTraceFlagForAllThreads: EThread %x (Teb: %x, CrossThreadFalgs: %x)\r\n", ethread, *(ADDRESS *)(ethread + offsets->ethread.Teb), *(UINT32 *)(ethread + offsets->ethread.CrossThreadFlags)));

            changeTrapFlagForThread( ethread, setTheFlag );

            KdPrint(( "Oregano: changeTraceFlagForAllThreads: Found new thread %x\r\n", ethread ));
        } /* For */

    
        /* Cleanup / close handles */
        functionResult = doneInterferingWithProcess(process_id, &process);

        if (FALSE != NT_SUCCESS(functionResult)) {
            KdPrint(( "Oregano: changeTraceFlagForAllThreads: All done ok\r\n" ));
        } else {
            KdPrint(( "Oregano: changeTraceFlagForAllThreads: Something went wrong\r\n" ));
        }

    } else {
        KdPrint(( "Oregano: changeTraceFlagForAllThreads: Failed to set thread from interfering\r\n" ));
    }

    /* Set back the Irql */
    if (OldIrql < APC_LEVEL) {
        KeLowerIrql (OldIrql);
    }

    KdPrint(( "Oregano: changeTraceFlagForAllThreads: Done\r\n" ));
    return functionResult;
}
#pragma warning (default:4305)

/* 
 * The following function is made to set the trace flag of all threads in a specific process, 
 * without debugging it.
 */
NTSTATUS setTrapFlagForAllThreads( HANDLE process_id )
{
    return changeTrapFlagForAllThreads( process_id, TRUE );
}

/* 
 * The following function is made to unset the trace flag of all threads in a specific process, 
 * without debugging it.
 */
NTSTATUS unsetTrapFlagForAllThreads( HANDLE process_id )
{
    return changeTrapFlagForAllThreads( process_id, FALSE );
}

NTSTATUS setTrapFlagForThread( HANDLE process_id, HANDLE thread_id )
{
    NTSTATUS functionResult = STATUS_SUCCESS;

    functionResult = changeTrapFlagForThreadId( process_id, thread_id, TRUE );
    if ( FALSE != NT_SUCCESS(functionResult) )
    {
        // This is done because on most of Windows versions when we get the notification about the new thread,
        // the thread is not found in the global linked list yet, and PsLookupThreadByThreadId will fail.
       KdPrint(( "Oregano: setTraceFlagForThread: Failed to change trace flag per thread, attempt to change all threads using threads linked list\r\n" ));
       functionResult = setTrapFlagForAllThreads(process_id);
    }
    return functionResult;
}
