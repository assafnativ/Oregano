#pragma once

#include <windows.h>
#include "GlobalDefines.hpp"

#pragma pack(1)
struct DBRootPage
{
    DWORD oreganoMagic;
    DWORD version;
    DWORD logVersion;
    DWORD processorType;
    DWORD logHasMemory;
    DWORD reserved[0x5];
    Cycle lastCycle;
    PageIndex eipRootPage;
#ifdef X86
    PageIndex ediRootPage;
    PageIndex esiRootPage;
    PageIndex ebpRootPage;
    PageIndex ebxRootPage;
    PageIndex edxRootPage;
    PageIndex ecxRootPage;
    PageIndex eaxRootPage;
    PageIndex ecsRootPage;
    PageIndex eflagsRootPage;
    PageIndex espRootPage;
#elif AMD64
    PageIndex rdiRootPage;
    PageIndex rsiRootPage;
    PageIndex rbpRootPage;
    PageIndex rbxRootPage;
    PageIndex rdxRootPage;
    PageIndex rcxRootPage;
    PageIndex raxRootPage;
    PageIndex r8RootPage;
    PageIndex r9RootPage;
    PageIndex r10RootPage;
    PageIndex r11RootPage;
    PageIndex r12RootPage;
    PageIndex r13RootPage;
    PageIndex r14RootPage;
    PageIndex r15RootPage;
    PageIndex rcsRootPage;
    PageIndex rflagsRootPage;
    PageIndex rspRootPage;
    PageIndex rssRootPage;
#endif
    PageIndex threadIdRootPage;
    PageIndex pairsRootPage;
    PageIndex memoryRootPage;
};
#pragma pack()
