#pragma once

#include "pagebase.hpp"

static const DWORD PAGE_SIZE = 0x1000;

class PageCache :
    public PageBase
{
public:
    PageCache(PageIndex index) : PageBase(index) {};
    virtual ~PageCache(void)
    {
    };
    virtual BYTE * getData() {return data;};
    virtual DWORD getDataLength() {return PAGE_SIZE;};

protected:
    BYTE data[PAGE_SIZE];
};

