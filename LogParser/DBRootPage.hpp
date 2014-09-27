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
    PageIndex threadIdRootPage;
    PageIndex pairsRootPage;
    PageIndex memoryRootPage;
};
#pragma pack()