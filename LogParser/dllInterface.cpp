
#include "stdafx.h"

#include "dllInterface.hpp"

LogParser * createLogParser()
{
    return new LogParser();
}

void parseLog(LogParser * logParser, const char * fileName, Cycle maxCycle)
{
    logParser->parse(fileName, maxCycle);
    logParser->getLastCycle();
}

DWORD getLastCycle(LogParser * logParser) {return logParser->getLastCycle();}
DWORD getProcessorType(LogParser * logParser) {return logParser->getProcessorType();}
#ifdef X86
DWORD getEip(LogParser * logParser, DWORD cycle) {return logParser->eip(cycle);}
DWORD getEdi(LogParser * logParser, DWORD cycle) {return logParser->edi(cycle);}
DWORD getEsi(LogParser * logParser, DWORD cycle) {return logParser->esi(cycle);}
DWORD getEbp(LogParser * logParser, DWORD cycle) {return logParser->ebp(cycle);}
DWORD getEbx(LogParser * logParser, DWORD cycle) {return logParser->ebx(cycle);}
DWORD getEdx(LogParser * logParser, DWORD cycle) {return logParser->edx(cycle);}
DWORD getEcx(LogParser * logParser, DWORD cycle) {return logParser->ecx(cycle);}
DWORD getEax(LogParser * logParser, DWORD cycle) {return logParser->eax(cycle);}
DWORD getEflags(LogParser * logParser, DWORD cycle) {return logParser->eflags(cycle);}
DWORD getEsp(LogParser * logParser, DWORD cycle) {return logParser->esp(cycle);}
#elif AMD64
QWORD getRip(LogParser * logParser, DWORD cycle) {return logParser->rip(cycle);}
QWORD getRdi(LogParser * logParser, DWORD cycle) {return logParser->rdi(cycle);}
QWORD getRsi(LogParser * logParser, DWORD cycle) {return logParser->rsi(cycle);}
QWORD getRbp(LogParser * logParser, DWORD cycle) {return logParser->rbp(cycle);}
QWORD getRbx(LogParser * logParser, DWORD cycle) {return logParser->rbx(cycle);}
QWORD getRdx(LogParser * logParser, DWORD cycle) {return logParser->rdx(cycle);}
QWORD getRcx(LogParser * logParser, DWORD cycle) {return logParser->rcx(cycle);}
QWORD getRax(LogParser * logParser, DWORD cycle) {return logParser->rax(cycle);}
QWORD getR8 (LogParser * logParser, DWORD cycle) {return logParser->r8 (cycle);}
QWORD getR9 (LogParser * logParser, DWORD cycle) {return logParser->r9 (cycle);}
QWORD getR10(LogParser * logParser, DWORD cycle) {return logParser->r10(cycle);}
QWORD getR11(LogParser * logParser, DWORD cycle) {return logParser->r11(cycle);}
QWORD getR12(LogParser * logParser, DWORD cycle) {return logParser->r12(cycle);}
QWORD getR13(LogParser * logParser, DWORD cycle) {return logParser->r13(cycle);}
QWORD getR14(LogParser * logParser, DWORD cycle) {return logParser->r14(cycle);}
QWORD getR15(LogParser * logParser, DWORD cycle) {return logParser->r15(cycle);}
QWORD getRcs(LogParser * logParser, DWORD cycle) {return logParser->rcs(cycle);}
QWORD getRflags(LogParser * logParser, DWORD cycle) {return logParser->rflags(cycle);}
QWORD getRsp(LogParser * logParser, DWORD cycle) {return logParser->rsp(cycle);}
QWORD getRss(LogParser * logParser, DWORD cycle) {return logParser->rss(cycle);}
#endif
DWORD getThreadId(LogParser * logParser, DWORD cycle) {return (DWORD)(logParser->threadId(cycle));}
DWORD findEffectiveCycle(LogParser * logParser, DWORD regId, DWORD cycle) {return logParser->findEffectiveCycle(regId, cycle);};
MACHINE_LONG getRegValue(LogParser * LogParser, DWORD regId, DWORD cycle) {return LogParser->getRegValueById(regId, cycle);};
BYTE  getByte(LogParser * logParser, DWORD cycle, ADDRESS addr) {return logParser->getByte(cycle, addr);}
WORD  getWord(LogParser * logParser, DWORD cycle, ADDRESS addr) { return logParser->getWord(cycle, addr); }
DWORD getDword(LogParser * logParser, DWORD cycle, ADDRESS addr) { return logParser->getDword(cycle, addr); }
QWORD getQword(LogParser * logParser, DWORD cycle, ADDRESS addr) { return logParser->getQword(cycle, addr); }
void deleteLogParserObject(LogParser * logParser) { delete logParser; }

