
#pragma once

#include <windows.h>
#include "LogConsts.hpp"
#include "PagedRandomAccess.hpp"
#include "RegLogIterBase.hpp"

typedef PagedRandomAccess<MACHINE_LONG> EipLogBase;

class EipLog: public EipLogBase
{
public:
    EipLog(DWORD rootIndex, PagedDataContainer * dc) : EipLogBase(rootIndex, dc)
    {
        return;
    }
};

class EipLogIter:RegLogIterBase
{
public:
    EipLogIter( EipLog * eipLog, DWORD startCycle=0 );
    virtual void next();
    virtual void prev();
    virtual DWORD getCycle() {return currentCycle;};
    virtual MACHINE_LONG getValue() {return currentCycle < eipLog->getNumItems() ? eipLog->getItem(currentCycle) : UNKNOWN_MACHINE_LONG;};
protected:
    DWORD currentCycle;
    EipLog * eipLog;
};