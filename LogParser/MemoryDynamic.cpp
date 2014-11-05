
#include <assert.h>

#include "MemoryDynamic.hpp"

int compareByteInTimeCycles( ByteInTime const * x, Cycle cycle )
{
    return !(x->cycle == cycle);
}

int compareByteInTimeAddress( ByteInTime const * x, ADDRESS addr )
{
    return !(x->addr == addr);
}

MemoryDynamic::MemoryDynamic(PageIndex rootPage, PagedDataContainer * dc)
    : 
    MemoryBase(rootPage, dc),
    cav(NULL),
    acv(NULL)
{
    createRootPage();
}


MemoryDynamic::~MemoryDynamic(void)
{
    if ( NULL != cav )
    {
        delete cav;
        cav = NULL;
    }
    if ( NULL != acv ) {
        delete acv;
        acv = NULL;
    }
}

void MemoryDynamic::createRootPage()
{
    // rootPageIndex is set at the constructor of the base class
    rootPage = (MemoryDynamicRootPage *)dc->obtainPage(rootPageIndex);
    if (0 == rootPage->cavRootPage) {
        dc->newConsecutiveData(&rootPage->cavRootPage, CAV_HASH_TABLE_SIZE * sizeof(PageIndex));
        dc->releasePage(rootPage->cavRootPage);
    }
    if (0 == rootPage->acvRootPage)
    {
        dc->newConsecutiveData(&rootPage->acvRootPage, ACV_HASH_TABLE_SIZE * sizeof(PageIndex));
        dc->releasePage(rootPage->acvRootPage);
    }
    cav = new HashTableByCycle(rootPage->cavRootPage, dc, 'CAV0');
    acv = new HashTableByAddr (rootPage->acvRootPage, dc, 'ACV0');
}

void MemoryDynamic::setByte( Address address, BYTE value )
{
    ByteInTime byteInTime(address, value);
    cav->append(byteInTime);
    acv->append(byteInTime);
}

void MemoryDynamic::setByte( Cycle cycle, ADDRESS addr, BYTE value )
{
    ByteInTime byteInTime(cycle, addr, value);
    cav->append(byteInTime);
    acv->append(byteInTime);
}

BYTE MemoryDynamic::getByte( Cycle cycle, ADDRESS addr )
{
    HashTableByAddrIter * iter = new HashTableByAddrIter(acv, addr, 'DMI0');
    assert(NULL != iter);
    BYTE result = UNKNOWN_BYTE;
	ByteInTime const * nextItem = NULL;
	ByteInTime const * currentItem = iter->current();
	assert(NULL != currentItem); // Should not happen because I've checked that byte is known.
	do
	{
		iter->next();
		nextItem = iter->current();
		
		if ( (currentItem->cycle <= cycle) && (
			 (NULL == nextItem) || (nextItem->cycle > cycle)) ) {

				 // Found byte
				 result = currentItem->value;
				 break;
		}

		currentItem = nextItem;
	} while( NULL != nextItem );

	delete iter;
    return result;
}

BOOL MemoryDynamic::isByteKnown( Cycle cycle, ADDRESS addr )
{
    HashTableByAddrIter * iter = new HashTableByAddrIter(acv, addr, 'DMN0');
    assert(NULL != iter);
    BOOL result = FALSE;
    for (ByteInTime const * item = iter->current(); NULL != item; iter->next(), item = iter->current()) {
        if (item->cycle < cycle) {
            result = TRUE;
            break;
        }
    }
    delete iter;
    return result;
}

BOOL MemoryDynamic::isByteKnown( ADDRESS addr )
{
    HashTableByAddrIter * iter = new HashTableByAddrIter(acv, addr, 'DMK0');
    assert(NULL != iter);
    BOOL result;
    ByteInTime const * item = iter->current();
    if (NULL != item) {
        result = TRUE;
    } else {
        result = FALSE;
    }
    delete iter;
    return result;
}

HashTableByCycleIter * MemoryDynamic::getAddressesOfCycle( Cycle cycle )
{
    return new HashTableByCycleIter(cav, cycle, 'HCI0');
}

HashTableByAddrIter * MemoryDynamic::getCyclesOfAddress( ADDRESS addr )
{
    return new HashTableByAddrIter(acv, addr, 'HAI0');
}

StatisticsInfo * MemoryDynamic::statistics()
{
	StatisticsInfo * result = new StatisticsInfo();
	// One for root page
	result->totalPages = 1;
	result->pagesInUse = 1;

	if (NULL != cav)
	{
		GET_AND_ADD_STATS(result, cav);
	}
	if (NULL != acv)
	{
		GET_AND_ADD_STATS(result, acv);
	}

	return result;
}
