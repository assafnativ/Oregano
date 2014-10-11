
/*
 * Oragano driver entry
 * Written by Assaf Nativ
 */

/* Includes */
#include <wdm.h>
#include "driver.h"
#include "trapInterrupt.h"

/* Set the functions types */
/* 
 * DriverEntry is needed only once, there for we set it to be Init,
 * which means The system can delete the page after we done with it.
 */
#pragma alloc_text( INIT, DriverEntry )

/* Functions definitions */
/* See header file for descriptions */
NTSTATUS	DriverEntry(	PDRIVER_OBJECT	driver_object,
	   						PUNICODE_STRING	registry_path )
{
	/* Not guilty till proved other wise */
	NTSTATUS        return_ntstatus	= STATUS_SUCCESS;
	/* Used for not so important functions */
	NTSTATUS        function_result = STATUS_SUCCESS;

	/* Would hold the information about the device, been allocated by the IoCreateDevice procedure */
	PDEVICE_OBJECT  device_object	= NULL;
	
	/* Would hold the driver name & dos device name, we must init unicode string for that */
	UNICODE_STRING  driver_name;
	UNICODE_STRING  dos_device_name;

	/* Loop iterator */
	unsigned int	i = 0;
	
    /* Would hold information about Windows version, for querying the right offsets */
    RTL_OSVERSIONINFOW version_info = {0};
    UINT32 windows_version[4] = {0};

	UNREFERENCED_PARAMETER(registry_path);

	KdPrint(( "Oregano: DriverEntry\r\n" ));

	/* Init strings to be valid unicode strings */
	RtlInitUnicodeString( &driver_name,		DRIVER_NAME );
	RtlInitUnicodeString( &dos_device_name,	DOS_DEVICE_NAME );

	/* Create me a device */
	return_ntstatus = IoCreateDevice(
							driver_object,
							0,							/* Device extension size, no extensions. */
							&driver_name,
							FILE_DEVICE_UNKNOWN,		/* Device type, there is no type for interrupt hook device. */
							FILE_DEVICE_SECURE_OPEN,	/* Device characteristics, allow file like access to the device. */
							FALSE,						/* Exclusive, I think i might need to change it to TRUE !TBD! */
							&device_object );			/* OUT */
	if( FALSE == NT_SUCCESS(return_ntstatus) ) {
		/* Create device failed */
		KdPrint(( "Oregano: IoCreateDevice faild due to %d\r\n", return_ntstatus ));
		goto RETURN_IO_CREATE_DEVICE_FAILD;
	}

	
	/* Set the driver IRP_MJ functions */
	/* First set them all to a default handler */
	for( i = 0; i < IRP_MJ_MAXIMUM_FUNCTION; ++i ) {
#pragma warning(suppress: 28169)
#pragma warning(suppress: 28023)
		driver_object->MajorFunction[i] = default_irp_handler;
	}
	/* Now set all the none default handlers, we set all the functions needed for IO control access type. */
	driver_object->MajorFunction[IRP_MJ_CLOSE]			= onClose;
	driver_object->MajorFunction[IRP_MJ_CREATE]			= onCreate;
	driver_object->MajorFunction[IRP_MJ_DEVICE_CONTROL]	= onDeviceControl;
	/* Set the unload function */
	driver_object->DriverUnload = DriverUnload;

	/* 
	 * Set device object flags, sets the I/O access to none buffered nor direct
	 * I am not so sure about it, if blue screen occurs I'll have to check it
	 * again !TBD! 
	 */
	device_object->Flags |= 0; // Yeah, I know it doesn't do anything, but it is there for me to remember.

	/*
	 * We are not required to clear this flag in the DriverEntry as the I/O Manager will
	 * clear it for us, but we will anyway. Creating a device in any other location and 
	 * we would have needed to clear it.
	 */
	device_object->Flags &= (~DO_DEVICE_INITIALIZING);

	/* Create me a symbolic link to the device. */
	IoCreateSymbolicLink( &dos_device_name, &driver_name );
	if( FALSE == NT_SUCCESS(function_result) ) {
		KdPrint(( "Oregano: faild to create a symbolic link for the device\r\n" ));
	}

    /* Get the right Windows offsets */
    function_result = RtlGetVersion(&version_info);
    if (FALSE == NT_SUCCESS(function_result) ) {
        KdPrint(( "Oregano: failed to query Windows version\r\n" ));
        return function_result;
    }
    windows_version[0] = version_info.dwMajorVersion;
    windows_version[1] = version_info.dwMinorVersion;
    windows_version[2] = version_info.dwBuildNumber;
    windows_version[3] = 0;
    KdPrint(( "Oregano: Running on Windows version: %d, %d, %d, %d\r\n", 
        windows_version[0],
        windows_version[1],
        windows_version[2],
        windows_version[3] ));
    /* Set the offsets global var */
    offsets = find_windows_offsets(windows_version);

    for (unsigned int i = 0; i < LOG_BUFFER_NUM_OF_BUFFERS; ++i)
    {
        log_buffer_item[i] = NULL;
    }

    /* TODO: On unload clear the trap on branch flag */
    isTrapOnBranchSet = 0;

	/* No error occurred */
	KdPrint(( "Oregano: device n' driver were created and loaded\r\n" ));
	

/* Function epilog */
RETURN_IO_CREATE_DEVICE_FAILD:
// DRIVER_ENTERY_RETURN: // Unreferenced label for now.
	KdPrint(( "Oregano: DriverEntery say bye bye.\r\n" ));
	return( return_ntstatus );
} /* DriverEntry */

/*
* The unload function is needed in the end, so we can not discard it
* until then.
*/
#pragma alloc_text( PAGE_CODE_LOCKED, DriverUnload )
void DriverUnload( PDRIVER_OBJECT	driver_object )
{
	/* Hold hold functions return codes */
	NTSTATUS	function_result = STATUS_SUCCESS;
	
	/* Would hold the dos device name, needed for deleting of the symbolic link */
	UNICODE_STRING	dos_device_name;

    PAGED_CODE_LOCKED();

	KdPrint(( "Oregano: DriverUnload\r\n" ));

	RtlInitUnicodeString( &dos_device_name, DOS_DEVICE_NAME );

	/* Delete the symbolic link */
	function_result = IoDeleteSymbolicLink( &dos_device_name );
	if( FALSE == NT_SUCCESS(function_result) ) {
		KdPrint(( "Oregano: failed to delete symbolic link\r\n" ));
		/* It's not so bad, we can carry on. */
	}

	/* Delete the device */
	IoDeleteDevice( driver_object->DeviceObject );

	/* Void return nothing, thats a clean up function,
	 * therefor we do not care whether it succeeded or not. */
	return;
} /* DriverUnload */

