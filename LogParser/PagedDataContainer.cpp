
#include <assert.h> 

#include "PagedDataContainer.hpp"

PagedDataContainer::PagedDataContainer(const char * fileName)
    : 
    isReadOnly(FALSE),
    numItems(0),
	stepper(0)
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
        cache[i].numItems = 0;
    }

    // Make the synchronization objects
    InitializeCriticalSection(&cacheLock);

    // Running flag for the threads
    cacheIsUp = TRUE;
    cacheGarbageCollectorThread = CreateThread(
        NULL,
        0,
        (LPTHREAD_START_ROUTINE)cacheGarbageCollector,
        this,
        0,
        &cacheGarbageCollectorThreadId);

}

PagedDataContainer::~PagedDataContainer()
{
    cacheIsUp = FALSE;
    Sleep(0);

    EnterCriticalSection(&cacheLock);

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

    LeaveCriticalSection(&cacheLock);
}

void PagedDataContainer::moveToTopOfTheList(PageBucket * bucket, PageBase * page)
{
	if (page != bucket->first)
	{
		// First remove the page from where it is currently found
		PageBase * oldNext = page->next;
		PageBase * oldPrev = page->prev;
        // It is not the first so it must have a prev
		oldPrev->next = oldNext;
        // But it doesn't have to have next
        if (NULL != oldNext) {
		    oldNext->prev = oldPrev;
        }
		// Put it on top of the list
		PageBase * oldFirst = bucket->first;
		bucket->first = page;
		page->next = oldFirst;
		page->prev = oldFirst->prev;
		oldFirst->prev = page;
	}	
}

PageBase * PagedDataContainer::findPageNoLock(PageIndex index)
{
    DWORD tableIndex = index % BUCKETS_IN_CACHE;

    // The result of the function
    PageBase * result = NULL;

    PageBase * pageIter = cache[tableIndex].first;
    for (; NULL != pageIter; pageIter = pageIter->next)
    {
        PageIndex pageIndex;
        pageIndex = pageIter->index;
        if (index == pageIndex) {
            // Page found
            result = pageIter;
			// Put it in the head of the list
			//moveToTopOfTheList(&cache[tableIndex], pageIter);
            break;
        }
    }

    return result;
}

PageBase * PagedDataContainer::findPage(PageIndex index)
{
    EnterCriticalSection(&cacheLock);
    PageBase * result = findPageNoLock( index );
    LeaveCriticalSection(&cacheLock);

    return result;
}

void PagedDataContainer::bucketInsert( PageBase * page )
{
    PageIndex index = page->index;
    DWORD tableIndex = index % BUCKETS_IN_CACHE;

    PageBucket * bucket = &cache[tableIndex];
    PageBase * firstPage = bucket->first;
    PageBase * lastPage  = bucket->last;
    page->prev = NULL;
    bucket->first = page;
    // Make the new page the first page
    // If no pages in the bucket, update the last pointer
    if (NULL == firstPage) {
        page->next = NULL;
        bucket->last = page;
    } else {
        // Bucket is not empty
        page->next = firstPage;
        firstPage->prev = page;
    }

    // Update statistics
    ++bucket->numItems;
    ++numItems;
}

void PagedDataContainer::seekToPage( PageIndex index )
{
    // Get the page offset
    LARGE_INTEGER pageOffset;
    pageOffset.QuadPart = index * PAGE_SIZE;

    // Seek
    BOOL seekResult = SetFilePointerEx(file, pageOffset, NULL, FILE_BEGIN);
    assert(FALSE != seekResult);
}

PageBase * PagedDataContainer::pageIn(PageIndex index)
{
    if (numItems > GARBAGE_COLLECT_CRITICAL_THRESHOLD)
    {
        // Give the garbage collector a chance
        Sleep(0);
    }

    // 1. Seek to right place
    // 2. Make a new page object
    // 3. Read page
    // 4. Add to a bucket
    // 5. Update statistics
    
    seekToPage(index);

    // The result of the function
    assert(INVALID_HANDLE_VALUE != file);
    PageBase * newPage = new PageCache(index);
    assert(NULL != newPage);

    // Read
    DWORD bytesRead = 0;
    BYTE * data = newPage->getData();
    assert(NULL != data);
    BOOL readResult = ReadFile(file, data, PAGE_SIZE, &bytesRead, NULL);
    assert((FALSE != readResult) && (PAGE_SIZE == bytesRead));

    // Insert to the bucket
    bucketInsert(newPage);

    return newPage;
}

