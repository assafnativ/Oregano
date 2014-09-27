
#pragma once

#include <windows.h>

#include "LogConsts.hpp"
#include "PagedDataContainer.hpp"
#include "Address.hpp"
#include "PairsCache.hpp"
#include "MemoryDynamic.hpp"
#include "MemoryStatic.hpp"

class Memory
{
	public:
		Memory(PageIndex rootPageIndex, PagedDataContainer * dc);
		~Memory();

        void setByte(Address address, BYTE value) {setByte(address.cycle, address.addr, value);};
        void setByte(Cycle cycle, ADDRESS addr, BYTE value);
        BOOL isMemoryKnown(const Cycle cycle, const ADDRESS address);
        BOOL isMemoryKnown(const Address address)
        {
            return isMemoryKnown(address.cycle, address.addr);
        }
        void setStaticDataChunk(const Address address, DWORD dataLength, const BYTE * data) 
        {
            staticMem->setDataChunk(address.addr, dataLength, data);
        }
        void endOfData();
        BYTE getByte(Cycle cycle, ADDRESS addr);
		BYTE getByte(const Address address) {return getByte(address.cycle, address.addr);};
        WORD getWord(Cycle cycle, ADDRESS addr);
        WORD getWord(const Address address) {return getWord(address.cycle, address.addr);};
        DWORD getDword(Cycle cycle, ADDRESS addr);
        DWORD getDword(const Address address) {return getDword(address.cycle, address.addr);};
        QWORD getQword(Cycle cycle, ADDRESS addr);
        QWORD getQword(const Address address) {return getQword(address.cycle, address.addr);};
        
        BYTE * getStaticMemoryPointer(ADDRESS addr);

		StatisticsInfo * statistics();

	protected:
		friend class FindChangingCycles;
		friend class FindData;

        PagedDataContainer * dc;
        class MemoryRootPage {
           public:
               PageIndex    memoryStaticRootPage;
               PageIndex    memoryDynamicRootPage;
               PageIndex    pairsCacheRootPage;
        };
        PageIndex        rootPageIndex;
        MemoryRootPage * rootPage;
        MemoryDynamic *  dynamicMem;
        MemoryStatic *   staticMem;
        PairsCache *     pairsCache;
};

class FindChangingCycles
{
public:
	FindChangingCycles(Memory * memory, ADDRESS addr, Cycle startCycle=0, Cycle endCycle=INVALID_CYCLE);
    void releaseIter();
	void restartSearch();
	inline BOOL isEndOfSearch() {return isDone;};
    Cycle current();
	void next();
private:
    void findNext();
    Memory *	    mem;
    HashTableByAddrIter  * iter;
    ByteInTime const *     currentItem;
    ADDRESS         addr;
	Cycle           bottomCycle;
	Cycle           topCycle;
	PageIndex       topIndex;
    Cycle           data;
    BOOL            isDone;
};

class FindData
{
	public:
		FindData(Memory * memory, BYTE const * data, DWORD dataLength, Cycle startCycle=0, Cycle endCycle=INVALID_CYCLE );
        ~FindData();
		void restartSearch();
		Address const * current();
        void next();
	private:
        BOOL cmpBytesInCyclesRange();
		void advanceByteIter(int index);
        void findNext();
        void releaseIter();
        void deleteValuesIter();
        void allocateValuesIter(ADDRESS addr);

		Memory *			mem;
		BYTE const *		target;
		DWORD				targetLength;
		DWORD				bottomCycle;
		DWORD				topCycle;
        DWORD               startIndex;
        DWORD               pair;
        PairsBucketIter *   pairsIter;
        const Address *     currentPair;
        ByteInTime *        byteInTime;
        CyclesRange *       byteCyclesRange;
        HashTableByAddrIter ** addrValuesIters;
        Address             currentItem;
        Cycle               currentTop;
};
