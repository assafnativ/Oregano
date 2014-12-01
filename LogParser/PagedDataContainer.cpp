
#include "stdafx.h"

#include "PagedDataContainer.hpp"

PagedDataContainer::PagedDataContainer(const char * fileName)
    : 
    isReadOnly(FALSE),
    totalPagesIn(0),
    bucketToClean(0)
{
    file = CreateFileA(
                fileName,
                GENERIC_ALL,
                0,
                NULL,
                OPEN_ALWAYS,
                FILE_ATTRIBUTE_NORMAL,
                0);
    assert(INVALID_HANDLE_VALUE != file);

    // Is that a new file
    LARGE_INTEGER fileSize;
    BOOL seekResult;
    seekResult = GetFileSizeEx(file, &fileSize);
    assert(FALSE != seekResult);
    if (0 == fileSize.QuadPart)
    {
        // Yes this is a new file, create the very first page
        DWORD bytesWritten = 0;
        BOOL writeResult = FALSE;
        writeResult = WriteFile(file, NULL_PAGE_DATA, PAGE_SIZE, &bytesWritten, NULL);
        assert((FALSE != writeResult) && (PAGE_SIZE == bytesWritten));
    } // if (0 == fileSize.QuadPart)

    // Init the cache
    for (DWORD i = 0; i < BUCKETS_IN_CACHE; ++i)
    {
        cache[i].first = NULL;
        cache[i].last  = NULL;
        cache[i].freeList = NULL;
        cache[i].numItems = 0;
    }
    validateCache();
}

PagedDataContainer::~PagedDataContainer()
{
    validateCache();
    // Free all
    for (DWORD bucketIter = 0; bucketIter < BUCKETS_IN_CACHE; ++bucketIter) {
        PageBucket * bucket = &cache[bucketIter];
        PageBase * pageIter = bucket->first;
        while (NULL != pageIter) {
            PageBase * nextPage = pageIter->next;
            delete pageIter;
            pageIter = nextPage;
        }
    }
}

void PagedDataContainer::removePageWithPrevFromBucket(PageBucket * bucket, PageBase * page)
{
    PageBase * oldNext = page->next;
    PageBase * oldPrev = page->prev;
    // It is not the last so it must have a prev
    oldNext->prev = oldPrev;
    // But it doesn't have to have next
    if (NULL != oldPrev) {
        oldPrev->next = oldNext;
    }
    else
    {
        // This page was the first
        bucket->first = oldNext;
    }
}

void PagedDataContainer::removePageWithNextFromBucket(PageBucket * bucket, PageBase * page)
{
    PageBase * oldNext = page->next;
    PageBase * oldPrev = page->prev;
    // It is not the first so it must have a prev
    oldPrev->next = oldNext;
    // But it doesn't have to have next
    if (NULL != oldNext) {
        oldNext->prev = oldPrev;
    }
    else
    {
        // This page was the last
        bucket->last = oldPrev;
    }
}

void PagedDataContainer::putPageInBucketAfter(PageBucket * bucket, PageBase * page, PageBase * pageBefore)
{
    if (NULL == pageBefore)
    {
        // Make it the first page in the bucket
        putPageInBucketTop(bucket, page);
    }
    else
    {
        PageBase * pageAfter = pageBefore->next;
        page->prev = pageBefore;
        if (NULL != pageAfter)
        {
            pageAfter->prev = page;
            page->next = pageAfter;
        }
        else
        {
            bucket->last = page;
            page->next = NULL;
        }
        pageBefore->next = page;
    }
}

void PagedDataContainer::putPageInBucketTop(PageBucket * bucket, PageBase * page)
{
    PageBase * oldFirst = bucket->first;
    bucket->first = page;
    page->next = oldFirst;
    page->prev = NULL;
    oldFirst->prev = page;
}

void PagedDataContainer::moveToBucketTop(PageBucket * bucket, PageBase * page)
{
    if (bucket->freeList == page)
    {
        bucket->freeList = page->next;
    }
    if (page == bucket->first)
    {
        // Nothing else to do here
        return;
    }
    // First remove the page from where it's currently found
    removePageWithNextFromBucket(bucket, page);
	// Put it on top of the list
    putPageInBucketTop(bucket, page);
}

