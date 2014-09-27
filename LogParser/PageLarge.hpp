#pragma once

#include "pagebase.hpp"

class PageLarge :
    public PageBase
{
public:
    PageLarge(PageIndex index, DWORD dataLength) : PageBase(index), dataLength(dataLength)
    {
        data = new BYTE[dataLength];
    };
    virtual ~PageLarge(void)
    {
        if (NULL != data) {
            delete [] data;
        }
        data = NULL;
    };
    virtual BYTE * getData() {return data;};
    virtual DWORD getDataLength() {return dataLength;};

protected:
    DWORD dataLength;
    BYTE * data;
};

