#include <wdm.h>
#include "offsets.h"

#ifdef AMD64
#include "offsets_AMD64.auto.h"
#else
#include "offsets_X86.auto.h"
#endif

windows_offsets * find_windows_offsets(UINT32 * version)
{
    windows_offsets * offsets_iter  = all_offsets;
    windows_offsets * most_fit      = all_offsets;
    UINT32 current_delta = 0xffffffff;
    UINT32 temp_delta;
    for (
           offsets_iter = all_offsets;
           (0 != offsets_iter->version[0]);
           ++offsets_iter ) {
        if (
                (offsets_iter->version[0] == version[0]) &&
                (offsets_iter->version[1] == version[1]) ) {

            if (version[2] > most_fit->version[2]) {
                temp_delta = version[2] - most_fit->version[2];
            } else {
                temp_delta = most_fit->version[2] - version[2];
            }
            if (temp_delta < current_delta) {
                most_fit = offsets_iter;
                current_delta = temp_delta;
            }
        }
    }
    if (current_delta > 0x100) {
        KdPrint(( "Oregano: find_windows_offsets: Failed to find matching (Offsets delta %x)\r\n", current_delta ));
    } else {
        KdPrint(( "Oregano: find_windows_offsets: Using offsets of version %d %d %d %d\r\n",
                    most_fit->version[0],
                    most_fit->version[1],
                    most_fit->version[2],
                    most_fit->version[3] ));
    }
    return most_fit;
}