PageLarge * PagedDataContainer::pageInConsecutiveData( PageIndex index, DWORD length )
{
    seekToPage(index);

    // The result of the function
    PageLarge * newPage = new PageLarge(index, length);
    assert(NULL != newPage);

    // Read
    DWORD bytesRead = 0;
    BYTE * data = newPage->getData();
    assert(NULL != data);
    BOOL readResult = ReadFile(file, data, length, &bytesRead, NULL);
    assert((FALSE != readResult) && (bytesRead == length));

    // Insert to the bucket
    bucketInsert(newPage);

    return newPage;
}


void PagedDataContainer::pageOut( PageIndex index )
{
    PageBase * page = findPage(index); 
    assert(NULL != page);
    pageOut(page);
}

void PagedDataContainer::pageOut( PageBase * page )
{
    EnterCriticalSection(&cacheLock);
    pageOutNoLock(page);
    LeaveCriticalSection(&cacheLock);
}

void PagedDataContainer::pageOutNoLock( PageBase * page )
{
    writePageNoLock(page);
    pageRemoveFromBucket( page );
    delete page;
}

void PagedDataContainer::pageRemoveFromBucket( PageBase * page )
{
    PageBucket * bucket = getBucket(page);
    PageBase * nextPage = page->next;
    if (NULL != nextPage) {
        nextPage->prev = page->prev;
    } else {
        bucket->last = page->prev;
    }
    PageBase * prevPage = page->prev;
    if (NULL != prevPage) {
        prevPage->next = page->next;
    } else {
        bucket->first = nextPage;
    }
    --bucket->numItems;
    --numItems;
}

DWORD WINAPI cacheGarbageCollector( PagedDataContainer * dataContainer )
{
    DWORD bucketsIter = 0;
    BOOL isLocked = FALSE;
	QWORD stepperCut = dataContainer->stepper / 2;
    DWORD targetTreshold = GARBAGE_COLLECT_TOP_THRESHOLD;

    if (dataContainer->numItems > GARBAGE_COLLECT_TOP_THRESHOLD)
    {
        targetTreshold = GARBAGE_COLLECT_TARGET_THRESHOLD;
    }
    while (dataContainer->cacheIsUp) {
        if (dataContainer->numItems > GARBAGE_COLLECT_BOTTOM_THRESHOLD)
        {
            if (FALSE == isLocked)
            {
                isLocked = TRUE;
                EnterCriticalSection(&dataContainer->cacheLock);
            }

            PageBase * pageToGoOut = NULL;
            DWORD endBucket = (bucketsIter + BUCKETS_IN_CACHE - 1) % BUCKETS_IN_CACHE;
            for (; 
                bucketsIter != endBucket; 
                bucketsIter = (bucketsIter + 1) % BUCKETS_IN_CACHE )
            {
                PagedDataContainer::PageBucket * bucket = &dataContainer->cache[bucketsIter];
                PageBase * pageIter = bucket->last;
                while (NULL != pageIter) 
                {
                    if (0 == pageIter->refCount) {
						// Decide on which page in this bucket to pageOut
						if (NULL == pageToGoOut) {
							pageToGoOut = pageIter;
						} else if (pageIter->accessCount < pageToGoOut->accessCount) {
							pageToGoOut = pageIter;
						}
						/*
						if (SMALL_ACCESS_COUNT >= pageToGoOut->accessCount)
						{
							break;
						}
						*/
						if (stepperCut > pageIter->accessCount)
						{
							break;
						}
                    }
                    pageIter = pageIter->prev;
                }
                // Have we found a page to page out in this bucket
                if (NULL != pageToGoOut)
                {
                    break;
                }
            }

            assert (NULL != pageToGoOut);
            // Release one page
            dataContainer->pageOutNoLock(pageToGoOut);

            // Should we release the lock on the cache
            // If the cache is too full, don't release the lock until we clean it
            if (    (dataContainer->numItems < targetTreshold) &&
                    (TRUE == isLocked) )
            {
                LeaveCriticalSection(&dataContainer->cacheLock);
                isLocked = FALSE;
                Sleep(0);
            }

            // Next iteration try another bucket
            bucketsIter = (bucketsIter + 1) % BUCKETS_IN_CACHE;
        } // GARBAGE_COLLECT_THRESHOLD
    } // cacheIsUp

    return STILL_ACTIVE;
}