void PagedDataContainer::moveToFreeListStart(PageBucket * bucket, PageBase * page)
{
    assert(page != bucket->freeList);
    // If we got here, the list has more than one page in it.
    // Find a place for it
    PageBase * freeStart = bucket->freeList;
    PageBase * pageBefore;
    if (NULL == freeStart)
    {
        // No free pages in this bucket
        pageBefore = bucket->last;
    }
    else
    {
        pageBefore = freeStart->prev;
    }
    // Page before can't be NULL, because either:
    //  There was some free page, the new page was just moved from the none free pages to the free pages.
    //  Or there was no free page, so pageBore was set for the last page and the list is not empty.
    assert(NULL != pageBefore);
    do {
        if (pageBefore == page)
        {
            // Just move the free list start one back and we are done
            break;
        }
        // First remove the page from where it's currently found
        removePageWithPrevFromBucket(bucket, page);
        // Put it in a new place
        putPageInBucketAfter(bucket, page, pageBefore);
    } while (FALSE);
    bucket->freeList = page;
}

PageBase * PagedDataContainer::findPage(PageIndex index)
{
    PageBucket * bucket = getBucket(index);
    return findPage(bucket, index);
}

PageBase * PagedDataContainer::findPage(PageBucket * bucket, PageIndex index)
{
    PageBase * result = NULL;

    PageBase * pageIter = bucket->first;
    for (; NULL != pageIter; pageIter = pageIter->next)
    {
        if (index == pageIter->index) {
            // Page found
            result = pageIter;
            break;
        }
    }

    return result;
}

void PagedDataContainer::bucketInsert( PageBase * page )
{
    // First free one page if we need to.
    // This done first so we won't free the new page.
    if (totalPagesIn >= GARBAGE_COLLECT_TOP_THRESHOLD)
    {
        freeOne();
    }
    
    PageBucket * bucket = getBucket(page);
    PageBase * oldFirst = bucket->first;
    bucket->first = page;
    // Make the new page the first page
    // If no pages in the bucket, update the last pointer
    if (NULL == oldFirst) {
        bucket->last = page;
    } else {
        // Bucket is not empty
        page->next = oldFirst;
        oldFirst->prev = page;
    }

    ++bucket->numItems;
    ++totalPagesIn;
}

void PagedDataContainer::seekToPage( PageIndex index )
{
    // Get the page offset
    LARGE_INTEGER pageOffset;
    pageOffset.QuadPart = ((LONGLONG)index) * PAGE_SIZE;

    // Seek
    BOOL seekResult = SetFilePointerEx(file, pageOffset, NULL, FILE_BEGIN);
}

PageBase * PagedDataContainer::pageIn(PageIndex index)
{
    // 1. Seek to right place
    // 2. Make a new page object
    // 3. Read page
    // 4. Add to a bucket
    // 5. Update statistics
    
    seekToPage(index);

    // The result of the function
    PageBase * newPage = new PageCache(index);

    // Read
    DWORD bytesRead = 0;
    BYTE * data = newPage->getData();
    BOOL readResult = ReadFile(file, data, PAGE_SIZE, &bytesRead, NULL);

    // Insert to the bucket
    bucketInsert(newPage);

    return newPage;
}

PageLarge * PagedDataContainer::pageInConsecutiveData( PageIndex index, DWORD length )
{
    seekToPage(index);

    // The result of the function
    PageLarge * newPage = new PageLarge(index, length);

    // Read
    DWORD bytesRead = 0;
    BYTE * data = newPage->getData();
    BOOL readResult = ReadFile(file, data, length, &bytesRead, NULL);

    // Insert to the bucket
    bucketInsert(newPage);

    return newPage;
}


void PagedDataContainer::pageOut( PageIndex index )
{
    PageBucket * bucket = getBucket(index);
    PageBase * page = findPage(bucket, index); 
    pageOut(bucket, page);
}

void PagedDataContainer::pageOut( PageBucket * bucket, PageBase * page )
{
    writePage(page);
    pageRemoveFromBucket(bucket, page);
    delete page;
}

void PagedDataContainer::pageRemoveFromBucket( PageBucket * bucket, PageBase * page )
{
    if (1 == bucket->numItems)
    {
        bucket->first = NULL;
        bucket->last = NULL;
        bucket->freeList = NULL;
        bucket->numItems = 0;
        return;
    }
    PageBase * nextPage = page->next;
    PageBase * prevPage = page->prev;
    if (NULL != nextPage) {
        nextPage->prev = prevPage;
    } else {
        bucket->last = prevPage;
    }
    if (NULL != prevPage) {
        prevPage->next = nextPage;
    } else {
        bucket->first = nextPage;
    }
    if (page == bucket->freeList)
    {
        bucket->freeList = nextPage;
    }
    // The bucket had more than one item, so this is a sanity check
    --bucket->numItems;
    --totalPagesIn;
}

