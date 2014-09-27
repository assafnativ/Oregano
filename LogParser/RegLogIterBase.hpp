
#pragma once

#include "GlobalDefines.hpp"
#include "LogConsts.hpp"

class RegLogIterBase
{
public:
    virtual void next() = 0;
    virtual void prev() = 0;
    virtual DWORD getCycle() = 0;
    virtual MACHINE_LONG getValue() = 0;
};