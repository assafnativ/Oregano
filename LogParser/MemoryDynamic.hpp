#pragma once

#include "MemoryBase.hpp"
#include "Address.hpp"
#include "PagedHashTable.hpp"
#include "ByteInTime.hpp"

static const DWORD ACV_HASH_TABLE_SIZE(DEFAULT_HASH_TABLE_SIZE);
static const DWORD CAV_HASH_TABLE_SIZE(DEFAULT_HASH_TABLE_SIZE);
int compareByteInTimeCycles (ByteInTime const * x, Cycle cycle);
int compareByteInTimeAddress(ByteInTime const * x, ADDRESS addr);
typedef PagedHashTable<ByteInTime, ACV_HASH_TABLE_SIZE, Cycle,   ByteInTimeGetCycle,   compareByteInTimeCycles>     HashTableByCycle;
typedef PagedHashTable<ByteInTime, CAV_HASH_TABLE_SIZE, ADDRESS, ByteInTimeGetAddress, compareByteInTimeAddress>    HashTableByAddr;
typedef PagedHashTableIter<ByteInTime, ACV_HASH_TABLE_SIZE, Cycle,   ByteInTimeGetCycle,   compareByteInTimeCycles>     HashTableByCycleIter;
typedef PagedHashTableIter<ByteInTime, CAV_HASH_TABLE_SIZE, ADDRESS, ByteInTimeGetAddress, compareByteInTimeAddress>    HashTableByAddrIter;

class MemoryDynamic :
    public MemoryBase
{
public:
    MemoryDynamic(PageIndex rootPage, PagedDataContainer * dc);
    ~MemoryDynamic(void);

    void setByte(Address address, BYTE value);
    void setByte(Cycle cycle, ADDRESS addr, BYTE value);
    virtual BYTE getByte(Cycle cycle, ADDRESS addr);
    virtual BYTE getByte(Address address) {return getByte(address.cycle, address.addr);};
    virtual BOOL isByteKnown(Cycle cycle, ADDRESS addr);
    virtual BOOL isByteKnown(Address address) {return isByteKnown(address.cycle, address.addr);};
    virtual BOOL isByteKnown(ADDRESS addr);
    virtual void endOfData() {};
    HashTableByCycleIter * getAddressesOfCycle(Cycle cycle); // Allocates
    HashTableByAddrIter  * getCyclesOfAddress(ADDRESS addr); // Allocates

	virtual StatisticsInfo * statistics();

protected:
    class MemoryDynamicRootPage {
        public:
            // Cycle Address Value
            PageIndex   cavRootPage;
            // Address Cycle Value
            PageIndex   acvRootPage;
    };
    MemoryDynamicRootPage   * rootPage;
    HashTableByCycle        * cav;
    HashTableByAddr         * acv;
    virtual void createRootPage();
};

