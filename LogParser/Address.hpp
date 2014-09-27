
#pragma once

#include <Windows.h>
#include "LogConsts.hpp"
#include "globalDefines.hpp"

class Address
{
	public:
        Address(Cycle cycle, ADDRESS addr)
            : addr(addr), cycle(cycle) {};
        Address() {};
		inline void copy(Address * address) {addr = address->addr; cycle = address->cycle;};
		inline void clear() {addr = 0; cycle = INVALID_CYCLE;};
		ADDRESS addr;
		Cycle cycle;
};
