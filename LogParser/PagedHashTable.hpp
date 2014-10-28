#pragma once

#include "PagedDataContainer.hpp"
#include "PagedLinkedList.hpp"
#include "StatisticsInfo.hpp"

static const DWORD DEFAULT_HASH_TABLE_SIZE(0x10000);

// COMPERATOR returns int where:
//  0 is for items are identical
//  This is done to support CMP format in the future
typedef int (* ItemsCompareFunction)(void * x, void * key);
typedef DWORD (* ItemDigestFunction)(void * x);

// Forward declaration of the iterator:
template <class T, int SIZE, class KEY_TYPE, KEY_TYPE (*DIGEST)(T const * x), int (* COMPERATOR)(T const * x, KEY_TYPE key)>
class PagedHashTableIter;

template <class T, int SIZE, class KEY_TYPE, KEY_TYPE (*DIGEST)(T const * x), int (* COMPERATOR)(T const * x, KEY_TYPE key)>
class PagedHashTable
{
public:
    PagedHashTable(PageIndex pageIndex, PagedDataContainer * dc, DWORD tag)
        : 
            rootPageIndex(pageIndex),
            dataContainer(dc)
    {
        const DWORD rootPageSize = SIZE * sizeof(pageIndex);
        DEBUG_ONLY(_tag = tag);
        rootPage = (PageIndex *)dataContainer->obtainConsecutiveData(rootPageIndex, rootPageSize);
        if (0 == *rootPage) {
            // Table is not initialize,
            // Initialize it now.
            for (DWORD i = 0; SIZE > i; ++i) {
                dataContainer->newPage(&rootPage[i]);
                dataContainer->releasePage(rootPage[i]);
            }
        }
        for (DWORD i = 0; SIZE > i; ++i) {
            table[i] = new PagedLinkedList<T>(rootPage[i], dataContainer, tag);
        }
    }

    ~PagedHashTable(void)
    {
        endOfData();
        for (DWORD i = 0; SIZE > i; ++i) {
            delete table[i];
            table[i] = NULL;
        }
        dataContainer->releasePage(*rootPage);
    }

    void append(T item)
    {
        KEY_TYPE key = DIGEST(&item);
        DWORD bucketIndex = key % SIZE;
        PagedLinkedList<T> * bucket = table[bucketIndex];
        bucket->append(item);
    }

    void endOfData()
    {
        for (DWORD i = 0; SIZE > i; ++i) {
            if (NULL != table[i])
            {
                table[i]->endOfData();
            }
        }
    }

	StatisticsInfo * statistics()
	{
		StatisticsInfo * result = new StatisticsInfo;
		// One for the root page
		result->totalPages = 1;
		result->pagesInUse = 1;

		for (DWORD i = 0; SIZE > i; ++i) {
			GET_AND_ADD_STATS(result, table[i]);
		}

		return result;
	}

    friend class PagedHashTableIter<T, SIZE, KEY_TYPE, DIGEST, COMPERATOR>;

protected:
    PagedDataContainer * dataContainer;
    DWORD rootPageIndex;
    PageIndex * rootPage;
    PagedLinkedList<T> * table[SIZE];
    DEBUG_ONLY(DWORD _tag);

};

template <class T, int SIZE, class KEY_TYPE, KEY_TYPE (*DIGEST)(T const * x), int (* COMPERATOR)(T const * x, KEY_TYPE key)>
class PagedHashTableIter
{
protected:
    PagedHashTable<T, SIZE, KEY_TYPE, DIGEST, COMPERATOR> * hashTable;
    PagedLinkedListIter<T> * iter;
    KEY_TYPE key;
    DEBUG_ONLY(DWORD _tag);
public:
    PagedHashTableIter(PagedHashTable<T, SIZE, KEY_TYPE, DIGEST, COMPERATOR> * targetHashTable, KEY_TYPE key, DWORD tag)
        : 
        hashTable(targetHashTable),
        iter(NULL),
        key(key)
    {
        DEBUG_ONLY(_tag = tag);
        DWORD bucketIndex = key % SIZE;
        PagedLinkedList<T> * bucket = hashTable->table[bucketIndex];
        iter = new PagedLinkedListIter<T>(bucket, tag);
        findNext();
    }

    void releaseIter()
    {
        if (NULL != iter) {
            delete iter;
            iter = NULL;
        }
    }

    ~PagedHashTableIter()
    {
        releaseIter();
    }

    T const * current()
    {
        if (NULL != iter) {
            return iter->current();
        }
        return NULL;
    }

    void next()
    {
        if (NULL != iter) {
            iter->next();
            findNext();
        }
    }

    void findNext()
    {
        for (T const * item = iter->current(); NULL != item; iter->next(), item = iter->current()) {
            if (!COMPERATOR(item, key)) {
                return;
            }
        }
        releaseIter();
    }
};