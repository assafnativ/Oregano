
#pragma once

#include <windows.h>
#include <assert.h>
#include <intrin.h>
#include "PageBase.hpp"
#include "PageCache.hpp"
#include "PageLarge.hpp"
#include "GlobalDefines.hpp"

static const BYTE NULL_PAGE_DATA[PAGE_SIZE]     = {0};
static const DWORD BUCKETS_IN_CACHE = 0x800;
// TODO calculate these number dynamically
#ifdef AMD64
static const DWORD GARBAGE_COLLECT_TOP_THRESHOLD = 0x80000;
#else
static const DWORD GARBAGE_COLLECT_TOP_THRESHOLD = 0x50000;
#endif
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
        PageBase * freeList;
        DWORD numItems;
    };
    PageBucket cache[BUCKETS_IN_CACHE];
    DWORD totalPagesIn;
    HANDLE file;
    BOOL isReadOnly;
    DWORD bucketToClean;


    void removePageWithPrevFromBucket(PageBucket * bucket, PageBase * page);
    void removePageWithNextFromBucket(PageBucket * bucket, PageBase * page);
    void putPageInBucketAfter(PageBucket * bucket, PageBase * page, PageBase * pageBefore);
    void putPageInBucketTop(PageBucket * bucket, PageBase * page);
    void moveToBucketTop(PageBucket * bucket, PageBase * page);
    void moveToFreeListStart(PageBucket * bucket, PageBase * page);
    PageBase * findPage(PageIndex index);
    PageBase * findPage(PageBucket * bucket, PageIndex index);
    void bucketInsert( PageBase * page );
    void seekToPage( PageIndex index );
    PageBase * pageIn( PageIndex index );
    PageLarge * pageInConsecutiveData( PageIndex index, DWORD length );
    void pageOut( PageIndex index );
    void pageOut( PageBucket * bucket, PageBase * page );
    void pageRemoveFromBucket( PageBucket * bucket, PageBase * page );
    void writePage( PageBase * page );
    BucketIndex  getBucketIndex( PageBase * page ) { return page->index % BUCKETS_IN_CACHE; }
    BucketIndex  getBucketIndex( PageIndex index ) { return index % BUCKETS_IN_CACHE; }
    PageBucket * getBucket( PageBase * page )      { return &cache[getBucketIndex(page)]; }
    PageBucket * getBucket( PageIndex index )      { return &cache[getBucketIndex(index)]; }
    void inline refInc( PageBase * page ) {
        assert(page->refCount >= 0);
        page->refCount++;
    }
    void inline refDec( PageBase * page ) {
        assert(page->refCount > 0);
        page->refCount--;
    }

    DWORD nextFreeIndex();
    void nextFreeIndexAndOffset(PageIndex * pageIndex, LARGE_INTEGER * pageOffset);
    void freeOne();
    void validateCache();
    DWORD validateBucket(PageBucket * bucket);

public:
    PagedDataContainer( const char * fileName );
    ~PagedDataContainer();
    void   setReadOnly() { isReadOnly = TRUE; }
    BYTE * obtainPage( PageIndex index );
    BYTE * obtainConsecutiveData( PageIndex startPage, DWORD length );
    void setPageTag( PageIndex index, DWORD tag );
    void releasePage( PageIndex index );
    BYTE * newPage( OUT PageIndex * index );
    BYTE * newConsecutiveData( OUT PageIndex * index, DWORD length );
    void writePage( PageIndex index );
    void endOfData();
};
