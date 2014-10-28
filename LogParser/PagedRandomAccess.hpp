
#pragma once

#include <windows.h>
#include "PagedDataContainer.hpp"
#include "StatisticsInfo.hpp"

template <class T>
class PagedRandomAccess
{
public:
    static const DWORD PAGE_ITEMS_CAPACITY      = PAGE_SIZE / sizeof(T);
    static const DWORD PAGE_ROOT_ITEMS_CAPACITY = PAGE_ITEMS_CAPACITY * (PAGE_INDEXES_CAPACITY - 1);
    PagedRandomAccess(PageIndex rootIndex, PagedDataContainer * dc, DWORD tag)
        : 
            dataContainer(dc),
            rootPageIndex(rootIndex),
            rootPage(NULL),
            lastPage(NULL),
            lastPageIndex(INVALID_PAGE_INDEX),
            numItems(NULL)
    {
        DEBUG_ONLY(_tag = tag);
        for (int i = 0; i < PAGE_INDEXES_CAPACITY; ++i) {
            level2Pages[i] = NULL;
        }

        rootPage = (PageIndex *)dataContainer->obtainPage(rootPageIndex);
        DEBUG_ONLY(dataContainer->setPageTag(rootPageIndex, tag));
        numItems = &rootPage[PAGE_INDEXES_CAPACITY - 1];
        // Load the level2 pages
        if (0 != *numItems)
        {
            DWORD rootIndexs = *numItems / PAGE_ROOT_ITEMS_CAPACITY;
            for (DWORD i = 0; i <= rootIndexs; ++i)
            {
                level2Pages[i] = (DWORD *)dataContainer->obtainPage(rootPage[i]);
                DEBUG_ONLY(dataContainer->setPageTag(rootPage[i], tag + 1));
            }
        }
    }

    ~PagedRandomAccess()
    {
        endOfData();

        // Release level 2
        // Only last page in Level 2 is retained
        releaseLastPage();

        // Release level 1
        PageIndex * pageIter = (DWORD *)level2Pages;
        for (PageIndex pageIndex = *pageIter; 0 != pageIndex; ++pageIter) {
            dataContainer->releasePage(pageIndex);
        }

        dataContainer->releasePage(rootPageIndex);
    }

    // Makes a copy of the item
    T getItem(DWORD itemIndex)
    {
        PageIndex pageIndex = getPageIndex(itemIndex);
        T * page = (T *)dataContainer->obtainPage(pageIndex);
        DEBUG_ONLY(dataContainer->setPageTag(pageIndex, _tag + 1));

        DWORD pageOffset = itemIndex % PAGE_ITEMS_CAPACITY;
        T result = page[pageOffset];

        dataContainer->releasePage(pageIndex);
        return result;
    }

    void releaseLastPage()
    {
        if (NULL != lastPage)
        {
            dataContainer->releasePage(lastPageIndex);
            lastPageIndex = INVALID_PAGE_INDEX;
            lastPage = NULL;
        }
    }

    T * newLastPage(PageIndex * pageIndex)
    {
        releaseLastPage();
        lastPage = (T *)dataContainer->newPage(&lastPageIndex);
        *pageIndex = lastPageIndex;
        return lastPage;
    }

    T * updateLastPage(PageIndex pageIndex)
    {
        if (lastPageIndex == pageIndex)
        {
            return lastPage;
        }
        releaseLastPage();
        lastPage = (T *)dataContainer->obtainPage(pageIndex);
        DEBUG_ONLY(dataContainer->setPageTag(pageIndex, _tag + 2));
        lastPageIndex = pageIndex;
        return lastPage;
    }

    void append(T item)
    {
        DWORD itemIndex = *numItems;
        DWORD itemRootIndex = itemIndex / PAGE_ROOT_ITEMS_CAPACITY;
        DWORD * level2Page  = level2Pages[itemRootIndex];
        if (NULL == level2Page) {
            // Allocate new level 1 page
            DWORD level2PageIndex = 0;
            level2Page = (DWORD *)dataContainer->newPage(&level2PageIndex);
            level2Pages[itemRootIndex] = level2Page;
            rootPage[itemRootIndex] = level2PageIndex;
        }
        DWORD level2Index = (itemIndex / PAGE_ITEMS_CAPACITY) % PAGE_INDEXES_CAPACITY;
        DWORD pageIndex = level2Page[level2Index];
        T * page = NULL;
        if (0 == pageIndex) {
            // Allocate new level 2 page
            page = newLastPage(&pageIndex);
            level2Page[level2Index] = pageIndex;
        } else {
            page = updateLastPage(pageIndex);
        }

        DWORD pageOffset = *numItems % PAGE_ITEMS_CAPACITY;
		T * targetCell = page + pageOffset;
		assert(0 == memcmp(ZERO_BUFFER_FOR_COMPARE, targetCell, sizeof(T)));
        *targetCell = item;
        ++(*numItems);
    }

    void endOfData()
    {
        releaseLastPage();
    }

    DWORD getNumItems() 
    {
        return *numItems;
    }

	StatisticsInfo * statistics()
	{
		StatisticsInfo * result = new StatisticsInfo;
		// One for the root page 
		result->totalPages = 1;
		result->pagesInUse = 1;

		result->totalPages += *numItems / PAGE_ITEMS_CAPACITY;
		result->totalPages += *numItems / PAGE_ROOT_ITEMS_CAPACITY;

		return result;
	}

protected:
    PagedDataContainer * dataContainer;
    PageIndex    rootPageIndex;
    PageIndex *  rootPage;
    PageIndex *  level2Pages[PAGE_INDEXES_CAPACITY];
    T *          lastPage;
    PageIndex    lastPageIndex;
    DWORD *      numItems;
    DEBUG_ONLY(DWORD _tag);

    DWORD getPageIndex(PageIndex itemIndex)
    {
        PageIndex   itemRootIndex   = itemIndex / PAGE_ROOT_ITEMS_CAPACITY;
        PageIndex * level2Page      = level2Pages[itemRootIndex];
        PageIndex   level2Index     = (itemIndex / PAGE_ITEMS_CAPACITY) % PAGE_ITEMS_CAPACITY;
        return (level2Page[level2Index]);
    }
};

