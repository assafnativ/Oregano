
#pragma once

#include <Windows.h>
#include <assert.h>
#include "GlobalDefines.hpp"

class FileReader
{
	public:
		FileReader(const char * fileName);
		~FileReader();
        inline QWORD    readQword()     {return readType<QWORD>(); }
		inline DWORD	readDword()	    {return readType<DWORD>(); }
		inline WORD		readWord()	    {return readType<WORD>(); }
		inline BYTE		readByte()	    {return readType<BYTE>(); }
        inline ADDRESS  readPointer()   {return readType<ADDRESS>(); }
        DWORD           ReadNullTermString(BYTE * output);
        void            readData(BYTE * outputBuffer, DWORD length);
        void            aligenReadTo4();
		inline BOOL		isEof()		{return totalBytesRead >= fileSize; }
		inline DWORD	tell()		{return totalBytesRead;}
		inline void		closeFile()		{CloseHandle(file);}
	private:
		template <class TYPE>
		inline TYPE readType()
		{
			TYPE result;
			DWORD bytesRead;
			ReadFile(
				file,
				(LPVOID)(&result),
				sizeof(TYPE),
				&bytesRead,
				NULL);
            assert(bytesRead == sizeof(TYPE));
			totalBytesRead += sizeof(TYPE);
			return result;
		}
	private:
		HANDLE	file;
		DWORD	fileSize;
		DWORD	totalBytesRead;

};