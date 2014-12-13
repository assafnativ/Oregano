
#pragma once

#include <windows.h>

#ifdef X86
    typedef unsigned long MACHINE_LONG;
#elif AMD64
    typedef unsigned long long MACHINE_LONG;
#else
#pragma(error, 0)
#endif

typedef unsigned long long QWORD;

typedef MACHINE_LONG ADDRESS;
typedef DWORD OFFSET;
typedef DWORD Cycle;
typedef DWORD PageIndex;

struct CyclesRange
{
    Cycle top;
    Cycle bottom;
};

// http://stackoverflow.com/questions/14698350/x86-64-asm-maximum-bytes-for-an-instruction
#ifdef X86
    static const DWORD MAX_OPCODE_LENGTH (12);
#elif AMD64
    static const DWORD MAX_OPCODE_LENGTH (15);
#else
#   pragma(error, 0)
#endif

#ifndef NULL
#   ifdef __cplusplus
#       define NULL    0
#   else
#       define NULL    ((void *)0)
#   endif
#endif

#ifdef _DEBUG
static const CHAR ZERO_BUFFER_FOR_COMPARE[0x100] = {0};
#endif

#ifdef _DEBUG
#define DEBUG_ONLY(x) (x)
#define DEBUG_PAGE_TAG(INDEX, TAG) (dc->setPageTag(INDEX, TAG))
#else
#define DEBUG_ONLY(x)
#define DEBUG_PAGE_TAG(INDEX, TAG)
#endif