FindCycleWithEipValue * findCycleWithEipValue( LogParser * logParser, ADDRESS target, DWORD startCycle, DWORD endCycle )
{
    FindCycleWithEipValue * newFinder = new FindCycleWithEipValue(logParser);
    newFinder->newSearch(target, startCycle, endCycle);
    return newFinder;
}
FindCycleWithEipValue * findCycleWithEipValueReverse(LogParser * logParser, ADDRESS target, DWORD startCycle, DWORD endCycle)
{
    FindCycleWithEipValue * newFinder = new FindCycleWithEipValue(logParser);
    newFinder->newReverseSearch(target, startCycle, endCycle);
    return newFinder;
}
void    findCycleWithEipValueObjectNext(FindCycleWithEipValue * ctx)          { ctx->next(); }
void    findCycleWithEipValueObjectPrev(FindCycleWithEipValue * ctx)          { ctx->prev(); }
DWORD   findCycleWithEipValueObjectCurrent(FindCycleWithEipValue * ctx)       { return ctx->current(); }
BOOL    findCycleWithEipValueIsEndOfSearch(FindCycleWithEipValue * ctx)       { return ctx->isEndOfSearch(); }
void    findCycleWithEipValueObjectRestartSearch(FindCycleWithEipValue * ctx) { ctx->restartSearch(); }
void    findCycleWithEipValueDelete(FindCycleWithEipValue * ctx)              { delete ctx; }

FindChangingCycles * findChangingCycles( LogParser * logParser, ADDRESS addr, DWORD startCycle, DWORD endCycle)
{
    return logParser->findChangingCycles(addr, startCycle, endCycle);
}
void    findChangingCyclesNext(FindChangingCycles * ctx)          {ctx->next();}
Cycle   findChangingCyclesCurrent(FindChangingCycles * ctx)       {return ctx->current();}
void    findChangingCyclesRestartSearch(FindChangingCycles * ctx) {ctx->restartSearch();}
void    findChangingCyclesDelete(FindChangingCycles * ctx)        {delete ctx;}

FindData * findData( LogParser * logParser, const BYTE * data, DWORD dataLength, DWORD startCycle, DWORD endCycle )
{
    return logParser->findData(data, dataLength, startCycle, endCycle);
}
void    findDataNext(FindData * ctx) {ctx->next();}
const Address * findDataCurrent(FindData * ctx) { return ctx->current();}
void    findDataRestartSearch(FindData * ctx) {ctx->restartSearch();}
void    findDataDelete(FindData * ctx) {delete ctx;}

RegLogIterBase * regLogIter( LogParser * logParser, DWORD regId, DWORD cycle )
{
    return logParser->getRegLogIter(regId, cycle);
}
MACHINE_LONG regLogIterGetValue(RegLogIterBase * ctx)    {return ctx->getValue();};
DWORD        regLogIterGetCycle(RegLogIterBase * ctx)    {return ctx->getCycle();};
void         regLogIterNext(RegLogIterBase * ctx)        {ctx->next();};
void         regLogIterPrev(RegLogIterBase * ctx)        {ctx->prev();};
BOOL         regLogIterIsLastCycle(RegLogIterBase * ctx) {return INVALID_CYCLE == ctx->getCycle();};
void         regLogIterDelete(RegLogIterBase * ctx)      {delete ctx;};
