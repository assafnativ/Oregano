
#pragma once

#include "memorybase.hpp"
#include "PagedLinkedList.hpp"

class DataRegionInfo
{
public:
    ADDRESS     address;
    DWORD       length;
    PageIndex   dataPageIndex;
    DWORD       privateIndex;
};

typedef PagedLinkedList<DataRegionInfo> RegionsList;
typedef PagedLinkedListIter<DataRegionInfo>  RegionsListIter;

class MemoryStatic :
    public MemoryBase
{
public:
    MemoryStatic(PageIndex rootPage, PagedDataContainer * dc);
    ~MemoryStatic(void);

    void setDataChunk(const ADDRESS address, const DWORD dataLength, const BYTE * data);
    BYTE getByte(ADDRESS addr);
    virtual BYTE getByte(Address address) {return getByte(address.addr);};
    virtual BYTE getByte(Cycle cycle, ADDRESS addr) {return getByte(addr);};
    virtual BOOL isByteKnown(ADDRESS addr);
    virtual BOOL isByteKnown(Address address) {return isByteKnown(address.addr);};
    virtual BOOL isByteKnown(Cycle cycle, ADDRESS addr) {return isByteKnown(addr);};
    virtual void endOfData() {};
    BYTE * getMemoryPointer(ADDRESS addr);

	virtual StatisticsInfo * statistics();

protected:
    static const DWORD MAX_REGIONS = 0x400;

    class MemoryStaticRootPage
    {
    public:
        PageIndex IndexesListRootPageIndex;
    };
    virtual void createRootPage();
    RegionsList * regions;
    DWORD numRegions;
    BYTE * regionsData[MAX_REGIONS];
};

