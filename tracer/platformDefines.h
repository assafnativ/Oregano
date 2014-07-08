
#ifndef _PLATFORM_DEFINES_H_
#define _PLATFORM_DEFINES_H_

#include <ntifs.h>
#include "GlobalDefines.h"
#pragma pack(push, 1)

/*
 * EPROCESS->ThreadListHead offset is found on PsGetNextProcessThread
 * ETHREAD->ThreadListHead offset is found on PsGetNextProcessThread
 * ETHREAD->InitialStack offset is found on MmInPageKernelStack
 * Offset of trap fram from initial kstack is defined at PspGetSetContextSpecialApc (PspGetBaseTrapFrame Macro in the WRK)
 */

#if WINVER < 0x501 // 0x500 Windows 2000, 0x400 Windows NT 4.0 0x351 Windows NT 3.51
    #pragma (error, "Unsupported target Windoes version")

#elif WINVER < 0x502 // 0x501 Windows XP
typedef struct ETHREAD_t {
    ADDRESS     Tcb;            // 0x0
    UINT8       GAP0[0x14];
    ADDRESS     InitialStack;   // 0x18
    ADDRESS     StackLimit;     // 0x1c
    ADDRESS     Teb;            // 0x20
    ADDRESS     TlsArray;       // 0x24
    ADDRESS     KernelStack;    // 0x28
    UINT8       GAP1[0x08];
    KAPC_STATE  ApcState;       // 0x34
    UINT32      ContextSwitches; // 0x4c
    UINT8       IdleSwapBlock;   // 0x50
    UINT8       VdmSafe;         // 0x51
    UINT8       Spare0;         // 0x52
    UINT8       GAP2[0x01];
    UINT32      WaitStatus;     // 0x54
    UINT8       WaitIrql;       // 0x58
    UINT8       WaitMode;       // 0x59
    UINT8       WaitNext;       // 0x05a
    UINT8       WaitReason;     // 0x05b
    UINT32      WaitBlockList;  // 0x05c
    LIST_ENTRY  WaitListEntry;  // 0x60
    UINT32      WaitTime;       // 0x068 
    UINT8       BasePriority;   // 0x06c
    UINT8       DecrementCount; // 0x06d
    UINT8       PriorityDecrement; // 0x06e
    UINT8       Quantum;        // 0x06f
    ADDRESS     WaitBlock;      // 0x70
    UINT8       GAP3[0x5c];
    UINT32      LegoData;       // 0x0d0 
    UINT32      KernelApcDisable; // 0x0d4
    UINT32      UserAffinity;    // 0x0d8
    UINT8       SystemAffinityActive; // 0x0dc
    UINT8       PowerState;     // 0x0dd
    UINT8       NpxIrql;        // 0x0de
    UINT8       InitialNode;    // 0x0df
    UINT32      ServiceTable;   // 0x0e0
    UINT32      Queue;          // 0x0e4
    UINT32      ApcQueueLock;   // 0x0e8
    UINT8       GAP4[0x78];
    UINT8       Alertable;      // 0x164
    UINT8       ApcStateIndex;  // 0x165
    UINT8       ApcQueueable;   // 0x166
    UINT8       AutoAlignment;  // 0x167
    ADDRESS     StackBase;      // 0x168
    KAPC        SuspendApc;     // 0x16c
    KSEMAPHORE  SuspendSemaphore;   // 0x19c
    LIST_ENTRY  KThreadListEntry;    // 0x1b0
    char        FreezeCount;    // 0x1b8
    char        SuspendCount;   // 0x1b9
    UINT8       GAP5[0x72];
    LIST_ENTRY  ThreadListEntry; // 0x22c
    EX_RUNDOWN_REF RundownProtect;  // 0x234
    EX_PUSH_LOCK ThreadLock;    // 0x238 
    UINT32      LpcReplyMessageId;  // 0x23c 
    UINT32      ReadClusterSize;    // 0x240 
    UINT32      GrantedAccess;      // 0x244 
    UINT32      CrossThreadFlags;   // 0x248 
} ETHREAD_s;


typedef struct EPROCESS_t {
    ADDRESS     Pcb;            // 0x00
    UINT8       GAP0[0x14];
    ADDRESS     DirectoryTableBase; // 0x18 (CR3)
    UINT8       GAP1[0x174];
    LIST_ENTRY  ThreadListHead; // 0x190
} EPROCESS_s;

#define START_OF_TRAP_FRAME_FROM_INITIAL_KSTACK	(0x29c)