// - Public functions -

BYTE * PagedDataContainer::obtainPage(PageIndex index)
{
    // 1. Search in the cache for the page.
    // 2. If it is not found, read it from disk and insert to cache
    // 3. Update cache
    // 4. Return Data

    // This function acquires the lock and not the find or pageIn functions,
    // Because if we get the page in the findPage function and than it is lost
    // before we inc the ref count we get a big shit.
    EnterCriticalSection(&cacheLock);

    PageBase * page = findPageNoLock(index);
    if (NULL == page) {
        page = pageIn(index);
        assert(NULL != page);
    }
    refInc(page);

    LeaveCriticalSection(&cacheLock);

    return page->getData();
}

BYTE * PagedDataContainer::obtainConsecutiveData( PageIndex startPage, DWORD length )
{
    EnterCriticalSection(&cacheLock);

    PageBase * page = findPageNoLock(startPage);
    if (NULL == page) {
        page = pageInConsecutiveData( startPage, length );
        assert(NULL != page);
    }
    refInc(page);

    LeaveCriticalSection(&cacheLock);

    return page->getData();
}

void PagedDataContainer::setPageTag(PageIndex index, DWORD tag)
{
#ifdef _DEBUG
    EnterCriticalSection(&cacheLock);

    PageBase * page = findPageNoLock(index);
    if (NULL != page)
    {
        page->tag = tag;
    }

    LeaveCriticalSection(&cacheLock);
#endif
}

void PagedDataContainer::releasePage(PageIndex index)
{
    // Don't need to lock cache here, because the page has ref count > 0
    // So it won't get lost on the way.
    PageBase * page = findPage(index);
    assert(page->refCount > 0);
    refDec(page);
}

// Unsafe, should be used under lock
DWORD PagedDataContainer::nextFreeIndex()
{
    LARGE_INTEGER fileSize;
    BOOL getFileSizeResult;

    assert(INVALID_HANDLE_VALUE != file);
    getFileSizeResult = GetFileSizeEx(file, &fileSize);
    assert(FALSE != getFileSizeResult);

    return (DWORD)(fileSize.QuadPart / (long long)PAGE_SIZE);
}

// Unsafe, should be used under lock
void PagedDataContainer::nextFreeIndexAndOffset(PageIndex * pageIndex, LARGE_INTEGER * pageOffset)
{
    BOOL getFileSizeResult;

    assert(INVALID_HANDLE_VALUE != file);
    getFileSizeResult = GetFileSizeEx(file, pageOffset);
    assert(FALSE != getFileSizeResult);

    *pageIndex = (PageIndex)(pageOffset->QuadPart / (long long)PAGE_SIZE);
    
}

BYTE * PagedDataContainer::newPage(DWORD * index)
{
    // 1. Find a index for the new page
    // 2. Create the page
    // 3. Return the page data

    EnterCriticalSection(&cacheLock);

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

    LeaveCriticalSection(&cacheLock);
    return result;
}

BYTE * PagedDataContainer::newConsecutiveData( OUT PageIndex * index, DWORD length )
{
    assert(0 != length);

    EnterCriticalSection(&cacheLock);

    // Find the EOF
    LARGE_INTEGER pageOffset = {0};
    nextFreeIndexAndOffset(index, &pageOffset);
    assert(INVALID_HANDLE_VALUE != file);
    assert(0 != index);
    assert(0 != pageOffset.QuadPart);
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

    LeaveCriticalSection(&cacheLock);

    return result;
}

void PagedDataContainer::writePage( PageIndex index )
{
    if (TRUE == isReadOnly) {
        return;
    }
    PageBase * page = findPage(index);
    // NULL page means attempt to write a page that is not in
    assert(NULL != page);

    EnterCriticalSection(&cacheLock);

    writePageNoLock(page);

    LeaveCriticalSection(&cacheLock);
}

void PagedDataContainer::writePageNoLock( PageBase * page )
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
    EnterCriticalSection(&cacheLock);
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
            writePageNoLock(pageIter);
        }
    }
    LeaveCriticalSection(&cacheLock);
    isReadOnly = TRUE;
}
