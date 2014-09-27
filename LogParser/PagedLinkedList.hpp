#pragma once

#include <assert.h>
#include "GlobalDefines.hpp"
#include "PagedDataContainer.hpp"
#include "StatisticsInfo.hpp"

#pragma pack(1)
template <class T>
class LinkedListPageFormat {
public:
    static const DWORD PAGE_ITEMS_CAPACITY = (PAGE_SIZE - sizeof(DWORD) - sizeof(WORD)) / sizeof(T);
    DWORD nextPage;
    T data[PAGE_ITEMS_CAPACITY];
    WORD  numItems;
};
#pragma pack()

template <class T>
class PagedLinkedList
{
protected:
    static const DWORD PAGE_ITEMS_CAPACITY = (PAGE_SIZE - sizeof(DWORD) - sizeof(WORD)) / sizeof(T);
    void addPage()
    {
        DWORD newPageIndex = 0;
        LinkedListPageFormat<T> * newPage = (LinkedListPageFormat<T> *)dataContainer->newPage(&newPageIndex);
        lastPage->nextPage = newPageIndex;
        dataContainer->releasePage(lastPageIndex);
        lastPageIndex = newPageIndex;
        lastPage = newPage;
        maxItems += PAGE_ITEMS_CAPACITY;
    }

    PagedDataContainer * dataContainer;
    DWORD numItems;
    DWORD maxItems;

    LinkedListPageFormat<T> * firstPage;
    LinkedListPageFormat<T> * lastPage;
    DWORD firstPageIndex;
    DWORD lastPageIndex;

    template<class T> friend class PagedLinkedListIter;
public:
    PagedLinkedList(DWORD anchorIndex, PagedDataContainer * dc)
        :
            dataContainer(dc),
            firstPageIndex(anchorIndex)
    {
        assert(INVALID_PAGE_INDEX != firstPageIndex);
        numItems = 0;
        firstPage = (LinkedListPageFormat<T> *)dataContainer->obtainPage(firstPageIndex);
        LinkedListPageFormat<T> * pageIter = (LinkedListPageFormat<T> *)dataContainer->obtainPage(firstPageIndex);
        assert(NULL != pageIter);
        DWORD pageIndexIter = firstPageIndex;
        while (0 != pageIter->nextPage) {
            numItems += PAGE_ITEMS_CAPACITY;
            DWORD nextPage = pageIter->nextPage;
            dataContainer->releasePage(pageIndexIter);
            pageIndexIter   = nextPage;
            pageIter        = (LinkedListPageFormat<T> *)dataContainer->obtainPage(pageIndexIter);
        }
        lastPageIndex   = pageIndexIter;
        lastPage        = pageIter;
        maxItems  = numItems + PAGE_ITEMS_CAPACITY;
        numItems += lastPage->numItems;
    }

    ~PagedLinkedList(void)
    {
        endOfData();
        dataContainer->releasePage(firstPageIndex);
        dataContainer->releasePage(lastPageIndex);
    }

    void append(T item) 
    {
        ++numItems;
        if (maxItems < numItems) {
            addPage();
        }

        WORD itemIndex = lastPage->numItems;
		T * targetCell = lastPage->data + itemIndex;
		assert(0 == memcmp(ZERO_BUFFER_FOR_COMPARE, targetCell, sizeof(T)));
        *targetCell = item;
        lastPage->numItems++;
    }

    void endOfData()
    {
        // Nothing to do for now.
    }

    T * getItem(DWORD index)
    {
        if (index > numItems) {
            return NULL;
        }
        DWORD pageNumber = index / PAGE_ITEMS_CAPACITY;
        DWORD pageIndex = getPageIndexForItemIndex(index);
        LinkedListPageFormat<T> * page = (LinkedListPageFormat<T> *)dataContainer->obtainPage(pageIndex);
        DWORD inPageIndex = getInPageItemIndex(index);
        T * result = &page->data[inPageIndex];
        return result;
    }

    void releaseItem(DWORD index)
    {
        DWORD pageIndex = getPageIndexForItemIndex(index);
        dataContainer->releasePage(pageIndex);
    }

