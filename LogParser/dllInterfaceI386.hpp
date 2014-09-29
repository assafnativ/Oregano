
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
#ifdef X86
LOG_PARSER_API DWORD getEip(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEdi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEsi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEbp(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEbx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEdx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEcx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEax(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEflags(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD getEsp(LogParser * logParser, DWORD cycle);
#elif AMD64
LOG_PARSER_API QWORD getRip(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRdi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRsi(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRbp(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRbx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRdx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRcx(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRax(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR8 (LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR9 (LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR10(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR11(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR12(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR13(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR14(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getR15(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRcs(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRflags(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRsp(LogParser * logParser, DWORD cycle);
LOG_PARSER_API QWORD getRss(LogParser * logParser, DWORD cycle);
#endif
LOG_PARSER_API DWORD getThreadId(LogParser * logParser, DWORD cycle);
LOG_PARSER_API DWORD findEffectiveCycle(LogParser * logParser, DWORD regId, DWORD cycle);
LOG_PARSER_API MACHINE_LONG getRegValue(LogParser * logParser, DWORD regId, DWORD cycle);

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
LOG_PARSER_API MACHINE_LONG regLogIterGetValue(RegLogIterBase * ctx);
LOG_PARSER_API DWORD        regLogIterGetCycle(RegLogIterBase * ctx);
LOG_PARSER_API void         regLogIterNext(RegLogIterBase * ctx);
LOG_PARSER_API void         regLogIterPrev(RegLogIterBase * ctx);
LOG_PARSER_API BOOL         regLogIterIsLastCycle(RegLogIterBase * ctx);
LOG_PARSER_API void         regLogIterDelete(RegLogIterBase * ctx);

}; // extern "C" 
