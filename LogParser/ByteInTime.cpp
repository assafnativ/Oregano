
#include "ByteInTime.hpp"

Cycle ByteInTimeGetCycle( ByteInTime const * x )
{
    return x->cycle;
}

ADDRESS ByteInTimeGetAddress( ByteInTime const * x )
{
    return x->addr;
}