void PagedDataContainer::freeOne()
{
    PageBase * pageToGoOut = NULL;
    PageBucket * bucket = NULL;
    for (DWORD i = 0; i < BUCKETS_IN_CACHE; ++i)
    {
        bucket = &cache[bucketToClean];
        bucketToClean++;
        bucketToClean %= BUCKETS_IN_CACHE;
        PageBase * pageIter = bucket->last;
        if ((NULL != pageIter) && (0 == pageIter->refCount))
        {
            pageToGoOut = pageIter;
            break;
        }
    }
    assert(NULL != pageToGoOut);
    // Release one page
    pageOut(bucket, pageToGoOut);
}

// - Public functions -

BYTE * PagedDataContainer::obtainPage(PageIndex index)
{
    // 1. Search in the cache for the page.
    // 2. If it is not found, read it from disk and insert to cache
    // 3. Update cache
    // 4. Return Data

    PageBucket * bucket = getBucket(index);
    PageBase * page = findPage(bucket, index);
    if (NULL == page) {
        page = pageIn(index);
    }
    else 
    {
        refInc(page);
        moveToBucketTop(bucket, page);
    }

    return page->getData();
}

BYTE * PagedDataContainer::obtainConsecutiveData( PageIndex startPage, DWORD length )
{
    PageBucket * bucket = getBucket(startPage);
    PageBase * page = findPage(bucket, startPage);
    if (NULL == page) {
        page = pageInConsecutiveData(startPage, length);
    }
    else 
    {
        refInc(page);
        moveToBucketTop(bucket, page);
    }

    return page->getData();
}

void PagedDataContainer::setPageTag(PageIndex index, DWORD tag)
{
#ifdef _DEBUG
    PageBase * page = findPage(index);
    if (NULL != page)
    {
        page->tag = tag;
    }
#endif
}

void PagedDataContainer::releasePage(PageIndex index)
{
    DWORD tableIndex = getBucketIndex(index);
    PageBucket * bucket = &cache[tableIndex];
    PageBase * page = findPage(bucket, index);
    refDec(page);
    if (0 == page->refCount)
    {
        moveToFreeListStart(bucket, page);
    }
}

DWORD PagedDataContainer::nextFreeIndex()
{
    LARGE_INTEGER fileSize;
    BOOL getFileSizeResult;

    getFileSizeResult = GetFileSizeEx(file, &fileSize);

    return (DWORD)(fileSize.QuadPart / (long long)PAGE_SIZE);
}

void PagedDataContainer::nextFreeIndexAndOffset(PageIndex * pageIndex, LARGE_INTEGER * pageOffset)
{
    BOOL getFileSizeResult;

    getFileSizeResult = GetFileSizeEx(file, pageOffset);

    *pageIndex = (PageIndex)(pageOffset->QuadPart / (long long)PAGE_SIZE);
}

BYTE * PagedDataContainer::newPage(DWORD * index)
{
    // 1. Find a index for the new page
    // 2. Create the page
    // 3. Return the page data

    LARGE_INTEGER pageOffset = {0};
    nextFreeIndexAndOffset(index, &pageOffset);
    // Create the page
    // Seek
    LARGE_INTEGER fileSize;
    BOOL seekResult;
    assert(INVALID_HANDLE_VALUE != file);
    seekResult = GetFileSizeEx(file, &fileSize);
    assert(FALSE != seekResult);
    // Do I have to add bytes to the file
    if (pageOffset.QuadPart >= fileSize.QuadPart) {
        long long bytesMissing;
        bytesMissing = pageOffset.QuadPart - fileSize.QuadPart + PAGE_SIZE;
        // Sanity check
        assert(PAGE_SIZE == bytesMissing);

        // Write missing bytes

        // Goto the end of the file
        LARGE_INTEGER zeroOffset;
        zeroOffset.QuadPart = 0;
        seekResult = SetFilePointerEx(file, zeroOffset, NULL, FILE_END);
        assert(FALSE != seekResult);

        // Extend file
        BOOL writeResult;
        long long totalBytesWritten = 0;
        while (totalBytesWritten < bytesMissing) {
            DWORD bytesWritten = 0;
            writeResult = WriteFile(file, NULL_PAGE_DATA, PAGE_SIZE, &bytesWritten, NULL);
            assert((FALSE != writeResult) && (PAGE_SIZE == bytesWritten));
            totalBytesWritten += PAGE_SIZE;
        } // while (totalBytesWritten < bytesMissing)
    } // if (pageOffset.QuadPart >= fileSize.QuadPart)

    BYTE * result = obtainPage(*index);
    return result;
}

