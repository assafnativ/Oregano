
#ifndef _OFFSETS_H_
#define _OFFSETS_H_

#include "GlobalDefines.h"

typedef struct kpcrcb_offsets_s {
    OFFSET kthread;
} kpcrcb_offsets;

typedef struct thread_context_offsets_s {
    OFFSET ktrapFrameSize;
    OFFSET eflags;
} thread_context_offsets;

typedef struct ethread_offsets_s {
    OFFSET ThreadListEntry; /* Note that this is the ThreadListEntry from the _ETHREAD and not from the _KTHREAD */
    OFFSET Teb;
    OFFSET CrossThreadFlags;
    OFFSET InitialStack;
    OFFSET TrapFrame;
    OFFSET Cid;
    OFFSET PreviousMode;
} ethread_offsets;

typedef struct eprocess_offsets_s {
    OFFSET DirectoryTableBase;
    OFFSET ThreadListHead;
} eprocess_offsets;

typedef struct windows_offsets_s {
    UINT32                  version[4];
    kpcrcb_offsets          kpcrcb;
    thread_context_offsets  threadContext;
    ethread_offsets         ethread;
    eprocess_offsets        eprocess;
} windows_offsets;

windows_offsets * offsets;

windows_offsets * find_windows_offsets(UINT32 * version);

#endif /* _OFFSETS_H_ */