#pragma once

#include "GlobalDefines.hpp"

class PageBase
{
public:
    PageBase * next;
    PageBase * prev;
    PageIndex index;
    volatile long refCount;
    DWORD accessCount;
    QWORD lastAccess;

    virtual BYTE * getData() = 0;
    virtual DWORD getDataLength() = 0;

    PageBase(PageIndex index) : 
        index(index),
        next(NULL),
        prev(NULL),
        refCount(0),
        accessCount(0),
        lastAccess(0)
    {
    };

    virtual ~PageBase(void) {};
};