#elif WINVER < 0x600    // 0x502 Windows 2k3
typedef struct ETHREAD_t {
    ADDRESS     Tcb;            // 0x0
    UINT8       GAP0[0x14];
    ADDRESS     InitialStack;   // 0x18
    ADDRESS     StackLimit;     // 0x1c
    ADDRESS     Teb;            // 0x20
    ADDRESS     TlsArray;       // 0x24
    ADDRESS     KernelStack;    // 0x28
    UINT8       GAP1[0x08];
    KAPC_STATE  ApcState;       // 0x34
    UINT32      ContextSwitches; // 0x4c
    UINT8       IdleSwapBlock;   // 0x50
    UINT8       VdmSafe;         // 0x51
    UINT8       Spare0;         // 0x52
    UINT8       GAP2[0x01];
    UINT32      WaitStatus;     // 0x54
    UINT8       WaitIrql;       // 0x58
    UINT8       WaitMode;       // 0x59
    UINT8       WaitNext;       // 0x05a
    UINT8       WaitReason;     // 0x05b
    UINT32      WaitBlockList;  // 0x05c
    LIST_ENTRY  WaitListEntry;  // 0x60
    UINT32      WaitTime;       // 0x068 
    UINT8       BasePriority;   // 0x06c
    UINT8       DecrementCount; // 0x06d
    UINT8       PriorityDecrement; // 0x06e
    UINT8       Quantum;        // 0x06f
    ADDRESS     WaitBlock;      // 0x70
    UINT8       GAP3[0x5c];
    UINT32      LegoData;       // 0x0d0 
    UINT32      KernelApcDisable; // 0x0d4
    UINT32      UserAffinity;    // 0x0d8
    UINT8       SystemAffinityActive; // 0x0dc
    UINT8       PowerState;     // 0x0dd
    UINT8       NpxIrql;        // 0x0de
    UINT8       InitialNode;    // 0x0df
    UINT32      ServiceTable;   // 0x0e0
    UINT32      Queue;          // 0x0e4
    UINT32      ApcQueueLock;   // 0x0e8
    UINT8       GAP4[0x78];
    UINT8       Alertable;      // 0x164
    UINT8       ApcStateIndex;  // 0x165
    UINT8       ApcQueueable;   // 0x166
    UINT8       AutoAlignment;  // 0x167
    ADDRESS     StackBase;      // 0x168
    KAPC        SuspendApc;     // 0x16c
    KSEMAPHORE  SuspendSemaphore;   // 0x19c
    LIST_ENTRY  KThreadListEntry;    // 0x1b0
    char        FreezeCount;    // 0x1b8
    char        SuspendCount;   // 0x1b9
    UINT8       GAP5[0x6a];
    LIST_ENTRY  ThreadListEntry; // 0x224
    EX_RUNDOWN_REF RundownProtect;  // 0x22c
    EX_PUSH_LOCK ThreadLock;    // 0x230 
    UINT32      LpcReplyMessageId;  // 0x234
    UINT32      ReadClusterSize;    // 0x238 
    UINT32      GrantedAccess;      // 0x23c 
    UINT32      CrossThreadFlags;   // 0x240 
} ETHREAD_s;


typedef struct EPROCESS_t {
    ADDRESS     Pcb;            // 0x00
    UINT8       GAP0[0x14];
    ADDRESS     DirectoryTableBase; // 0x18 (CR3)
    UINT8       GAP1[0x164];
    LIST_ENTRY  ThreadListHead; // 0x180
} EPROCESS_s;

#define START_OF_TRAP_FRAME_FROM_INITIAL_KSTACK	(0x29c)

#elif WINVER < 0x700    // 0x600 Windows Vista, Windows Server 2008, 0x601 Windows 7, Windows 2008 R2
typedef struct ETHREAD_t {
    ADDRESS     Tcb;            // 0x0
    UINT8       GAP0[0x14];
    ADDRESS     InitialStack;   // 0x18
    ADDRESS     StackLimit;     // 0x1c
    ADDRESS     KernelStack;    // 0x20
    UINT32      ThreadLockInt;  // 0x24
    KAPC_STATE  ApcState;       // 0x28
    UINT8       GAP1[0x1c];
    UINT32      ContextSwitches; // 0x48
    UINT8       State;          // 0x4c
    UINT8       NpxState;       // 0x4d
    UINT8       GAP2[0x12];
    ADDRESS     Teb;            // 0x74
    UINT8       GAP3[0x168];
    LIST_ENTRY  ThreadListEntry; // 0x268
    EX_RUNDOWN_REF RundownProtect;  // 0x270
    EX_PUSH_LOCK ThreadLock;    // 0x274
    UINT32      LpcReplyMessageId;  // 0x278
    UINT32      ReadClusterSize;    // 0x27c 
    UINT32      GrantedAccess;      // 0x280 
    UINT32      CrossThreadFlags;   // 0x284 
} ETHREAD_s;

typedef struct EPROCESS_t {
    ADDRESS     Pcb;            // 0x00
    UINT8       GAP0[0x14];
    ADDRESS     DirectoryTableBase; // 0x18 (CR3)
    UINT8       GAP1[0x16c];
    LIST_ENTRY  ThreadListHead; // 0x188
} EPROCESS_s;

#define START_OF_TRAP_FRAME_FROM_INITIAL_KSTACK	(0x29c)

#else
    #pragma(Error, "Platform not supported")
#endif

#pragma pack(pop)


#define PS_CROSS_THREAD_FLAGS_TERMINATED           0x00000001UL
#define PS_CROSS_THREAD_FLAGS_DEADTHREAD           0x00000002UL
#define PS_CROSS_THREAD_FLAGS_HIDEFROMDBG          0x00000004UL
#define PS_CROSS_THREAD_FLAGS_IMPERSONATING        0x00000008UL
#define PS_CROSS_THREAD_FLAGS_SYSTEM               0x00000010UL
#define PS_CROSS_THREAD_FLAGS_HARD_ERRORS_DISABLED 0x00000020UL
#define PS_CROSS_THREAD_FLAGS_BREAK_ON_TERMINATION 0x00000040UL
#define PS_CROSS_THREAD_FLAGS_SKIP_CREATION_MSG    0x00000080UL
#define PS_CROSS_THREAD_FLAGS_SKIP_TERMINATION_MSG 0x00000100UL

#endif /* _PLATFORM_DEFINES_H_ */
