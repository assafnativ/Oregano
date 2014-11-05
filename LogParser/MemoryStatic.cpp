
#include <assert.h>

#include "MemoryStatic.hpp"
#include "LogConsts.hpp"

MemoryStatic::MemoryStatic(PageIndex rootPage, PagedDataContainer * dc)
    : 
    MemoryBase(rootPage, dc),
    numRegions(0)
{
    createRootPage();
}


MemoryStatic::~MemoryStatic(void)
{
    DataRegionInfo const * regionInfo;
    RegionsListIter * regionsIter = new RegionsListIter(regions, 'SMI0');
    for (regionInfo = regionsIter->current(); NULL != regionInfo; regionsIter->next(), regionInfo = regionsIter->current()) {
        dc->releasePage(regionInfo->dataPageIndex);
        regionsData[regionInfo->privateIndex] = NULL;
    }
    delete regionsIter;
    delete regions;
}

void MemoryStatic::setDataChunk( const ADDRESS address, const DWORD dataLength, const BYTE * data )
{
    DataRegionInfo newRegion;
    newRegion.address       = address;
    newRegion.length        = dataLength;
    newRegion.privateIndex  = numRegions;
    numRegions += 1;
    assert(numRegions < MAX_REGIONS);
    BYTE * regionData = dc->newConsecutiveData(&newRegion.dataPageIndex, dataLength);
    DEBUG_ONLY(dc->setPageTag(newRegion.dataPageIndex, 'MSR0'));
    memcpy(regionData, data, dataLength);
    regions->append(newRegion);
    regionsData[newRegion.privateIndex] = regionData;
    // For now we keep the static data paged in all the time
    //dc->releasePage(newRegion.dataPageIndex);
}

BOOL MemoryStatic::isByteKnown( const ADDRESS address )
{
    BOOL result = FALSE;
    DataRegionInfo const * regionInfo;
    RegionsListIter * regionsIter = new RegionsListIter(regions, 'MRI0');
    for (regionInfo = regionsIter->current(); NULL != regionInfo; regionsIter->next(), regionInfo = regionsIter->current()) {
        if ((regionInfo->address <= address) && ((regionInfo->address + regionInfo->length) > address)) {
            result = TRUE;
            break;
        }
    }
    delete regionsIter;
    return result;
}

void MemoryStatic::createRootPage()
{
    regions = new RegionsList(rootPageIndex, dc, 'RGL0');
    // Load regions that are already set in DB
    DataRegionInfo const * regionInfo;
    RegionsListIter * regionsIter = new RegionsListIter(regions, 'RLI0');
    for (regionInfo = regionsIter->current(); NULL != regionInfo; regionsIter->next(), regionInfo = regionsIter->current()) {
        regionsData[regionInfo->privateIndex] = dc->obtainConsecutiveData(regionInfo->dataPageIndex, regionInfo->length);
        DEBUG_ONLY(dc->setPageTag(regionInfo->dataPageIndex, 'RSME'));
        if (numRegions <= regionInfo->privateIndex) {
            numRegions = regionInfo->privateIndex + 1;
        }
    }
    delete regionsIter;
}

BYTE MemoryStatic::getByte( ADDRESS addr )
{
    BYTE result = UNKNOWN_BYTE;
    BYTE * memPtr = getMemoryPointer(addr);
    if (NULL != memPtr) {
        result = *memPtr;
    }
    return result;    
}

BYTE * MemoryStatic::getMemoryPointer( ADDRESS addr )
{
    BYTE * result = NULL;
    DataRegionInfo const * regionInfo;
    RegionsListIter * regionsIter = new RegionsListIter(regions, 'SMI0');
    for (regionInfo = regionsIter->current(); NULL != regionInfo; regionsIter->next(), regionInfo = regionsIter->current()) {
        if ((regionInfo->address <= addr) && ((regionInfo->address + regionInfo->length) > addr)) {
            OFFSET offset = (OFFSET)(addr - regionInfo->address);
            result = regionsData[regionInfo->privateIndex] + offset;
            break;
        }
    }
    delete regionsIter;
    return result;
}

StatisticsInfo * MemoryStatic::statistics()
{
	StatisticsInfo * result = new StatisticsInfo();
	// One for root page
	result->totalPages = 1;
	result->pagesInUse = 1;

	if (NULL != regions)
	{
		GET_AND_ADD_STATS(result, regions);
	}

	return result;
}
