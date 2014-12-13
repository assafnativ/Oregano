#pragma once

#include "GlobalDefines.hpp"

class PageBase
{
public:
    PageBase * next;
    PageBase * prev;
    PageIndex index;
    long refCount;
    DWORD tag;

    virtual BYTE * getData() = 0;
    virtual DWORD getDataLength() = 0;

    PageBase(PageIndex index) :
        index(index),
        next(NULL),
        prev(NULL),
        // It must have a reference because something made this page in call
        refCount(1)
    {
        DEBUG_ONLY((tag = 0));
    };

    virtual ~PageBase(void) {};
};