BYTE * PagedDataContainer::newConsecutiveData( OUT PageIndex * index, DWORD length )
{
    // Find the EOF
    LARGE_INTEGER pageOffset = {0};
    nextFreeIndexAndOffset(index, &pageOffset);
    BOOL seekResult = SetFilePointerEx(file, pageOffset, NULL, FILE_BEGIN);
    assert(FALSE != seekResult);

    // How many pages do we need
    DWORD pagesNeeded = length / PAGE_SIZE;
    if (0 != (length % PAGE_SIZE)) {
        pagesNeeded++;
    }
    // Fill it with empty data, page by page
    for (PageIndex indexIter = 0; indexIter < pagesNeeded; ++indexIter) {
        DWORD bytesWritten = 0;
        BOOL writeResult = WriteFile(file, NULL_PAGE_DATA, PAGE_SIZE, &bytesWritten, NULL);
        assert((FALSE != writeResult) && (PAGE_SIZE == bytesWritten));
    }

    BYTE * result = obtainConsecutiveData(*index, length);

    return result;
}

void PagedDataContainer::writePage( PageIndex index )
{
    if (TRUE == isReadOnly) {
        return;
    }
    PageBase * page = findPage(index);
    writePage(page);
}

void PagedDataContainer::writePage( PageBase * page )
{
    if (TRUE == isReadOnly) {
        return;
    }
    PageIndex index = page->index;

    LARGE_INTEGER pageOffset;
    BOOL seekResult;
    BOOL writeResult;
    pageOffset.QuadPart = (LONGLONG)page->index * PAGE_SIZE;

    seekResult = SetFilePointerEx(file, pageOffset, NULL, FILE_BEGIN);
    assert(FALSE != seekResult);
    DWORD bytesWritten;
    writeResult = WriteFile(file, page->getData(), page->getDataLength(), &bytesWritten, NULL);
    assert((FALSE != writeResult) && (bytesWritten == page->getDataLength()));
}

void PagedDataContainer::endOfData()
{
    // Write all pages in all buckets.
    // Pages that are paged-out are already written.
    for (DWORD bucketIndex = 0; bucketIndex != BUCKETS_IN_CACHE; ++bucketIndex)
    {
        PagedDataContainer::PageBucket * bucket = &cache[bucketIndex];
        for (
            PageBase * pageIter = bucket->first;
            pageIter != NULL;
            pageIter = pageIter->next )
        {
            writePage(pageIter);
        }
    }
    isReadOnly = TRUE;
}

void PagedDataContainer::validateCache()
{
#ifdef _DEBUG
    DWORD totalPages = 0;
    for (DWORD bucketId = 0; bucketId < BUCKETS_IN_CACHE; ++bucketId)
    {
        PageBucket * bucket = &cache[bucketId];
        totalPages += validateBucket(bucket);
    }
    assert(totalPages == totalPagesIn);
#endif
}

DWORD PagedDataContainer::validateBucket(PageBucket * bucket)
{
#ifdef _DEBUG
    assert(bucket->numItems < ((GARBAGE_COLLECT_TOP_THRESHOLD / BUCKETS_IN_CACHE) * 5));
    if (bucket->numItems > 0)
    {
        assert(NULL != bucket->first);
        assert(NULL != bucket->last);
        assert(NULL == bucket->first->prev);
        assert(NULL == bucket->last->next);
        if (1 == bucket->numItems)
        {
            assert(bucket->first == bucket->last);
            assert((0 != bucket->first->refCount) || (bucket->freeList == bucket->first));
            assert((0 == bucket->first->refCount) || (bucket->freeList == NULL));
        }
        else
        {
            PageBase * lastPage = NULL;
            PageBase * pageIter = bucket->first;
            bool isZeroRefs = false;
            assert(NULL != pageIter);
            for (DWORD itemIndex = 0; itemIndex < bucket->numItems; ++itemIndex)
            {
                assert(NULL != pageIter);
                assert(pageIter->prev == lastPage);
                assert(NULL != pageIter->getData());
                assert(0 < pageIter->getDataLength());
                if ((0 == pageIter->refCount) && (false == isZeroRefs))
                {
                    isZeroRefs = true;
                    assert(pageIter == bucket->freeList);
                }
                assert((!isZeroRefs) || (0 == pageIter->refCount));
                assert((isZeroRefs) || (0 != pageIter->refCount));
                assert(pageIter->refCount < 0x10000);
                lastPage = pageIter;
                pageIter = pageIter->next;
            }
            assert(NULL == pageIter);
            assert((false != isZeroRefs) || (NULL == bucket->freeList));
        }
    }
    else
    {
        assert(NULL == bucket->first);
        assert(NULL == bucket->last);
        assert(NULL == bucket->freeList);
    }
#endif
    return bucket->numItems;
}