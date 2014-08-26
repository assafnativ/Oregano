
#ifndef _DRIVER_H_
#define _DRIVER_H_

/* Bullshit stuff */
#include "GlobalDefines.h"
/* Defines the io control codes */
#include "iocontrolCodes.h"
/* Defines structs that holds information about needed Windows offsets */
#include "offsets.h"

/* Oregano fine tuning consts */
/* NOTICE!
 * 	values here must match the values in the trap_interrupt.asm source and the PyOregano file */
#define LOG_BUFFER_SIZE					(0x4000)
#define LOG_BUFFER_NUM_OF_BUFFERS		(0x1000)
#define LOG_BUFFER_NUM_OF_BUFFERS_MASK	(0x0fff)
#define MAX_LOG_CYCLES                  (0xffffffff)

#define THREAD_CONTEXT_MAX_THREADS      (0x1000)
#define THREAD_ID_MASK                  (0x03ffc0)
#define THREAD_ID_IGNORED_BITS          (6)

#define MAX_LOG_RANGES                  (0x80)

/* Program consts & strings */
#define DRIVER_NAME			(L"\\Device\\Oregano")
#define DOS_DEVICE_NAME		(L"\\DosDevices\\Oregano")
#define OREGANO_MEMORY_TAG	((ULONG)'oNaG')

/* Structers declarations */
#ifdef AMD64
typedef struct ThreadContext_t {
    UINT64  ID;     /* 0x00 */
    UINT64  RDI;    /* 0x08 */
    UINT64  RSI;    /* 0x10 */
    UINT64  RBP;    /* 0x18 */
    UINT64  RBX;    /* 0x20 */
    UINT64  RDX;    /* 0x28 */
    UINT64  RCX;    /* 0x30 */
    UINT64  RAX;    /* 0x38 */
    UINT64  R8;     /* 0x40 */
    UINT64  R9;     /* 0x48 */
    UINT64  R10;    /* 0x50 */
    UINT64  R11;    /* 0x58 */
    UINT64  R12;    /* 0x60 */
    UINT64  R13;    /* 0x68 */
    UINT64  R14;    /* 0x70 */
    UINT64  R15;    /* 0x78 */
    ADDRESS RIP;    /* 0x80 */
    UINT64  RCS;    /* 0x88 */
    UINT64  RFLAGS; /* 0x90 */
    UINT64  RSP;    /* 0x98 */
    UINT64  RESERVED[12];
} ThreadContext;
#else
/* Keep the size of this struct 0x40 bytes */
typedef struct ThreadContext_t {
    UINT32  ID;     /* 0x00 */
    UINT32  EDI;    /* 0x04 */
    UINT32  ESI;    /* 0x08 */
    UINT32  EBP;    /* 0x0c */
    UINT32  EBX;    /* 0x10 */
    UINT32  EDX;    /* 0x14 */
    UINT32  ECX;    /* 0x18 */
    UINT32  EAX;    /* 0x1c */
    ADDRESS EIP;    /* 0x20 */
    UINT32  ECS;    /* 0x24 */
    UINT32  EFLAGS; /* 0x28 */
    UINT32  ESP;    /* 0x2c */
    UINT32  RESERVED[4];
} ThreadContext;
#endif

/* Defines logging range */
typedef struct LoggingRange_t {
    ADDRESS  BOTTOM_BOUND;
    ADDRESS  TOP_BOUND;
} LoggingRange;

/* Globals */
windows_offsets * offsets;

/* Functions declarations */
/*
 * DriverUnload
 * 	
 * 	Args:
 * 		driver_object
 *
 */
void		DriverUnload(	PDRIVER_OBJECT	driver_object );
/*
 * DriverEntry
 *
 * 	Args:
 * 			driver_object
 * 			rigistery_path
 */
NTSTATUS	DriverEntry(	PDRIVER_OBJECT	driver_object,
	   						PUNICODE_STRING	registry_path );
/*
 * default_irp_handler
 * 
 * This proc handles all the major functions that we do not implements.
 * 
 * 	Args:
 * 		device_object
 * 		irp
 */
NTSTATUS default_irp_handler( PDEVICE_OBJECT device_object, PIRP irp );
/*
 * on_close
 * 
 * Called when instance of the driver is closed (CloseHandle).
 * This function is responsible for unhooking int1.
 * 
 * 	Args:
 * 		device_object
 * 		irp
 */
NTSTATUS on_close( PDEVICE_OBJECT device_object, PIRP irp );
/*
 * on_create
 * 
 * Called when instance of the driver is created (CreateFile).
 * This function settes the int1 (Trap interrupt) hook.
 * 
 * 	Args:
 * 		device_object
 * 		irp
 */
NTSTATUS on_create( PDEVICE_OBJECT device_object, PIRP irp );
/*
 * on_device_control
 * 
 * called when an IOCTL is issued on the device handle (DeviceIoControl)
 * 
 * 	Args:
 * 		device_object
 * 		irp
 */
NTSTATUS on_device_control( PDEVICE_OBJECT device_object, PIRP irp );


#endif /* _DRIVER_H_ */
