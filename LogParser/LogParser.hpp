
#pragma once

#include <windows.h>

#include "PagedDataContainer.hpp"
#include "DBRootPage.hpp"
#include "LogConsts.hpp"
#include "Memory.hpp"
#include "Address.hpp"
#include "EipLog.hpp"
#include "RegLog.hpp"
#include "FileReader.hpp"

static const DWORD MAX_FILE_NAME = 0x200;
static const PCHAR LOG_DB_EXTENTION = ".oreganodb";
static const DWORD DB_OREGANO_MAGIC = 'OREG';
static const DWORD OREGANO_VERSION  = 2;

// Forward declaration
class OpcodesSideEffects;

class LogParser
{
	public:
		LogParser(const char * logFile);
		~LogParser();
        DWORD getLastCycle()            {return *lastCycle;};
        DWORD eip(DWORD cycle)			{return eipLog->getItem(cycle);};
		DWORD edi(DWORD cycle)			{return getRegValue<REG_ID_EDI>(cycle);};
		DWORD esi(DWORD cycle)			{return getRegValue<REG_ID_ESI>(cycle);};
		DWORD ebp(DWORD cycle)			{return getRegValue<REG_ID_EBP>(cycle);};
		DWORD ebx(DWORD cycle)			{return getRegValue<REG_ID_EBX>(cycle);};
		DWORD edx(DWORD cycle)			{return getRegValue<REG_ID_EDX>(cycle);};
		DWORD ecx(DWORD cycle)			{return getRegValue<REG_ID_ECX>(cycle);};
		DWORD eax(DWORD cycle)			{return getRegValue<REG_ID_EAX>(cycle);};
		DWORD ecs(DWORD cycle)			{return getRegValue<REG_ID_ECS>(cycle);};
		DWORD eflags(DWORD cycle)		{return getRegValue<REG_ID_EFLAGS>(cycle);};
		DWORD esp(DWORD cycle)			{return getRegValue<REG_ID_ESP>(cycle);};
		DWORD threadId(DWORD cycle)		{return getRegValue<THREAD_ID>(cycle);};
		DWORD findEffectiveCycle(DWORD regId, DWORD cycle);
        MACHINE_LONG getRegValueById(DWORD regId, DWORD cycle);
		DWORD findCycleWithEipValue(DWORD targetEip, DWORD startCycle, DWORD endCycle);
		DWORD findCycleWithRegValue(DWORD regId, DWORD targetValue, DWORD startCycle, DWORD endCycle);
		BYTE  getByte (Address address);
        WORD  getWord (Address address);
        DWORD getDword(Address address);
        QWORD getQword(Address address);
        BYTE  getByte (Cycle cycle, ADDRESS addr) {return memory->getByte (cycle, addr);};
        WORD  getWord (Cycle cycle, ADDRESS addr) {return memory->getWord (cycle, addr);};
        DWORD getDword(Cycle cycle, ADDRESS addr) {return memory->getDword(cycle, addr);};
        QWORD getQword(Cycle cycle, ADDRESS addr) {return memory->getQword(cycle, addr);};
        BYTE  getByte (ADDRESS addr) {return memory->getByte (*lastCycle, addr);};
        WORD  getWord (ADDRESS addr) {return memory->getWord (*lastCycle, addr);};
        DWORD getDword(ADDRESS addr) {return memory->getDword(*lastCycle, addr);};
        QWORD getQword(ADDRESS addr) {return memory->getQword(*lastCycle, addr);};
        BYTE * getStaticMemoryPointer(ADDRESS addr) {return memory->getStaticMemoryPointer(addr);};
        DWORD getProcessorType() { return *processorType; };
        RegLogIterBase * getRegLogIter(DWORD regId, DWORD cycle);
        FindChangingCycles * findChangingCycles(DWORD addr, DWORD startCycle, DWORD endCycle) {
            return new FindChangingCycles(memory, addr, startCycle, endCycle);
        }
        FindData * findData(const BYTE * data, DWORD dataLength, DWORD startCycle, DWORD endCycle) {
            return new FindData(memory, data, dataLength, startCycle, endCycle);
        }
		void DumpMemoryUsage();

        void setByte(ADDRESS addr, BYTE val);
#ifdef _DEBUG
		void * obtainPage(PageIndex index)  {return dataContainer->obtainPage(index);};
		void * obtainConsecutiveData(PageIndex index, DWORD length)  {return dataContainer->obtainConsecutiveData(index, length);};
		void   releasePage(PageIndex index) {dataContainer->releasePage(index);};

		StatisticsInfo * statisticsReg(DWORD regId)
		{
			if (REG_ID_EIP == regId)
			{
				return eipLog->statistics();
			}
			return reg[regId]->statistics();
		};
		StatisticsInfo * statisticsMemory() {return memory->statistics();};
#endif
	protected:
		template <int REG_ID>
		inline DWORD getRegValue(DWORD cycle)
		{
			DWORD index = reg[REG_ID]->findEffectiveIndex(cycle);
			if (index >= reg[REG_ID]->getNumItems()) {
				return UNKNOWN_DWORD;
			}
			return reg[REG_ID]->getItem(index).value;
		}
        inline DWORD getEffectiveRegCycle(DWORD regId, DWORD cycle)
        {
            if ((0 == regId) || (NUMBER_OF_REGS >= regId)) {
                return INVALID_CYCLE;
            }
            return reg[regId]->findEffectiveCycle(cycle);
        }
		BOOL parseLog(FileReader &log);
        BOOL parseTrace(FileReader &log);
        BOOL parseModulesInfo(FileReader &log);
        BOOL parseRangesInfo(FileReader &log);
        void initContext();
        void initMemory();
		void addRegChange(RegLog * regLog);
        DWORD findRegEffectiveIndex(DWORD regId, DWORD cycle);
        DWORD readSectionTag();
        OpcodesSideEffects * opcodesSideEffects;

        EipLog * getEipLog() const { return eipLog; };
        RegLog * getRegLog(DWORD regId) const { return reg[regId]; };

    protected:
        PagedDataContainer * dataContainer;
		FileReader log;
		RegLog * reg[NUMBER_OF_REGS];
		EipLog * eipLog;
        Memory * memory;
        DBRootPage * rootPage;
		DWORD * lastCycle;
        DWORD * logVersion;
        DWORD * processorType;
        DWORD * logHasMemory;
		friend class FindCycleWithEipValue;
        friend class BX_CPU_C;
        friend class BX_MEM_C;
}; /* LogParser */

class FindCycleWithEipValue
{
	public:
		FindCycleWithEipValue(LogParser * logParser);
		void restartSearch();
		void newSearch( DWORD target, DWORD startCycle, DWORD endCycle );
		BOOL isEndOfSearch() {return isDone;};
		void next();
        void prev();
        Cycle current();
    protected:
        void findNext();
        void findPrev();
		LogParser *	logParser;
        DWORD       target;
		DWORD		currentCycle;
		DWORD		bottomCycle;
		DWORD		topCycle;
		BOOL		isDone;
		EipLog *	eipLog;
}; /* FindCycleWithEipValue */
