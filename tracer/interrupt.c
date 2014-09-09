

/*
 * Interrupts manipulation functions.
 *
 * Written by Assaf Nativ
 */

/* Includes */
#include <wdm.h>
#include "interrupt.h"
#include "interruptsHooks.h"

/* Functions definitions */

/* Public functions */

/* For functions declaration see the header file */

#ifndef AMD64
/* See header file for descriptions */
void load_idt( OUT idt_t * idt )
{
	KdPrint(( "Oregano: load_idt: Loading IDT\r\n" ));
	/* Load the idt address */
	__asm {
		mov eax, [idt]
		sidt [eax]
	}

	KdPrint((
			"Oregano: load_idt: IDT was loaded limit = %X, base = %p\r\n",
			idt->limit,
			idt->base ));

	return;
}
#endif

/* See header file for descriptions */
void get_interrupt_info(
						IN	idt_t *				idt,
						IN	unsigned char		interrupt_index,
						OUT interrupt_info_t *	interrupt_info )
{
	/* Would hold the address of the interrupt in the idt */
	unsigned char * int_pointer = NULL;

	KdPrint(( "Oregano: get_interrupt_info: Get int %x info\r\n", interrupt_index ));

	/* Just for safety */
	__try {
		/* Calculate the address of the interrupt from the idt */
		int_pointer = idt->base + 
						( interrupt_index * sizeof(interrupt_info_t) );
		/* Copy the relevant data */
		RtlCopyMemory(
			   interrupt_info,
			   (const void *)int_pointer,
			   sizeof(interrupt_info_t) );
		
	}
	__except( 1 ) {
		/* O my, we got an exception :( */
		KdPrint(( "Oregano: get_interrupt_info: Exception!\r\n" ));
	}
#ifdef i386
    KdPrint(( "Oregano: get_interrupt_info: Current value low: %x selector: %x access: %x unused: %x hight: %x\r\n",
                    (unsigned int)interrupt_info->low_offset, 
                    (unsigned int)interrupt_info->selector, 
                    (unsigned int)interrupt_info->access, 
                    (unsigned int)interrupt_info->unused, 
                    (unsigned int)interrupt_info->high_offset ) );
#elif AMD64
    KdPrint(( "Oregano: get_interrupt_info64: Current value low: %x mid: %x hight: %x selector: %x\r\n",
                    (unsigned int)interrupt_info->low_offset, 
                    (unsigned int)interrupt_info->middle_offset, 
                    (unsigned int)interrupt_info->high_offset,
                    (unsigned int)interrupt_info->selector) );
#endif
}

#ifndef AMD64
/* See header file for descriptions */
void set_interrupt(
					IN	ADDRESS				idt,
					IN	unsigned char		interrupt_index,
					IN	interrupt_info_t *	new_interrupt )
{
	/* Would hold the address of the interrupt in the idt */
	unsigned char * int_pointer = NULL;
	
	KdPrint(( "Oregano: set_interrupt: setting interrupt 0x%02x to %p\r\n", interrupt_index, new_interrupt ));

	/* Just for safety */
	__try {
		/* Calculate the address of the interrupt from the idt */
		int_pointer = idt + 
						( interrupt_index * sizeof(interrupt_info_t) );
		/* Now disable all interrupts,
		 * we must do it to install a new one */
		__asm { cli };
		/* Write the new interrupt */
		RtlCopyMemory(
			   (void *)int_pointer,
			   new_interrupt,
			   sizeof(interrupt_info_t) );
		/* It's ok now we can enable all interrupts again. */
		__asm { sti };
	}
	__except( 1 ) {
		/* O my, we got an exception :( */
		KdPrint(( "Oregano: set_interrupt: Exception, you are gonna get a blue screen, you know.\r\n" ));
	}

}
#endif

ADDRESS getInterruptAddress( IN interrupt_info_t * interruptInfo )
{
#ifdef i386
    return (ADDRESS)(
            (interruptInfo->high_offset << 16) |
             interruptInfo->low_offset );
#elif AMD64
    return (ADDRESS)(
            ((unsigned long long)interruptInfo->high_offset << 32) |
            ((unsigned long long)interruptInfo->middle_offset << 16) |
             (unsigned long long)interruptInfo->low_offset );
#endif
}

KEVENT              InterruptsHookSyncEvent = {0};
unsigned char       InterruptToHook = 0;
interrupt_info_t *  NewInterruptInfo = NULL;
unsigned int        NumOfHookedProcessors = 0;

