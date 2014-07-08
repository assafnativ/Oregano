
#ifndef _CONTROL_THREAD_CONTEXT_H_
#define _CONTROL_THREAD_CONTEXT_H_

#include "GlobalDefines.h"

#define CONTROL_THREAD_CONTEXT_MEMORY_TAG	((ULONG)'McTC')

// x_FROM_START_OF_TRAP_FRAME are all defined at_KTRAP_FRAME

#ifdef x64
    #define PREVIOUSMODE_FROM_START_OF_TRAP_FRAME       (0x28)
    #define PREVIOUSIRQL_FROM_START_OF_TRAP_FRAME       (0x29)
    #define FAULTINDICATOR_FROM_START_OF_TRAP_FRAME     (0x2A)
    #define RAX_FROM_START_OF_TRAP_FRAME                (0x30)
    #define RCX_FROM_START_OF_TRAP_FRAME                (0x38)
    #define RDX_FROM_START_OF_TRAP_FRAME                (0x40)
    #define R8_FROM_START_OF_TRAP_FRAME                 (0x48)
    #define R9_FROM_START_OF_TRAP_FRAME                 (0x50)
    #define R10_FROM_START_OF_TRAP_FRAME                (0x58)
    #define R11_FROM_START_OF_TRAP_FRAME                (0x60)
    #define FAULTADDRESS_FROM_START_OF_TRAP_FRAME       (0xD0)
    #define DEBUGCONTROL_FROM_START_OF_TRAP_FRAME       (0x108)
    #define SEGDS_FROM_START_OF_TRAP_FRAME              (0x130)
    #define SEGES_FROM_START_OF_TRAP_FRAME              (0x132)
    #define SEGFS_FROM_START_OF_TRAP_FRAME              (0x134)
    #define SEGGS_FROM_START_OF_TRAP_FRAME              (0x136)
    #define TRAPFRAME_FROM_START_OF_TRAP_FRAME          (0x138)
    #define RBX_FROM_START_OF_TRAP_FRAME                (0x140)
    #define RDI_FROM_START_OF_TRAP_FRAME                (0x148)
    #define RSI_FROM_START_OF_TRAP_FRAME                (0x150)
    #define RBP_FROM_START_OF_TRAP_FRAME                (0x158)
    #define ERRORCODE_FROM_START_OF_TRAP_FRAME          (0x160)
    #define RIP_FROM_START_OF_TRAP_FRAME                (0x168)
    #define SEGCS_FROM_START_OF_TRAP_FRAME              (0x170)
    #define EFLAGS_FROM_START_OF_TRAP_FRAME             (0x178)
    #define RSP_FROM_START_OF_TRAP_FRAME                (0x180)
    #define SEGSS_FROM_START_OF_TRAP_FRAME              (0x188)
    #define SIZE_KTRAP_FRAME                            (0x190)
#else
    #define EDX_FROM_START_OF_TRAP_FRAME	    (0x3c)
    #define ECX_FROM_START_OF_TRAP_FRAME	    (0x40)
    #define EAX_FROM_START_OF_TRAP_FRAME	    (0x44)
    #define EDI_FROM_START_OF_TRAP_FRAME	    (0x54)
    #define ESI_FROM_START_OF_TRAP_FRAME	    (0x58)
    #define EBX_FROM_START_OF_TRAP_FRAME	    (0x5C)
    #define EBP_FROM_START_OF_TRAP_FRAME	    (0x60)
    #define ERRCODE_FROM_START_OF_TRAP_FRAME	(0x64)
    #define EIP_FROM_START_OF_TRAP_FRAME    	(0x68)
    #define SEGCS_FROM_START_OF_TRAP_FRAME	    (0x6C)
    #define EFLAGS_FROM_START_OF_TRAP_FRAME	    (0x70)
    #define ESP_FROM_START_OF_TRAP_FRAME        (0x74)
    #define ESS_FROM_START_OF_TRAP_FRAME        (0x78)
#endif

/* The flag in EFlags that sets the single step */
#define TRAP_FLAG						(0x100)
/* TODO: Whats the EFLAGS offset? */

NTSTATUS setTraceFlagForAllThreads  ( HANDLE process_id );
NTSTATUS unsetTraceFlagForAllThreads( HANDLE process_id );
NTSTATUS setTraceFlagForThread      ( HANDLE process_id, HANDLE thread_id );

#endif /* _CONTROL_THREAD_CONTEXT_H_ */
