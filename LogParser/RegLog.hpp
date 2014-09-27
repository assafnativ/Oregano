
#pragma once

#include <windows.h>

#include "GlobalDefines.hpp"
#include "LogConsts.hpp"
#include "RegValue.hpp"
#include "PagedRandomAccess.hpp"
#include "RegLogIterBase.hpp"

typedef PagedRandomAccess<RegValue> RegLogBase;

static RegValue InvalidRegValue = {INVALID_CYCLE, 0};

class RegLog: public RegLogBase
{
public:
    RegLog(char * reg_name, PageIndex rootIndex, PagedDataContainer * dc) : 
        RegLogBase(rootIndex, dc),
        name(reg_name)
    {
        return;
    }

    DWORD findEffectiveIndex(Cycle cycle)
    {
        return bsearchByCycle(cycle);
    }

    Cycle findEffectiveCycle(Cycle cycle)
    {
		DWORD itemIndex = findEffectiveIndex(cycle);
		if (itemIndex >= *numItems) {
			return INVALID_CYCLE;
		}
        return getItem(itemIndex).cycle;
    }

    friend class RegLogIter;

protected:
    char * name;
    // Returns an index
    DWORD bsearchByCycle(DWORD);
};


class RegLogIter: public RegLogIterBase
{
public:
    RegLogIter( RegLog * regLog, DWORD startCycle=0 );
    virtual void next();
    virtual void prev();
    virtual Cycle getCycle() {return currentCycle;};
    virtual MACHINE_LONG getValue() {return currentIndex < regLog->getNumItems() ? regLog->getItem(currentIndex).value : UNKNOWN_MACHINE_LONG;};
protected:
    Cycle currentCycle;
    DWORD currentIndex;
    RegLog * regLog;
};