KSTART_ROUTINE hookInterruptFromGlobalInfo;
void hookInterruptFromGlobalInfo(_In_ PVOID startContext)
{
    idt_t               idtr = {0};
    interrupt_info_t    currentInterruptInfo;
    ADDRESS             currentInterruptAddress;
    ADDRESS             hookInterruptAddress;

    UNREFERENCED_PARAMETER(startContext);

    #ifndef AMD64
    load_idt( &idtr );
    #else
    loadIdt64( &idtr );
    #endif
    KdPrint(( "Oregano: hookInterruptFromGlobalInfo: idtr is 0x%p\r\n", idtr.base ));

    get_interrupt_info( &idtr, InterruptToHook, &currentInterruptInfo );
    currentInterruptAddress     = getInterruptAddress( &currentInterruptInfo );
    hookInterruptAddress        = getInterruptAddress( NewInterruptInfo );
    if (currentInterruptAddress == hookInterruptAddress) {
        KdPrint(( "Oregano: hookInterruptFromGlobalInfo: Interrupt already hooked\r\n" ));
        goto HOOK_INTERRUPT_FROM_GLOBAL_INFO_DONE;
    }

    KdPrint((
            "Oregano: Hooking Interrupt 0x%02x 0x%p with 0x%p\r\n", 
            InterruptToHook, 
            currentInterruptAddress,
            NewInterruptInfo ));
    #ifndef AMD64
    set_interrupt( idtr.base, InterruptToHook, NewInterruptInfo );
    #else
    setInterrupt64( idtr.base, InterruptToHook, NewInterruptInfo );
    #endif

    ++NumOfHookedProcessors;
HOOK_INTERRUPT_FROM_GLOBAL_INFO_DONE:
    KeSetEvent( &InterruptsHookSyncEvent, 0, FALSE );
    PsTerminateSystemThread(0);
    return;
}

/* Code from rootkit arsenal page 272 */
void hookAllCPUs(
                IN  unsigned char       interruptIndex,
                IN  interrupt_info_t *  newInterrupt )
{
    HANDLE              threadHandle = 0;
    idt_t               idtr = {0};
    interrupt_info_t    oldInterrupt = {0};
    unsigned int        numOfProcessors = 0;

    /* Get current interrupt and check that the hook is not set yet */
    #ifndef AMD64
    load_idt( &idtr );
    #else
    loadIdt64( &idtr );
    #endif
    get_interrupt_info( &idtr, interruptIndex, &oldInterrupt );
    if (getInterruptAddress(&oldInterrupt) == getInterruptAddress(newInterrupt)) {
        KdPrint(( "Oregano: hookAllCPUs: Hook is already set\r\n" ));
        return;
    }

    /* We need to hook the IDT on every processor */
    numOfProcessors = KeNumberProcessors;
    KdPrint(( "Oregano: hookAllCPUs: hooking %d processors\r\n", numOfProcessors ));

    /* We are going to try to create thread by thread until we get to run on all CPUs.
     * We use InterruptsHookSyncEvent to sync all threads */
    /* Set global vars that are accessed from the global thread procedure */
    InterruptToHook = interruptIndex;
    NewInterruptInfo = newInterrupt;
    NumOfHookedProcessors = 0;
    KeInitializeEvent( &InterruptsHookSyncEvent, SynchronizationEvent, FALSE );
    while( NumOfHookedProcessors < numOfProcessors )
    {
        NTSTATUS apiResult = PsCreateSystemThread(
                                        &threadHandle,
                                        (ACCESS_MASK)0,
                                        NULL,
                                        NULL,
                                        NULL,
                                        (PKSTART_ROUTINE)hookInterruptFromGlobalInfo,
                                        NULL );
        if (!NT_SUCCESS(apiResult))
        {
            KdPrint(("Oregano: hookAllCPUs: Failed to create thread!\r\n"));
            break;
        }
        /* Don't lunch a new thread until the last one is done */
        apiResult = KeWaitForSingleObject(
                        &InterruptsHookSyncEvent,
                        Executive,
                        KernelMode,
                        FALSE,
                        NULL );
        if (!NT_SUCCESS(apiResult))
        {
            KdPrint(("Oregano: hookAllCPUs: Failed to wait on single object!\r\n"));
            break;
        }
    }

    KeSetEvent(&InterruptsHookSyncEvent, 0, FALSE);
    KdPrint(( "Oregano: hookAllCPUs: Done hooking all IDTs\r\n" ));
    return;
}



