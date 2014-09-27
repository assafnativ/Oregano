
#include "dllInterfaceI386.hpp"

LogParser * parseLog(const char * fileName)
{
    return new LogParser(fileName);
}
DWORD getLastCycle(LogParser * logParser) {return logParser->getLastCycle();}
DWORD getProcessorType(LogParser * logParser) {return logParser->getProcessorType();}
DWORD eip(LogParser * logParser, DWORD cycle) {return logParser->eip(cycle);}
DWORD edi(LogParser * logParser, DWORD cycle) {return logParser->edi(cycle);}
DWORD esi(LogParser * logParser, DWORD cycle) {return logParser->esi(cycle);}
DWORD ebp(LogParser * logParser, DWORD cycle) {return logParser->ebp(cycle);}
DWORD ebx(LogParser * logParser, DWORD cycle) {return logParser->ebx(cycle);}
DWORD edx(LogParser * logParser, DWORD cycle) {return logParser->edx(cycle);}
DWORD ecx(LogParser * logParser, DWORD cycle) {return logParser->ecx(cycle);}
DWORD eax(LogParser * logParser, DWORD cycle) {return logParser->eax(cycle);}
DWORD eflags(LogParser * logParser, DWORD cycle) {return logParser->eflags(cycle);}
DWORD esp(LogParser * logParser, DWORD cycle) {return logParser->esp(cycle);}
DWORD threadId(LogParser * logParser, DWORD cycle) {return logParser->threadId(cycle);}
DWORD findEffectiveCycle(LogParser * logParser, DWORD regId, DWORD cycle) {return logParser->findEffectiveCycle(regId, cycle);};
DWORD getRegValue(LogParser * LogParser, DWORD regId, DWORD cycle) {return LogParser->getRegValueById(regId, cycle);};
BYTE  getByte(LogParser * logParser, DWORD cycle, DWORD addr) {return logParser->getByte(cycle, addr);}
WORD  getWord (LogParser * logParser, DWORD cycle, DWORD addr) {return logParser->getWord(cycle, addr);}
DWORD getDword(LogParser * logParser, DWORD cycle, DWORD addr) {return logParser->getDword(cycle, addr);}
QWORD getQword(LogParser * logParser, DWORD cycle, DWORD addr) {return logParser->getQword(cycle, addr);}
void deleteLogParserObject(LogParser * logParser) {delete logParser;}

FindCycleWithEipValue * findCycleWithEipValue( LogParser * logParser, DWORD target, DWORD startCycle, DWORD endCycle )
{
	FindCycleWithEipValue * newFinder = new FindCycleWithEipValue(logParser);
	newFinder->newSearch(target, startCycle, endCycle);
	return newFinder;
}
void    findCycleWithEipValueObjectNext(FindCycleWithEipValue * ctx)          {ctx->next();}
DWORD   findCycleWithEipValueObjectCurrent(FindCycleWithEipValue * ctx)       {return ctx->current();}
BOOL    findCycleWithEipValueIsEndOfSearch(FindCycleWithEipValue * ctx)       {return ctx->isEndOfSearch();}
void	findCycleWithEipValueObjectRestartSearch(FindCycleWithEipValue * ctx) {ctx->restartSearch();}
void	findCycleWithEipValueDelete(FindCycleWithEipValue * ctx)              {delete ctx;}

FindChangingCycles * findChangingCycles( LogParser * logParser, DWORD addr, DWORD startCycle, DWORD endCycle)
{
    return logParser->findChangingCycles(addr, startCycle, endCycle);
}
void            findChangingCyclesNext(FindChangingCycles * ctx)          {ctx->next();}
Cycle           findChangingCyclesCurrent(FindChangingCycles * ctx)       {return ctx->current();}
void	        findChangingCyclesRestartSearch(FindChangingCycles * ctx) {ctx->restartSearch();}
void	        findChangingCyclesDelete(FindChangingCycles * ctx)        {delete ctx;}

FindData * findData( LogParser * logParser, const BYTE * data, DWORD dataLength, DWORD startCycle, DWORD endCycle )
{
    return logParser->findData(data, dataLength, startCycle, endCycle);
}
void    findDataNext(FindData * ctx) {ctx->next();}
const Address * findDataCurrent(FindData * ctx) { return ctx->current();}
void	findDataRestartSearch(FindData * ctx) {ctx->restartSearch();}
void	findDataDelete(FindData * ctx) {delete ctx;}

RegLogIterBase * regLogIter( LogParser * logParser, DWORD regId, DWORD cycle )
{
    return logParser->getRegLogIter(regId, cycle);
}
DWORD    regLogIterGetValue(RegLogIterBase * ctx)       {return ctx->getValue();};
DWORD    regLogIterGetCycle(RegLogIterBase * ctx)       {return ctx->getCycle();};
void     regLogIterNext(RegLogIterBase * ctx)           {ctx->next();};
void     regLogIterPrev(RegLogIterBase * ctx)           {ctx->prev();};
BOOL     regLogIterIsLastCycle(RegLogIterBase * ctx)    {return INVALID_CYCLE == ctx->getCycle();};
void     regLogIterDelete(RegLogIterBase * ctx)         {delete ctx;};
