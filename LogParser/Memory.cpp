
#include <assert.h>

#include "Memory.hpp"
#include "LogConsts.hpp"

Memory::Memory(PageIndex rootPageIndex, PagedDataContainer * dc)
    : rootPageIndex(rootPageIndex),
    dc(dc)
{
    rootPage = (MemoryRootPage *)dc->obtainPage(rootPageIndex);
    dc->setPageTag(rootPageIndex, 'mrot');
    if (0 == rootPage->memoryStaticRootPage) {
        dc->newPage(&rootPage->memoryStaticRootPage);
        dc->setPageTag(rootPage->memoryStaticRootPage, 'srot');
        dc->releasePage(rootPage->memoryStaticRootPage);
    }
    if (0 == rootPage->memoryDynamicRootPage) {
        dc->newPage(&rootPage->memoryDynamicRootPage);
        dc->setPageTag(rootPage->memoryDynamicRootPage, 'drot');
        dc->releasePage(rootPage->memoryDynamicRootPage);
    }
    if (0 == rootPage->pairsCacheRootPage) {
        dc->newPage(&rootPage->pairsCacheRootPage);
        dc->setPageTag(rootPage->pairsCacheRootPage, 'crot');
        dc->releasePage(rootPage->pairsCacheRootPage);
    }
    staticMem  = new MemoryStatic (rootPage->memoryStaticRootPage, dc);
    dynamicMem = new MemoryDynamic(rootPage->memoryDynamicRootPage, dc);
    pairsCache = new PairsCache   (rootPage->pairsCacheRootPage, dc, 'PC_0');
}

Memory::~Memory()
{
    delete staticMem;
    delete dynamicMem;
    delete pairsCache;

    staticMem  = NULL;
    dynamicMem = NULL;
    pairsCache = NULL;

    dc->releasePage(rootPage->memoryStaticRootPage);
    dc->releasePage(rootPage->memoryDynamicRootPage);
    dc->releasePage(rootPage->pairsCacheRootPage);
}

BYTE Memory::getByte( Cycle cycle, ADDRESS addr )
{
    if (dynamicMem->isByteKnown(addr)) {
        return dynamicMem->getByte(cycle, addr);
    }
    if (staticMem->isByteKnown(addr)) {
        return staticMem->getByte(addr);
    }
    return UNKNOWN_BYTE;
}

BYTE * Memory::getStaticMemoryPointer( ADDRESS addr )
{
    return staticMem->getMemoryPointer( addr );
}

WORD Memory::getWord( Cycle cycle, ADDRESS addr )
{
    return getByte(cycle, addr) + (getByte(cycle, addr+1) * 0x100);
}

DWORD Memory::getDword( Cycle cycle, ADDRESS addr )
{
    return 
        (getByte(cycle, addr)) + 
        (getByte(cycle, addr+1) * 0x100) +
        (getByte(cycle, addr+2) * 0x10000) +
        (getByte(cycle, addr+3) * 0x1000000);
}

QWORD Memory::getQword( Cycle cycle, ADDRESS addr )
{
    return 
        (getByte(cycle, addr)) + 
        (getByte(cycle, addr+1) * 0x100) +
        (getByte(cycle, addr+2) * 0x10000) +
        (getByte(cycle, addr+3) * 0x1000000) +
        (getByte(cycle, addr+4) * 0x100000000) +
        (getByte(cycle, addr+5) * 0x10000000000) +
        (getByte(cycle, addr+6) * 0x1000000000000) +
        (getByte(cycle, addr+7) * 0x100000000000000);
}

BOOL Memory::isMemoryKnown( const Cycle cycle, const ADDRESS address )
{
    if (dynamicMem->isByteKnown(cycle, address) || staticMem->isByteKnown(address)) {
        return TRUE;
    }
    return FALSE;
}

void Memory::endOfData()
{
    dynamicMem->endOfData();
    staticMem->endOfData();
}

StatisticsInfo * Memory::statistics()
{
	StatisticsInfo * result = new StatisticsInfo;
	// One for the root page
	result->totalPages = 1;
	result->pagesInUse = 1;

	if (NULL != pairsCache)
	{
		GET_AND_ADD_STATS(result, pairsCache);
	}
	if (NULL != dynamicMem)
	{
		GET_AND_ADD_STATS(result, dynamicMem);
	}
	if (NULL != staticMem)
	{
		GET_AND_ADD_STATS(result, staticMem);
	}

	return result;

}

