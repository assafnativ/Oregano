
#include "stdafx.h"

#include "MemoryBase.hpp"

MemoryBase::MemoryBase( PageIndex rootPage, PagedDataContainer * dc )
    : 
    dc(dc),
    rootPageIndex(rootPage)
{
}

MemoryBase::~MemoryBase(void)
{
    dc->releasePage(rootPageIndex);
}

