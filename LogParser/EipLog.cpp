
#include "stdafx.h"

#include "EipLog.hpp"



EipLogIter::EipLogIter( EipLog * eipLog, DWORD startCycle/*=0 */ )
    : eipLog(eipLog)
{
    // Remember in EIP, cycle and index are the same
    DWORD maxCycle = eipLog->getNumItems();
    if (maxCycle <= startCycle) {
        currentCycle = INVALID_CYCLE;
    } else {
        currentCycle = startCycle;
    }
}

void EipLogIter::next()
{
    currentCycle += 1;
    if (currentCycle >= eipLog->getNumItems()) {
        currentCycle = INVALID_CYCLE;
    }
}

void EipLogIter::prev()
{
    if (INVALID_CYCLE == currentCycle) {
        return;
    } else if (0 < currentCycle) {
        currentCycle -= 1;
    } else {
        currentCycle = INVALID_CYCLE;
        return;
    }
}