FindChangingCycles::FindChangingCycles(Memory * memory, ADDRESS addr, Cycle startCycle, Cycle endCycle)
					: 
                    mem(memory),
                    iter(NULL),
                    currentItem(NULL),
                    addr(addr),
                    bottomCycle(startCycle),
                    topCycle(endCycle)
{
    restartSearch();
}


void FindChangingCycles::releaseIter()
{
    if (NULL != iter) {
        delete iter;
        iter = NULL;
    }
    currentItem = NULL;
}

void FindChangingCycles::restartSearch()
{
    releaseIter();
    iter = mem->dynamicMem->getCyclesOfAddress(addr);
    findNext();
}

Cycle FindChangingCycles::current()
{
    if (NULL != currentItem) {
        return currentItem->cycle;
    }
    return INVALID_CYCLE;
}

void FindChangingCycles::next() 
{
    iter->next();
    FindChangingCycles::findNext();
}

void FindChangingCycles::findNext()
{
    for (
            currentItem = iter->current();
            NULL != currentItem;
            iter->next(), currentItem = iter->current() )
    {
        if (currentItem->cycle > bottomCycle) {
            break;
        }
    }
    if (NULL == currentItem) {
        releaseIter();
    }
}

FindData::FindData(Memory * memory, BYTE const * data, DWORD dataLength, Cycle startCycle, Cycle endCycle)
			: 
            mem(memory),
            target(data),
            targetLength(dataLength),
            bottomCycle(startCycle),
            topCycle(endCycle),
            pairsIter(NULL),
            addrValuesIters(NULL),
            byteInTime(NULL),
            byteCyclesRange(NULL)
{
    // Both startCycle and endCycle must be valid
    pair = data[0] + (data[1] * 0x100);
    startIndex = mem->pairsCache->bsearchIndex(pair, bottomCycle);
    restartSearch();
}

FindData::~FindData()
{
    releaseIter();
}

void FindData::releaseIter()
{
    if (NULL != pairsIter) {
        delete pairsIter;
        pairsIter = NULL;
    }
    if (NULL != addrValuesIters) {
	    deleteValuesIter();
        delete [] addrValuesIters;
        addrValuesIters = NULL;
    }
    if (NULL != byteInTime)
    {
        delete [] byteInTime;
        byteInTime = NULL;
    }
    if (NULL != byteCyclesRange)
    {
        delete [] byteCyclesRange;
        byteCyclesRange = NULL;
    }
    currentTop      = 0;
    currentPair     = NULL;
	currentItem.clear();
}

void FindData::restartSearch()
{
    releaseIter();
    pairsIter = new PairsBucketIter(mem->pairsCache->getBucket(pair), startIndex);
    addrValuesIters = new HashTableByAddrIter *[targetLength];
    byteInTime      = new ByteInTime[targetLength];
    byteCyclesRange = new CyclesRange[targetLength];
	for (DWORD i = 0; i < targetLength; ++i) {
		addrValuesIters[i]	= NULL;
		byteInTime[i].addr	= 0;
		byteInTime[i].cycle = INVALID_CYCLE;
		byteInTime[i].value = 0;
		byteCyclesRange[i].bottom	= bottomCycle;
		byteCyclesRange[i].top		= topCycle;
	}
    deleteValuesIter();
    currentPair = NULL;
	currentItem.clear();
	next();
}

void FindData::allocateValuesIter(ADDRESS addr)
{
    for (DWORD byteIndex = 0; byteIndex < targetLength; ++byteIndex) {
        if (NULL != addrValuesIters[byteIndex])
        {
            delete addrValuesIters[byteIndex];
            addrValuesIters[byteIndex] = NULL;
        }
		byteInTime[byteIndex].clear();
        byteCyclesRange[byteIndex].bottom = bottomCycle;
        byteCyclesRange[byteIndex].top    = topCycle;
    }
}

