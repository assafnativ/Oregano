
#pragma once

#include <Windows.h>

#include "PagedDataContainer.hpp"
#include "PagedLinkedList.hpp"
#include "Address.hpp"
#include "StatisticsInfo.hpp"

// Redesign: I'll use a B-Tree like object of three layers.
static const DWORD PAIRS_CACHE_SIZE(0x10000);
static const DWORD PAIRS_CACHE_SIZE_MASK(0xffff);
class PairsCacheRootPage
{
public:
    DWORD size;
    PageIndex Buckets;
};

typedef PagedLinkedList<Address> PairsBucket;
typedef PagedLinkedListIter<Address> PairsBucketIter;

class PairsCache
{
	public:
		PairsCache(PageIndex rootPage, PagedDataContainer * dc);
		~PairsCache();
		void                append(DWORD pair, Address address) {cache[pair]->append(address);};
        void                append(DWORD pair, Cycle cycle, ADDRESS addr) {Address tempAddress(cycle, addr); append(pair, tempAddress);};
		Cycle               bsearchCycle(DWORD pair, Cycle cycle);
        DWORD               bsearchIndex(DWORD pair, Cycle cycle);
		const Address *	    get(DWORD pair, DWORD index) {return cache[pair]->getItem(index);};
        void                releaseItem(DWORD pair, DWORD index) {cache[pair]->releaseItem(index);};
		DWORD		        getNumItems(DWORD pair) {return cache[pair]->getNumItems();};
        PairsBucket *       getBucket(DWORD pair) {return cache[pair];};

		StatisticsInfo *	statistics();

	protected:
        PageIndex rootPageIndex;
        PagedDataContainer * dc;
        PairsCacheRootPage * rootPage;
		PairsBucket * cache[PAIRS_CACHE_SIZE];
        PageIndex * BucketsIndexes;

        void CreateRootPage();

		friend class PairCacheIter;
};

class PairCacheIter
{
	public:
		PairCacheIter(PairsCache * cache, DWORD pair, Cycle startCycle, Cycle endCycle);
        ~PairCacheIter();
        void next();
        Address const * current() {return currentItem;};
        void restartSearch();

	protected:
        void PairCacheIter::findNext();
        void releaseIter();

		PairsCache * cache;
        PairsBucketIter * bucketIter;
        DWORD pair;
        Cycle bottomCycle;
        Cycle topCycle;
        DWORD startIndex;
        Address const * currentItem;
};