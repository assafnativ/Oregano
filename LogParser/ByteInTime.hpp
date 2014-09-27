
#pragma once

#include <Windows.h>
#include "LogConsts.hpp"
#include "Address.hpp"

#pragma pack(1)
class ByteInTime
{
	public:
        ByteInTime(Cycle cycle, ADDRESS addr, BYTE value) 
            : 
            cycle(cycle), 
            addr(addr), 
            value(value)
        {
            // pass
        };
        ByteInTime(Address address, BYTE value)
            :
            cycle(address.cycle),
            addr(address.addr),
            value(value)
        {
            // pass
        };
        ByteInTime()
            :
            cycle(INVALID_CYCLE),
            addr(0)
        {
            // pass
        }
        inline void copy(ByteInTime const * other)
        {
            if (NULL == other) 
            {
				clear();
            } else {
                addr    = other->addr;
                cycle   = other->cycle;
                value   = other->value;
            }
        }
		inline void clear()
		{
			addr = 0;
			cycle = INVALID_CYCLE;
			value = 0;
		}
        ADDRESS addr;
		Cycle   cycle;
		BYTE value;
};
#pragma pack()

Cycle ByteInTimeGetCycle(ByteInTime const * x); 
ADDRESS ByteInTimeGetAddress(ByteInTime const * x);
