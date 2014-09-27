
#pragma once

#include <windows.h>

#include "RegLog.hpp"

// Returns an index
DWORD RegLog::bsearchByCycle( DWORD cycle )
{
	if (0 == (*numItems)) {
		return 0;
	}
	DWORD lo = 0;
	DWORD hi = (*numItems) - 1;
	DWORD mid;
	DWORD midCycle;

	while (lo < hi) {
		mid = (lo + hi) / 2;
		midCycle = getItem(mid).cycle;
		if (midCycle < cycle) {
			lo = mid + 1;
		} else if (midCycle > cycle) {
			hi = mid;
		} else {
			return mid + 1;
		}
	}
    // Prefer the cycle before
    if (getItem(lo).cycle <= cycle) {
        return lo;
    }
	if (0 == lo)
	{
		return INVALID_CYCLE;
	}
    return lo - 1;
}

RegLogIter::RegLogIter( RegLog * regLog, DWORD startCycle/* =0 */ )
    : regLog(regLog)
{
	if (0 == regLog->getNumItems()) {
        currentIndex = INVALID_CYCLE;
        currentCycle = INVALID_CYCLE;
	} else if (0 == startCycle) {
        currentIndex = 0;
        currentCycle = 0;
	} else {
        currentIndex = regLog->bsearchByCycle(startCycle);
        if (currentIndex < regLog->getNumItems()) {
            currentCycle = regLog->getItem(currentIndex).cycle;
        } else {
            currentIndex = INVALID_CYCLE;
            currentCycle = INVALID_CYCLE;
        }
    }
}

void RegLogIter::next()
{
    currentIndex += 1;
    if (currentIndex >= regLog->getNumItems()) {
        currentCycle = INVALID_CYCLE;
        currentIndex = INVALID_CYCLE;
    } else {
        currentCycle = regLog->getItem(currentIndex).cycle;
    }
}

void RegLogIter::prev()
{
    if ((currentCycle != INVALID_CYCLE) && (0 < currentIndex)) {
        currentIndex -= 1;
        currentCycle = regLog->getItem(currentIndex).cycle;
    } else {
        currentIndex = INVALID_CYCLE;
        currentCycle = INVALID_CYCLE;
    }
}
