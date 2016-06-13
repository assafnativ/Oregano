
#ifndef _GLOBALDEFINES_H_
#define _GLOBALDEFINES_H_

/************************************************************
 * File name: GlobalDefines.h                               *
 * Dates:                                                   *
 *          24.10.03                                        *
 * Author:  Assaf                                           *
 * Purpose: Declares some defines and consts values for the *
 *              use of all other cpp or header files.       *
 ************************************************************/

#ifndef IN
#   define IN
#endif
#ifndef OUT
#   define OUT
#endif
#ifndef INOUT
#   define INOUT
#endif
#ifndef FALSE
#   define FALSE (0)
#endif
#ifndef TRUE
#   define TRUE (!FALSE)
#endif

#ifndef UNREFERENCED_PARAMETER
#   define UNREFERENCED_PARAMETER(P) (P)
#endif

#define READ_FROM_OFFSET( ptr, offset, result_type ) ( *((result_type *)(((UCHAR *)ptr) + offset)) )
#define ADD_OFFSET( ptr, offset, result_type ) ( (result_type)(((UCHAR *)ptr) + offset) )

/* Typedefs */
typedef unsigned int        UINT32;
typedef unsigned short      UINT16;
typedef unsigned char       UINT8;

typedef unsigned char *     ADDRESS;
typedef int                 OFFSET;

#ifdef AMD64
typedef unsigned long long MACHINE_LONG;
#elif i386
typedef unsigned long MACHINE_LONG;
#endif

#define UNKNOWN_DWORD_VALUE (0x3f3f3f3f)
#define UNKNOWN_QWORD_VALUE (0x3f3f3f3f3f3f3f3f)
#endif
