
#pragma once

#include <windows.h>

class StatisticsInfo
{
public:
	DWORD totalPages;
	DWORD pagesInUse;
};

#define GET_AND_ADD_STATS(X, Y) \
			StatisticsInfo * tempStats = Y->statistics(); \
			X->totalPages += tempStats->totalPages; \
			X->pagesInUse += tempStats->pagesInUse; \
			delete tempStats; \
			tempStats = NULL