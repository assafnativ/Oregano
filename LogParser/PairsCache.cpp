
#include "stdafx.h"

#include "PairsCache.hpp"

PairsCache::PairsCache(PageIndex rootPageIndex, PagedDataContainer * dc, DWORD tag)
    : rootPageIndex(rootPageIndex), 
      dc(dc)
{
    DEBUG_ONLY(_tag = tag);
    CreateRootPage();
}

PairsCache::~PairsCache()
{
    dc->releasePage(rootPage->Buckets);
    dc->releasePage(rootPageIndex);
}

void PairsCache::CreateRootPage()
{
    rootPage = (PairsCacheRootPage *)dc->obtainPage(rootPageIndex);
    DEBUG_PAGE_TAG(rootPageIndex, 'PCRT');
    if (0 == rootPage->size) {
        // New log
        rootPage->size = PAIRS_CACHE_SIZE;
        BucketsIndexes = (PageIndex *)dc->newConsecutiveData(&rootPage->Buckets, sizeof(PageIndex) * PAIRS_CACHE_SIZE);
        DEBUG_PAGE_TAG(*BucketsIndexes, 'PCBU');
        for (DWORD i = 0; PAIRS_CACHE_SIZE > i; ++i) {
            dc->newPage(&BucketsIndexes[i]);
            DEBUG_PAGE_TAG(BucketsIndexes[i], 'APCR');
            cache[i] = new PairsBucket(BucketsIndexes[i], dc, 'PRS0');
            dc->releasePage(BucketsIndexes[i]);
        }
    } else {
        // Data is already saved to disk, just load it
        assert(rootPage->size == PAIRS_CACHE_SIZE);
        BucketsIndexes = (PageIndex *)dc->obtainConsecutiveData(rootPage->Buckets, sizeof(PageIndex) * PAIRS_CACHE_SIZE);
        DEBUG_PAGE_TAG(*BucketsIndexes, 'PCBU');
        for (DWORD i = 0; PAIRS_CACHE_SIZE > i; ++i) {
            cache[i] = new PairsBucket(BucketsIndexes[i], dc, 'PBU0');
        }
    }
}

Cycle PairsCache::bsearchCycle( DWORD pair, Cycle cycle )
{
    DWORD itemIndex = bsearchIndex(pair, cycle);
    return cache[pair]->getItem(itemIndex)->cycle;
}

DWORD PairsCache::bsearchIndex( DWORD pair, Cycle cycle )
{
    PairsBucket * bucket = cache[pair];
    DWORD lo = 0;
    DWORD hi = bucket->getNumItems();
    DWORD mid;
    DWORD midCycle;

    while (lo < hi) {
        mid = (lo + hi) / 2;
        midCycle = bucket->getItem(mid)->cycle;
        if (midCycle < cycle) {
            lo = mid + 1;
        } else if (midCycle > cycle) {
            hi = mid;
        } else {
            return mid + 1;
        }
    }
    return lo;
}

StatisticsInfo * PairsCache::statistics()
{
	StatisticsInfo * result = new StatisticsInfo;
	// One for the root page
	result->totalPages = 1;
	result->pagesInUse = 1;

	for (DWORD i = 0; PAIRS_CACHE_SIZE > i; ++i) {
		GET_AND_ADD_STATS(result, cache[i]);
	}

	return result;
}
PairCacheIter::PairCacheIter(PairsCache * cache, DWORD pair, Cycle startCycle, Cycle endCycle)
						: 
                        cache(cache),
                        pair(pair),
                        bottomCycle(startCycle),
                        topCycle(endCycle)
{
    startIndex = cache->bsearchIndex(pair, startCycle);
    restartSearch();
}

void PairCacheIter::releaseIter()
{
    if (NULL != bucketIter) {
        delete bucketIter;
        bucketIter = NULL;
    }
    currentItem = NULL;
}

PairCacheIter::~PairCacheIter()
{
    releaseIter();
}

void PairCacheIter::restartSearch()
{
    currentItem = NULL;
    if (NULL != bucketIter) {
        delete bucketIter;
        bucketIter = NULL;
    }
    bucketIter = new PairsBucketIter(cache->cache[pair], startIndex);
    findNext();
}


void PairCacheIter::next()
{
    if (NULL != bucketIter)
    {
        bucketIter->next();
        findNext();
    }
}

void PairCacheIter::findNext()
{
    currentItem = bucketIter->current();
    if ((NULL == currentItem) || (topCycle > currentItem->cycle)) {
        releaseIter();
        currentItem = NULL;
    }
}
