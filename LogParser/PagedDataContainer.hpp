
#pragma once

#include <windows.h>
#include <assert.h>
#include <intrin.h>
#include "PageBase.hpp"
#include "PageCache.hpp"
#include "PageLarge.hpp"
#include "GlobalDefines.hpp"

static const BYTE NULL_PAGE_DATA[PAGE_SIZE]     = {0};
static const DWORD BUCKETS_IN_CACHE             = 0x8000;
// TODO calculate these number dynamically
static const DWORD GARBAGE_COLLECT_BOTTOM_THRESHOLD = 0x60000;
static const DWORD GARBAGE_COLLECT_TARGET_THRESHOLD = 0x80000;
static const DWORD GARBAGE_COLLECT_TOP_THRESHOLD    = 0xa0000;
static const DWORD SMALL_ACCESS_COUNT				= 2;
static const PageIndex INVALID_PAGE_INDEX           = 0xffffffff;
static const DWORD PAGE_INDEXES_CAPACITY            = PAGE_SIZE / sizeof(PageIndex);

typedef DWORD BucketIndex;

class PagedDataContainer
{
protected:
    struct PageBucket {
        PageBase * first;
        PageBase * last;
        DWORD numItems;
    };
    PageBucket cache[BUCKETS_IN_CACHE];
    volatile DWORD numItems;
    DWORD totalPagesIn;
    QWORD stepper;
    HANDLE file;
    BOOL isReadOnly;

	void moveToTopOfTheList(PageBucket * bucket, PageBase * page);
    PageBase * findPage( PageIndex index );
    PageBase * findPageNoLock( PageIndex index );
    void bucketInsert( PageBase * page );
    void seekToPage( PageIndex index );
    PageBase * pageIn( PageIndex index );
    PageLarge * pageInConsecutiveData( PageIndex index, DWORD length );
    void pageOut( PageIndex index );
    void pageOut( PageBase * page );
    void pageOutNoLock( PageBase * page );
    void pageRemoveFromBucket( PageBase * page );
    void writePageNoLock( PageBase * page );
    BucketIndex  getBucketIndex( PageBase * page ) { return page->index % BUCKETS_IN_CACHE; };
    BucketIndex  getBucketIndex( PageIndex index ) { return index % BUCKETS_IN_CACHE; };
    PageBucket * getBucket( PageBase * page )      { return &cache[getBucketIndex(page)]; };
    PageBucket * getBucket( PageIndex index )      { return &cache[getBucketIndex(index)]; };
    void inline refInc( PageBase * page ) {
		++stepper;
        assert(page->refCount >= 0);
        InterlockedIncrement(&page->refCount);
        ++page->accessCount;
		page->lastAccess = stepper;
    }
    void inline refDec( PageBase * page ) {
		++stepper;
        assert(page->refCount > 0);
        InterlockedDecrement(&page->refCount);
    }

    // Cache synchronization objects
    CRITICAL_SECTION cacheLock;
    // Running flag for the threads
    BOOL cacheIsUp;

    DWORD nextFreeIndex();
    void nextFreeIndexAndOffset(PageIndex * pageIndex, LARGE_INTEGER * pageOffset);

    // Clean thread
    HANDLE cacheGarbageCollectorThread;
    DWORD cacheGarbageCollectorThreadId;
    friend DWORD WINAPI cacheGarbageCollector( PagedDataContainer * dataContainer );

public:
    PagedDataContainer( const char * fileName );
    ~PagedDataContainer();
    void   setReadOnly() {isReadOnly = TRUE;};
    BYTE * obtainPage( PageIndex index );
    BYTE * obtainConsecutiveData( PageIndex startPage, DWORD length );
    void setPageTag( PageIndex index, DWORD tag );
    void releasePage( PageIndex index );
    BYTE * newPage( OUT PageIndex * index );
    BYTE * newConsecutiveData( OUT PageIndex * index, DWORD length );
    void writePage( PageIndex index );
    void endOfData();
};