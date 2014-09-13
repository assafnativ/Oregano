
#ifndef _TRAP_INTERRUPT_H_
#define _TRAP_INTERRUPT_H_

#include "GlobalDefines.h"
#include "driver.h"

/* Interrupts global data:
 * Trust me, this is the best way to pass
 * arguments. I know, I don't like it either. */
/* Would be used for calling the original trap interrupt, if needed. */
extern ADDRESS orgTrapInterrupt;
/* Would be used for simulating a breakpoint */
extern ADDRESS orgBreakpointInterrupt;
/* What process are we debugging? */
extern HANDLE targetProcessId;
/* What thread are we debugging, if zero we debug all threads in the process */
HANDLE targetThreadId;
extern void * target_process;	// CR3
/* Where should we stop logging */
extern void * stopAddress;
/* Current logging range */
extern void * bottom_log_address;
extern void * top_log_address;
/* Log buffer, where every opcode is being logged */
extern void * log_buffer;
/* Used buffers are the number of buffers used since last probe */
extern unsigned int used_buffers;
/* Continuer of all log buffers */
extern void * log_buffer_item[LOG_BUFFER_NUM_OF_BUFFERS];
/* A hash table to save threads context */
extern ThreadContext threads[THREAD_CONTEXT_MAX_THREADS];
/* An array of logging ranges, hold sorted */
extern LoggingRange loggingRanges[MAX_LOG_RANGES];
/* Holds the last used context */
extern void * lastContext;
/* Index of current buffer */
extern unsigned int active_log_buffer;
extern unsigned int next_free_log_buffer;
/* Offset to current thread from KPCR */
extern OFFSET kthread_from_kpcr;
#ifdef DEBUG
/* For debugging and shit. */
extern unsigned long DebugVar0;
extern unsigned long DebugVar1;
extern unsigned long DebugVar2;
extern unsigned long DebugVar3;
extern unsigned long DebugVar4;
extern unsigned long DebugVar5;
extern unsigned long DebugVar6;
extern unsigned long DebugVar7;
#endif

/* Functions declarations */
/*
 * trap_interrupt
 * 	
 * 	Description:
 *	 	This function should replace the original trap interrupt.
 * 		The purpose of this function is to log the current opcode,
 * 		and it's affect on memory, registers and anything else that
 * 		might be in the interest of the programmer.
 * 		This function should be as fast, efficient and effective as
 * 		possible, cause it is called once for every opcode running.
 * 		It is written in mostly pure x86 assembly.
 *
 * 	Known issues:
 * 		Because this function replaces the original windows trap interrupt,
 * 		it is impassable to use debuggers single step function while it is running,
 * 		an attempt to do so might cause a BSOD.
 *
 */
extern void trap_interrupt( void );



#endif /* _TRAP_INTERRUPT_H_ */