void FindData::deleteValuesIter()
{
    for (DWORD byteIndex = 0; byteIndex < targetLength; ++byteIndex)
    {
        if (NULL != addrValuesIters[byteIndex]) {
            delete addrValuesIters[byteIndex];
            addrValuesIters[byteIndex] = NULL;
        }
        byteInTime[byteIndex].addr  = 0;
        byteInTime[byteIndex].cycle = 0;
        byteInTime[byteIndex].value = 0;
        byteCyclesRange[byteIndex].bottom = bottomCycle;
        byteCyclesRange[byteIndex].top    = topCycle;
    }
}

void FindData::advanceByteIter(int index)
{
	byteInTime[index].copy(addrValuesIters[index]->current());
	addrValuesIters[index]->next();
}

BOOL FindData::cmpBytesInCyclesRange()
{
    // All items at index > currentOffset contains the right value in the current range
    int byteIndex = targetLength - 1;
    ByteInTime * currentValue = NULL;
    while (byteIndex >= 0)
    {
        if (NULL == addrValuesIters[byteIndex]) {
			addrValuesIters[byteIndex] = mem->dynamicMem->getCyclesOfAddress(currentItem.addr + byteIndex);
			advanceByteIter(byteIndex);
        }
        currentValue = &byteInTime[byteIndex];
        ByteInTime const * nextValue = addrValuesIters[byteIndex]->current();
        while (INVALID_CYCLE != currentValue->cycle)
        {
            if (
                (currentValue->value == target[byteIndex]) &&
                (currentValue->cycle <= currentTop) &&
                (   (NULL == nextValue) || (nextValue->cycle <= currentTop) ) )
            {
                break;
            }
			advanceByteIter(byteIndex);
            nextValue = addrValuesIters[byteIndex]->current();
            // Restart of the following bytes
            for (int i = byteIndex - 1; i >= 0; --i)
            {
                if (NULL != addrValuesIters[i]) {
                    delete addrValuesIters[i];
                    addrValuesIters[i] = NULL;
                    byteCyclesRange[i].bottom = bottomCycle;
                    byteCyclesRange[i].top    = topCycle;
                }
            }
        }
        if (INVALID_CYCLE == currentValue->cycle)
        {
			if (NULL != addrValuesIters[byteIndex]) {
				delete addrValuesIters[byteIndex];
				addrValuesIters[byteIndex] = NULL;
			}
            byteIndex++;
            if ((DWORD)byteIndex >= targetLength) 
            {
                return FALSE;
            } else {
                currentItem.cycle = byteCyclesRange[byteIndex].bottom;
                currentTop        = byteCyclesRange[byteIndex].top;
				advanceByteIter(byteIndex);
            }
        }
        else {
            if (0 < byteIndex)
            {
				int nextByteIndex = byteIndex - 1;
                currentItem.cycle = max(currentItem.cycle, currentValue->cycle);
                byteCyclesRange[nextByteIndex].bottom = currentItem.cycle;
                if (NULL == nextValue) {
                    byteCyclesRange[nextByteIndex].top = currentTop;
                } else {
                    currentTop = min(currentTop, nextValue->cycle);
                    byteCyclesRange[nextByteIndex].top = currentTop;
                }
            }
            byteIndex--;
        }
    }
    assert(NULL != currentValue);
    currentItem.cycle = max(currentItem.cycle, currentValue->cycle);
    return TRUE;
}

void FindData::next()
{
    if (NULL == pairsIter) {
		// Search ended
        return;
    }
    if (NULL != currentPair)
    {
        assert(NULL != addrValuesIters[0]);
		// Advance the first byte to next value
		advanceByteIter(0);
        if (TRUE == cmpBytesInCyclesRange())
        {
			// Yield result
            return;
        }
        deleteValuesIter();
		pairsIter->next();
    }
    currentPair = pairsIter->current();
    while (NULL != currentPair) {
		currentItem.addr   = currentPair->addr;
        currentItem.cycle  = max(bottomCycle, currentPair->cycle);
        if (topCycle <= currentItem.cycle) {
			// Passed the topCycle, no more pairs in range
            break;
        }
        currentTop = topCycle;
		allocateValuesIter(currentItem.addr);
        if (TRUE == cmpBytesInCyclesRange()) {
			// Yield result
            return;
        }
        deleteValuesIter();
        pairsIter->next();
        currentPair = pairsIter->current();
    }
    releaseIter();
}

Address const * FindData::current()
{
    return &currentItem;
}
