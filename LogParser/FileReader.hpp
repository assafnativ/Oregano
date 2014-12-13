
#pragma once

#include <Windows.h>
#include <assert.h>
#include "GlobalDefines.hpp"

class FileReader
{
	public:
		FileReader();
		~FileReader();
        void openFile(const char * fileName);
        void close();
        inline QWORD    readQword()     { return readType<QWORD>(); }
		inline DWORD	readDword()	    { return readType<DWORD>(); }
		inline WORD		readWord()	    { return readType<WORD>(); }
		inline BYTE		readByte()	    { return readType<BYTE>(); }
        inline ADDRESS  readPointer()   { return readType<ADDRESS>(); }
        DWORD           ReadNullTermString(BYTE * output);
        void            readData(BYTE * outputBuffer, DWORD length);
        void            aligenReadTo4();
		inline BOOL		isEof()		{ return totalBytesRead >= fileSize; }
		inline DWORD	tell()		{ return totalBytesRead; }
		inline void		closeFile()		{ CloseHandle(file); }
	private:
		template <class TYPE>
		inline TYPE readType()
		{
			TYPE result;
			DWORD bytesRead;
			BOOL readResult = ReadFile(
				                file,
				                (LPVOID)(&result),
				                sizeof(TYPE),
				                &bytesRead,
				                NULL);
            assert((bytesRead == sizeof(TYPE)) && (0 != readResult));
			totalBytesRead += sizeof(TYPE);
			return result;
		}
	private:
		HANDLE	file;
		DWORD	fileSize;
		DWORD	totalBytesRead;
};
