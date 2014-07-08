/* This file is Auto generated, do not change it. Change the templete. */


#include <wdm.h>
#include "offsets.h"

windows_offsets offsets_for_versions[] = {
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.1.2600.3093.exe */
	{
		{5, 1, 2600, 21},
		{0x124},
		{0x29c, 0x70},
		{0x22c, 0x20, 0x248, 0x18, 0x1ec},
		{0x18, 0x190},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.1.2600.5973.exe */
	{
		{5, 1, 2600, 85},
		{0x124},
		{0x29c, 0x70},
		{0x22c, 0x20, 0x248, 0x18, 0x1ec},
		{0x18, 0x190},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.1.2600.6055.exe */
	{
		{5, 1, 2600, 167},
		{0x124},
		{0x29c, 0x70},
		{0x22c, 0x20, 0x248, 0x18, 0x1ec},
		{0x18, 0x190},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.1.2600.6165.exe */
	{
		{5, 1, 2600, 21},
		{0x124},
		{0x29c, 0x70},
		{0x22c, 0x20, 0x248, 0x18, 0x1ec},
		{0x18, 0x190},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.2.3790.4922.exe */
	{
		{5, 2, 3790, 58},
		{0x124},
		{0x29c, 0x70},
		{0x224, 0x74, 0x240, 0x18, 0x1e4},
		{0x18, 0x180},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_5.2.3790.4998.exe */
	{
		{5, 2, 3790, 134},
		{0x124},
		{0x29c, 0x70},
		{0x224, 0x74, 0x240, 0x18, 0x1e4},
		{0x18, 0x180},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_6.0.6002.18005.exe */
	{
		{6, 0, 6002, 85},
		{0x124},
		{0x29c, 0x70},
		{0x248, 0x84, 0x260, 0x28, 0x20c},
		{0x18, 0x168},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_6.1.7600.16385.exe */
	{
		{6, 1, 7600, 1},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_6.1.7600.16695.exe */
	{
		{6, 1, 7600, 55},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_6.1.7600.16905.exe */
	{
		{6, 1, 7600, 9},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_WOW64_6.1.7600.16385.exe */
	{
		{6, 1, 7600, 1},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_WOW64_6.1.7600.16841.exe */
	{
		{6, 1, 7600, 201},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},
	/* ../windows_internals/ntosVersions\ntoskrnl_x86_WOW64_6.1.7601.17640.exe */
	{
		{6, 1, 7601, 232},
		{0x124},
		{0x29c, 0x70},
		{0x268, 0x88, 0x280, 0x28, 0x22c},
		{0x18, 0x188},
	},

    {
        {0, 0, 0, 0},
        {0},
        {0, 0},
        {0, 0, 0, 0},
        {0, 0},
    }
};

windows_offsets * find_windows_offsets(UINT32 * version)
{
    windows_offsets * offsets_iter  = offsets_for_versions;
    windows_offsets * most_fit      = offsets_for_versions;
    UINT32 current_delta = 0xffffffff;
    UINT32 temp_delta;
    for (
           offsets_iter = offsets_for_versions;
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
        KdPrint(( "Oregano: find_windows_offsets: Failed to find matching offsets\r\n" ));
    } else {
        KdPrint(( "Oregano: find_windows_offsets: Using offsets of version %d %d %d %d\r\n",
                    most_fit->version[0],
                    most_fit->version[1],
                    most_fit->version[2],
                    most_fit->version[3] ));
    }
    return most_fit;
}

