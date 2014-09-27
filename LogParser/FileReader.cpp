
#include "FileReader.hpp"

FileReader::FileReader(const char * fileName):
			        totalBytesRead(0)
{
	file =	CreateFileA(
					fileName,
					GENERIC_READ,
					FILE_SHARE_READ,
					NULL,
					OPEN_EXISTING,
					FILE_FLAG_SEQUENTIAL_SCAN,
					NULL );
	if (INVALID_HANDLE_VALUE == file) {
		/* Raise or something */
		fileSize = 0;
		return;
	}

	LARGE_INTEGER tempFileSize;
	if (FALSE == GetFileSizeEx(file, &tempFileSize)) {
		fileSize = 0;
		return;
	}
	fileSize = tempFileSize.LowPart;
}

FileReader::~FileReader()
{
	CloseHandle(file);
	file = NULL;
}

DWORD FileReader::ReadNullTermString(BYTE * output)
{
    BYTE * startPoint = output;
    BYTE byteRead = 0;

    do {
        byteRead = readByte();
        *output = byteRead;
        ++output;
    } while( 0 != byteRead );

    return output - startPoint;
}

void FileReader::readData( BYTE * outputBuffer, DWORD length )
{
    DWORD bytesRead;
    ReadFile(
        file,
        (LPVOID)(outputBuffer),
        length,
        &bytesRead,
        NULL);
    totalBytesRead += length;
    assert(bytesRead == length);
    return;
}
