
#pragma once

#ifdef _DEBUG

#ifdef LOGPARSER_EXPORTS
#define LOG_PARSER_API __declspec( dllexport )
#else
#define LOG_PARSER_API __declspec( dllimport )
#endif

#include <windows.h>

#include "LogParser.hpp"

extern "C"
{

LOG_PARSER_API void * obtainPage(LogParser * logParser, DWORD pageIndex) {return logParser->obtainPage(pageIndex);};
LOG_PARSER_API void * obtainConsecutivePage(LogParser * logParser, DWORD pageIndex, DWORD length) {return logParser->obtainConsecutiveData(pageIndex, length);};
LOG_PARSER_API void   releasePage(LogParser * LogParser, DWORD pageIndex) {LogParser->releasePage(pageIndex);};


LOG_PARSER_API void statisticsEip(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEdi(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEsi(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEbp(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEbx(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEdx(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEcx(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEax(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEflags(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsEsp(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsThreadId(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);
LOG_PARSER_API void statisticsMemory(LogParser * logParser, DWORD * pagesInUse, DWORD * totalPages);

}; // extern "C"

#endif // _DEBUG