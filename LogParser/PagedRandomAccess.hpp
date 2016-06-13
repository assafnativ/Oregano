#pragma once

#include <windows.h>
#include "PagedDataContainer.hpp"
#include "StatisticsInfo.hpp"

typedef DWORD RandomAccessItemIndex;
typedef DWORD RandomAccessOffsetInRoot;
typedef DWORD RandomAccessOffsetInLevel2Page;
typedef DWORD RandomAccessLeafOffset;

template <class T>
class PagedRandomAccess
{
public:
    static const DWORD LEAF_PAGE_CAPACITY = PAGE_SIZE / sizeof(T);
    static const DWORD LEAFS_IN_LEVEL2_ITEM = (PAGE_INDEXES_CAPACITY);
    static const DWORD ROOT_PAGE_CAPACITY = LEAF_PAGE_CAPACITY * LEAFS_IN_LEVEL2_ITEM;
    static const DWORD INDEXES_IN_ROOT_PAGE = (PAGE_INDEXES_CAPACITY - 1);
    static const DWORD TOTAL_CAPACITY = INDEXES_IN_ROOT_PAGE * ROOT_PAGE_CAPACITY;
    struct RandomAccessRootPage
    {
        DWORD numItems;
        PageIndex level2[INDEXES_IN_ROOT_PAGE];
    };
    PagedRandomAccess(PageIndex rootIndex, PagedDataContainer * dc, DWORD tag) :
            dc(dc),
            rootPageIndex(rootIndex),
            rootPage(NULL)
    {
        DEBUG_ONLY(_tag = tag);
        rootPage = (RandomAccessRootPage *)dc->obtainPage(rootPageIndex);
        DEBUG_PAGE_TAG(rootPageIndex, _tag);
    }

    ~PagedRandomAccess()
    {
        endOfData();
        dc->releasePage(rootPageIndex);
    }

    // Makes a copy of the item
    T getItem(RandomAccessItemIndex itemIndex)
    {
        PageIndex leafPageIndex;
        T * leaf = (T *)obtainLeafPage(leafPageIndex, itemIndex);

        RandomAccessLeafOffset pageOffset = getLeafOffset(itemIndex);
        T result = leaf[pageOffset];

        dc->releasePage(leafPageIndex);
        return result;
    }

    void append(T item)
    {
        RandomAccessItemIndex itemIndex = rootPage->numItems;
        PageIndex leafIndex;
        T * leaf = obtainLeafPageSafe(leafIndex, itemIndex);
        RandomAccessLeafOffset itemOffset = getLeafOffset(itemIndex);
        T * targetCell = leaf + itemOffset;
        assert(0 == memcmp(ZERO_BUFFER_FOR_COMPARE, targetCell, sizeof(T)));
        *targetCell = item;
        dc->releasePage(leafIndex);
        rootPage->numItems++;
    }

    void endOfData()
    {
    }

    DWORD getNumItems()
    {
        return rootPage->numItems;
    }

    StatisticsInfo * statistics()
    {
        StatisticsInfo * result = new StatisticsInfo;
        // One for the root page
        result->totalPages = 1;
        result->pagesInUse = 1;

        result->totalPages += rootPage->numItems / LEAF_PAGE_CAPACITY;
        result->totalPages += rootPage->numItems / ROOT_PAGE_CAPACITY;

        return result;
    }

protected:
    PagedDataContainer * dc;
    PageIndex    rootPageIndex;
    RandomAccessRootPage * rootPage;
    DEBUG_ONLY(DWORD _tag);

    RandomAccessOffsetInRoot getLevel2Offset(RandomAccessItemIndex itemIndex)
    {
        return itemIndex / ROOT_PAGE_CAPACITY;
    }

    RandomAccessOffsetInLevel2Page getLevel2PageOffset(RandomAccessItemIndex itemIndex)
    {
        return (itemIndex / LEAF_PAGE_CAPACITY) % LEAFS_IN_LEVEL2_ITEM;
    }

    RandomAccessLeafOffset getLeafOffset(RandomAccessItemIndex itemIndex)
    {
        return itemIndex % LEAF_PAGE_CAPACITY;
    }

    PageIndex * obtainLevel2PageSafe(PageIndex & level2PageIndex, RandomAccessItemIndex itemIndex)
    {
        PageIndex * level2Page = NULL;
        RandomAccessOffsetInRoot rootPageOffset = getLevel2Offset(itemIndex);
        level2PageIndex = rootPage->level2[rootPageOffset];
        if (0 == level2PageIndex)
        {
            level2Page = (PageIndex *)dc->newPage(&level2PageIndex);
            rootPage->level2[rootPageOffset] = level2PageIndex;
        }
        else
        {
            level2Page = (PageIndex *)dc->obtainPage(level2PageIndex);
        }
        DEBUG_PAGE_TAG(level2PageIndex, _tag + 3);
        return level2Page;
    }

    PageIndex * obtainLevel2Page(PageIndex & level2PageIndex, RandomAccessItemIndex itemIndex)
    {
        RandomAccessOffsetInRoot rootPageOffset = getLevel2Offset(itemIndex);
        level2PageIndex = rootPage->level2[rootPageOffset];
        assert(0 != level2PageIndex);
        PageIndex * level2Page = (PageIndex *)dc->obtainPage(level2PageIndex);
        DEBUG_PAGE_TAG(level2PageIndex, _tag + 3);
        return level2Page;
    }

    T * obtainLeafPageSafe(PageIndex * level2Page, PageIndex & leafIndex, RandomAccessItemIndex itemIndex)
    {
        T * leaf = NULL;
        RandomAccessOffsetInLevel2Page level2PageOffset = getLevel2PageOffset(itemIndex);
        leafIndex = level2Page[level2PageOffset];
        if (0 == leafIndex)
        {
            leaf = (T *)dc->newPage(&leafIndex);
            level2Page[level2PageOffset] = leafIndex;
        }
        else
        {
            leaf = (T *)dc->obtainPage(leafIndex);
        }
        DEBUG_PAGE_TAG(leafIndex, _tag + 4);
        return leaf;
    }

    T * obtainLeafPageSafe(PageIndex & leafIndex, RandomAccessItemIndex itemIndex)
    {
        PageIndex level2PageIndex;
        PageIndex * level2Page = obtainLevel2PageSafe(level2PageIndex, itemIndex);
        T * leaf = obtainLeafPageSafe(level2Page, leafIndex, itemIndex);
        dc->releasePage(level2PageIndex);
        return leaf;
    }

    T * obtainLeafPage(PageIndex * level2Page, PageIndex & leafIndex, RandomAccessItemIndex itemIndex)
    {
        RandomAccessOffsetInLevel2Page level2PageOffset = getLevel2PageOffset(itemIndex);
        leafIndex = level2Page[level2PageOffset];
        assert(0 != leafIndex);
        T * leaf = (T *)dc->obtainPage(leafIndex);
        DEBUG_PAGE_TAG(leafIndex, _tag + 4);
        return leaf;
    }

    T * obtainLeafPage(PageIndex & leafIndex, RandomAccessItemIndex itemIndex)
    {
        PageIndex level2PageIndex;
        PageIndex * level2Page = obtainLevel2Page(level2PageIndex, itemIndex);
        T * leaf = obtainLeafPage(level2Page, leafIndex, itemIndex);
        DEBUG_PAGE_TAG(leafIndex, _tag + 4);
        dc->releasePage(level2PageIndex);
        return leaf;
    }
};

