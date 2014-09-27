
#pragma once

#include "PagedDataContainer.hpp"
#include "GlobalDefines.hpp"
#include "Address.hpp"
#include "StatisticsInfo.hpp"

class MemoryBase
{
public:
    MemoryBase(PageIndex rootPage, PagedDataContainer * dc);
    virtual ~MemoryBase(void);
    virtual BYTE getByte(Address address) = 0;
    virtual BYTE getByte(Cycle cycle, ADDRESS addr) = 0;
    virtual BOOL isByteKnown(Address address) = 0;
    virtual BOOL isByteKnown(Cycle cycle, ADDRESS addr) = 0;
    virtual BOOL isByteKnown(ADDRESS addr) = 0;
    virtual void endOfData() = 0;
	virtual StatisticsInfo * statistics() = 0;

protected:
    PagedDataContainer * dc;
    PageIndex rootPageIndex;

    virtual void createRootPage() = 0;
};

