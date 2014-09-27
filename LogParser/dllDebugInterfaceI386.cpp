
#include "dllDebugInterfaceI386.hpp"

#ifdef _DEBUG

#define RETURN_STATS_FOR_REG(REG_NAME, REG_ID) \
LOG_PARSER_API void statistics##REG_NAME(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages) { \
	StatisticsInfo * stats = logParser->statisticsReg(REG_ID); \
	*pagesInUse = stats->pagesInUse; \
	*totalPages = stats->totalPages; \
	delete stats; \
	stats = NULL; \
}

RETURN_STATS_FOR_REG(Eip, REG_ID_EIP);
RETURN_STATS_FOR_REG(Edi, REG_ID_EDI);
RETURN_STATS_FOR_REG(Esi, REG_ID_ESI);
RETURN_STATS_FOR_REG(Ebp, REG_ID_EBP);
RETURN_STATS_FOR_REG(Ebx, REG_ID_EBX);
RETURN_STATS_FOR_REG(Edx, REG_ID_EDX);
RETURN_STATS_FOR_REG(Ecx, REG_ID_ECX);
RETURN_STATS_FOR_REG(Eax, REG_ID_EAX);
RETURN_STATS_FOR_REG(Eflags, REG_ID_EFLAGS);
RETURN_STATS_FOR_REG(Esp, REG_ID_ESP);
RETURN_STATS_FOR_REG(ThreadId, THREAD_ID);

LOG_PARSER_API void statisticsMemory(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages)
{
	StatisticsInfo * stats = logParser->statisticsMemory();

	*pagesInUse = stats->pagesInUse;
	*totalPages = stats->totalPages;

	delete stats;
	stats = NULL;
}

#endif // _DEBUG