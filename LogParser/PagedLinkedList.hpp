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
        LinkedListPageFormat<T> * lastPage = obtainLastPage();
        DWORD newPageIndex = 0;
        LinkedListPageFormat<T> * newPage = (LinkedListPageFormat<T> *)dc->newPage(&newPageIndex);
        DEBUG_PAGE_TAG(newPageIndex, _tag + 8);
        dc->releasePage(newPageIndex);
        lastPage->nextPage = newPageIndex;
        dc->releasePage(lastPageIndex);
        lastPageIndex = newPageIndex;
        maxItems += PAGE_ITEMS_CAPACITY;
    }

    PagedDataContainer * dc;
    DWORD numItems;
    DWORD maxItems;
#ifdef _DEBUG
    DWORD _tag;
#endif
    DWORD firstPageIndex;
    DWORD lastPageIndex;

    template<class T> friend class PagedLinkedListIter;
public:
    PagedLinkedList(DWORD anchorIndex, PagedDataContainer * dc, DWORD tag)
        :
            dc(dc),
            firstPageIndex(anchorIndex)
    {
        assert(INVALID_PAGE_INDEX != firstPageIndex);
        numItems = 0;
        LinkedListPageFormat<T> * pageIter = (LinkedListPageFormat<T> *)dc->obtainPage(firstPageIndex);
        DEBUG_ONLY(_tag = tag);
        DEBUG_PAGE_TAG(firstPageIndex, _tag);
        DWORD pageIndexIter = firstPageIndex;
        while (0 != pageIter->nextPage) {
            numItems += PAGE_ITEMS_CAPACITY;
            DWORD nextPage = pageIter->nextPage;
            dc->releasePage(pageIndexIter);
            pageIndexIter   = nextPage;
            pageIter        = (LinkedListPageFormat<T> *)dc->obtainPage(pageIndexIter);
            DEBUG_PAGE_TAG(pageIndexIter, _tag + 1);
        }
        lastPageIndex   = pageIndexIter;
        maxItems  = numItems + PAGE_ITEMS_CAPACITY;
        numItems += pageIter->numItems;
        dc->releasePage(pageIndexIter);
    }

    ~PagedLinkedList(void)
    {
        endOfData();
    }

    LinkedListPageFormat<T> * obtainLastPage()
    {
        LinkedListPageFormat<T> * result = (LinkedListPageFormat<T> *)dc->obtainPage(lastPageIndex);
        DEBUG_PAGE_TAG(lastPageIndex, _tag + 9);
        return result;
    }

    void append(T item) 
    {
        ++numItems;
        if (maxItems < numItems) {
            addPage();
        }

        LinkedListPageFormat<T> * lastPage = obtainLastPage();
        WORD itemIndex = lastPage->numItems;
		T * targetCell = lastPage->data + itemIndex;
		assert(0 == memcmp(ZERO_BUFFER_FOR_COMPARE, targetCell, sizeof(T)));
        *targetCell = item;
        lastPage->numItems++;
        dc->releasePage(lastPageIndex);
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
        LinkedListPageFormat<T> * page = (LinkedListPageFormat<T> *)dc->obtainPage(pageIndex);
        DEBUG_PAGE_TAG(pageIndex, _tag);
        DWORD inPageIndex = getInPageItemIndex(index);
        T * result = &page->data[inPageIndex];
        return result;
    }

    void releaseItem(DWORD index)
    {
        DWORD pageIndex = getPageIndexForItemIndex(index);
        dc->releasePage(pageIndex);
    }

    DWORD getPageIndexForItemIndex(DWORD itemIndex)
    {
        DWORD pageNumber = itemIndex / PAGE_ITEMS_CAPACITY;
        DWORD pageIndexIter = firstPageIndex;
        LinkedListPageFormat<T> * pageIter = (LinkedListPageFormat<T> *)dc->obtainPage(pageIndexIter);
        DEBUG_PAGE_TAG(pageIndexIter, _tag + 1);
        for (DWORD i = 0; i < pageNumber; ++i) {
            DWORD nextPageIndex = pageIter->nextPage;
            dc->releasePage(pageIndexIter);
            pageIter = (LinkedListPageFormat<T> *)dc->obtainPage(nextPageIndex);
            DEBUG_PAGE_TAG(nextPageIndex, _tag + 2);
        }
        dc->releasePage(pageIndexIter);
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
    PagedLinkedListIter( PagedLinkedList<T> * linkedList, DWORD tag )
        : 
        parent(linkedList),
        dc(parent->dc),
        numItems(parent->getNumItems())
    {
        DEBUG_ONLY(_tag = tag);
        if (0 < numItems) {
            pageIndex = parent->firstPageIndex;
            page = (LinkedListPageFormat<T> *)dc->obtainPage(pageIndex);
            DEBUG_PAGE_TAG(pageIndex, _tag);
            itemIndex = 0;
            inPageIndex = 0;
        } else {
            itemIndex = parent->getNumItems() + 1;
            page = NULL;
            pageIndex = INVALID_PAGE_INDEX;
            inPageIndex = 0;
        }
    }
    PagedLinkedListIter( PagedLinkedList<T> * linkedList, DWORD startIndex, DWORD tag )
        : 
        parent(linkedList),
        dc(parent->dc),
        numItems(parent->getNumItems())
    {
        DEBUG_ONLY(_tag = tag);
        if (startIndex < numItems) {
            itemIndex   = startIndex;
            pageIndex   = parent->getPageIndexForItemIndex(itemIndex);
            inPageIndex = parent->getInPageItemIndex(itemIndex);
            page = (LinkedListPageFormat<T> *)dc->obtainPage(pageIndex);
            DEBUG_PAGE_TAG(pageIndex, _tag + 1);
        }
        else {
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
                    page = (LinkedListPageFormat<T> *)dc->obtainPage(nextPageIndex);
                    DEBUG_PAGE_TAG(nextPageIndex, _tag + 2);
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
            dc->releasePage(pageIndex);
            page = NULL;
            pageIndex = INVALID_PAGE_INDEX;
        }
    }
    T data;
    PagedLinkedList<T> * parent;
    PagedDataContainer * dc;
    DWORD numItems;
    DWORD itemIndex;
    DWORD inPageIndex;
    PageIndex pageIndex;
    LinkedListPageFormat<T> * page;
    T item;
    DEBUG_ONLY(DWORD _tag);
};

