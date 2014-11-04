
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

        void setByte(Address address, BYTE value) { setByte(address.cycle, address.addr, value); }
        void setWord(Address address, WORD value) { setWord(address.cycle, address.addr, value); }
        void setDword(Address address, DWORD value) { setDword(address.cycle, address.addr, value); }
        void setQword(Address address, QWORD value) { setQword(address.cycle, address.addr, value); }
        void setByte(Cycle cycle, ADDRESS addr, BYTE value)  { setMemory<BYTE>(cycle, addr, (BYTE *)&value); }
        void setWord (Cycle cycle, ADDRESS addr, WORD value)  { setMemory<WORD> (cycle, addr, (BYTE *)&value); }
        void setDword(Cycle cycle, ADDRESS addr, DWORD value) { setMemory<DWORD>(cycle, addr, (BYTE *)&value); }
        void setQword(Cycle cycle, ADDRESS addr, QWORD value) { setMemory<QWORD>(cycle, addr, (BYTE *)&value); }
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
		BYTE getByte(const Address address) {return getByte(address.cycle, address.addr);}
        WORD getWord(Cycle cycle, ADDRESS addr);
        WORD getWord(const Address address) {return getWord(address.cycle, address.addr);}
        DWORD getDword(Cycle cycle, ADDRESS addr);
        DWORD getDword(const Address address) {return getDword(address.cycle, address.addr);}
        QWORD getQword(Cycle cycle, ADDRESS addr);
        QWORD getQword(const Address address) {return getQword(address.cycle, address.addr);}
        
        BYTE * getStaticMemoryPointer(ADDRESS addr);

		StatisticsInfo * statistics();

	protected:
        template <class TYPE>
        inline void setMemory(Cycle cycle, ADDRESS addr, BYTE * value)
        {
            for (DWORD i = 0; i < sizeof(TYPE); ++i)
            {
                dynamicMem->setByte(cycle, addr + i, *(value + i));
            }

            // Add to pairs cache
            // First add the pair with the prev byte
            ADDRESS prevAddr = addr - 1;
            BYTE firstByte = *value;
            if (dynamicMem->isByteKnown(MAX_CYCLE, prevAddr))
            {
                BYTE prevValue = dynamicMem->getByte(MAX_CYCLE, prevAddr);
                DWORD key = prevValue + (0x100 * firstByte);
                pairsCache->append(key, cycle, prevAddr);
            }
            else if (staticMem->isByteKnown(prevAddr)) {
                BYTE prevValue = staticMem->getByte(prevAddr);
                DWORD key = prevValue + (0x100 * firstByte);
                pairsCache->append(key, cycle, prevAddr);
            }
            // Add all bytes in between
            if (sizeof(TYPE) > 1)
            {
                BYTE currentByte = *value;
                BYTE nextByte = *(value + 1);
                for (DWORD i = 0; i < (sizeof(TYPE) - 1); ++i)
                {
                    DWORD key = nextByte << 8;
                    key |= currentByte;
                    pairsCache->append(key, cycle, addr + i);
                    currentByte = nextByte;
                    nextByte = *(value + i + 1);
                }
            }

            // Now add the pair with the next byte
            ADDRESS nextAddr = addr + sizeof(TYPE) + 1;
            BYTE lastByte = *(value + sizeof(TYPE) - 1);
            if (dynamicMem->isByteKnown(MAX_CYCLE, nextAddr))
            {
                BYTE nextValue = dynamicMem->getByte(MAX_CYCLE, nextAddr);
                DWORD key = lastByte + (0x100 * nextValue);
                pairsCache->append(key, cycle, addr);
            }
            else if (staticMem->isByteKnown(nextAddr))
            {
                BYTE nextValue = staticMem->getByte(nextAddr);
                DWORD key = lastByte + (0x100 * nextValue);
                pairsCache->append(key, cycle, addr);
            }
        }

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
