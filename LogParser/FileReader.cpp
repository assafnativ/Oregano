
#include "stdafx.h"

#include "FileReader.hpp"

FileReader::FileReader() :
                file(NULL),
                fileSize(0),
                totalBytesRead(0)
{

}

void FileReader::openFile(const char * fileName)
{
    close();
    file =  CreateFileA(
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

void FileReader::close()
{
    if (NULL != file)
    {
        CloseHandle(file);
    }
    file = NULL;
    totalBytesRead = 0;
    fileSize = 0;
}

FileReader::~FileReader()
{
    close();
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

    return (DWORD)(output - startPoint);
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

void FileReader::aligenReadTo4()
{
    DWORD bytesRead;
    char outputBuffer[4];
    DWORD paddingBytes = 4 - totalBytesRead & 3;
    if (4 == paddingBytes)
    {
        return;
    }
    ReadFile(
        file,
        (LPVOID)(&outputBuffer),
        paddingBytes,
        &bytesRead,
        NULL);
    totalBytesRead += paddingBytes;
    assert(bytesRead == paddingBytes);
    return;
}