    DWORD getPageIndexForItemIndex(DWORD itemIndex)
    {
        DWORD pageNumber = itemIndex / PAGE_ITEMS_CAPACITY;
        DWORD pageIndexIter = firstPageIndex;
        LinkedListPageFormat<T> * pageIter = (LinkedListPageFormat<T> *)dataContainer->obtainPage(pageIndexIter);
        for (DWORD i = 0; i < pageNumber; ++i) {
            DWORD nextPageIndex = pageIter->nextPage;
            dataContainer->releasePage(pageIndexIter);
            pageIter = (LinkedListPageFormat<T> *)dataContainer->obtainPage(nextPageIndex);
        }
        dataContainer->releasePage(pageIndexIter);
        return pageIndexIter;
    };

    DWORD getInPageItemIndex(DWORD itemIndex)
    {
        return itemIndex % PAGE_ITEMS_CAPACITY;
    }

    DWORD getNumItems() {return numItems;};
    DWORD getItemsPerPage() {return PAGE_ITEMS_CAPACITY;};

	StatisticsInfo * statistics()
	{
		StatisticsInfo * result = new StatisticsInfo;

		if (0 == numItems)
		{
			result->totalPages = 1;
		} else {
			result->totalPages = (numItems / PAGE_ITEMS_CAPACITY) + 2;
		}
		result->pagesInUse = 1;

		return result;
	}
};

template <class T>
class PagedLinkedListIter {
public:
    PagedLinkedListIter( PagedLinkedList<T> * linkedList )
        : 
        parent(linkedList),
        dataContainer(parent->dataContainer),
        numItems(parent->getNumItems())
    {
        if (0 < numItems) {
            pageIndex = parent->firstPageIndex;
            page = (LinkedListPageFormat<T> *)dataContainer->obtainPage(pageIndex);
            itemIndex = 0;
            inPageIndex = 0;
        } else {
            itemIndex = parent->getNumItems() + 1;
            page = NULL;
            pageIndex = INVALID_PAGE_INDEX;
            inPageIndex = 0;
        }
    }
    PagedLinkedListIter( PagedLinkedList<T> * linkedList, DWORD startIndex )
        : 
        parent(linkedList),
        dataContainer(parent->dataContainer),
        numItems(parent->getNumItems())
    {
        if (startIndex < numItems) {
            itemIndex   = startIndex;
            pageIndex   = parent->getPageIndexForItemIndex(itemIndex);
            inPageIndex = parent->getInPageItemIndex(itemIndex);
            page = (LinkedListPageFormat<T> *)dataContainer->obtainPage(pageIndex);
        } else {
            page = NULL;
            itemIndex = numItems + 1;
        }
    }
    ~PagedLinkedListIter()
    {
        releaseCurrentPage();
    }
    void next()
    {
        if (itemIndex < numItems) {
            ++itemIndex;
            ++inPageIndex;
            if (inPageIndex > page->numItems) {
                inPageIndex = 0;
                PageIndex nextPageIndex = page->nextPage;
                releaseCurrentPage();
                if (INVALID_PAGE_INDEX != nextPageIndex) {
                    page = (LinkedListPageFormat<T> *)dataContainer->obtainPage(nextPageIndex);
                }
                pageIndex = nextPageIndex;
            }
        } else {
            releaseCurrentPage();
        }
    }
    T const * current()
    {
        if (itemIndex < numItems) {
            return &(page->data[inPageIndex]);
        }
        return NULL;
    }
protected:
    void releaseCurrentPage()
    {
        if ((INVALID_PAGE_INDEX != pageIndex) && (NULL != page)) {
            dataContainer->releasePage(pageIndex);
            page = NULL;
            pageIndex = INVALID_PAGE_INDEX;
        }
    }
    T data;
    PagedLinkedList<T> * parent;
    PagedDataContainer * dataContainer;
    DWORD numItems;
    DWORD itemIndex;
    DWORD inPageIndex;
    PageIndex pageIndex;
    LinkedListPageFormat<T> * page;
    T item;
};

