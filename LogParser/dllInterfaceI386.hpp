
#pragma once

#ifdef LOGPARSER_EXPORTS
#define LOG_PARSER_API __declspec( dllexport )
#else
#define LOG_PARSER_API __declspec( dllimport )
#endif

#include <windows.h>

#include "LogParser.hpp"

extern "C" {

LOG_PARSER_API LogParser * parseLog(const char * fileName);
LOG_PARSER_API DWORD getLastCycle(LogParser * logParser);
LOG_PARSER_API DWORD getProcessorType(LogParser * logParser);
LOG_PARSER_API DWORD eip(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD edi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD esi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD ebp(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD ebx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD edx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD ecx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD eax(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD eflags(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD esp(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD threadId(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD findEffectiveCycle(LogParser * logParser, DWORD regId, DWORD cycle);
LOG_PARSER_API DWORD getRegValue(LogParser * logParser, DWORD regId, DWORD cycle);

LOG_PARSER_API BYTE	 getByte (LogParser * logParser, DWORD cycle, DWORD addr);
LOG_PARSER_API WORD	 getWord (LogParser * logParser, DWORD cycle, DWORD addr);
LOG_PARSER_API DWORD getDword(LogParser * logParser, DWORD cycle, DWORD addr);
LOG_PARSER_API QWORD getQword(LogParser * logParser, DWORD cycle, DWORD addr);

LOG_PARSER_API void deleteLogParserObject(LogParser * logParser);

LOG_PARSER_API FindCycleWithEipValue * findCycleWithEipValue( LogParser * logParser, DWORD target, DWORD startCycle, DWORD endCycle );
LOG_PARSER_API void 	findCycleWithEipValueObjectNext(FindCycleWithEipValue * ctx);
LOG_PARSER_API DWORD	findCycleWithEipValueObjectCurrent(FindCycleWithEipValue * ctx);
LOG_PARSER_API BOOL     findCycleWithEipValueIsEndOfSearch(FindCycleWithEipValue * ctx);
LOG_PARSER_API void		findCycleWithEipValueObjectRestartSearch(FindCycleWithEipValue * ctx);
LOG_PARSER_API void		findCycleWithEipValueDelete(FindCycleWithEipValue * ctx);

LOG_PARSER_API FindChangingCycles * findChangingCycles( LogParser * logParser, DWORD addr, DWORD startCycle, DWORD endCycle) ;
LOG_PARSER_API void  	findChangingCyclesNext(FindChangingCycles * ctx);
LOG_PARSER_API Cycle 	findChangingCyclesCurrent(FindChangingCycles * ctx);
LOG_PARSER_API void		findChangingCyclesRestartSearch(FindChangingCycles * ctx);
LOG_PARSER_API void		findChangingCyclesDelete(FindChangingCycles * ctx);

LOG_PARSER_API FindData * findData( LogParser * logParser, const BYTE * data, DWORD dataLength, DWORD startCycle, DWORD endCycle );
LOG_PARSER_API void     findDataNext(FindData * ctx);
LOG_PARSER_API const Address * findDataCurrent(FindData * ctx);
LOG_PARSER_API void		findDataRestartSearch(FindData * ctx);
LOG_PARSER_API void		findDataDelete(FindData * ctx);

LOG_PARSER_API RegLogIterBase * regLogIter( LogParser * logParser, DWORD regId, DWORD cycle );
LOG_PARSER_API DWORD    regLogIterGetValue(RegLogIterBase * ctx);
LOG_PARSER_API DWORD    regLogIterGetCycle(RegLogIterBase * ctx);
LOG_PARSER_API void     regLogIterNext(RegLogIterBase * ctx);
LOG_PARSER_API void     regLogIterPrev(RegLogIterBase * ctx);
LOG_PARSER_API BOOL     regLogIterIsLastCycle(RegLogIterBase * ctx);
LOG_PARSER_API void     regLogIterDelete(RegLogIterBase * ctx);

}; // extern "C" 
