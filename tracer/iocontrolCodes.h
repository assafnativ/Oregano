
#ifndef _IOCONTROL_CODES_H_
#define _IOCONTROL_CODES_H_

#define IOCTL_INIT_OREGANO      CTL_CODE( FILE_DEVICE_UNKNOWN, 0x801, METHOD_NEITHER, FILE_ALL_ACCESS )
#define IOCTL_DEBUG_PRINT       CTL_CODE( FILE_DEVICE_UNKNOWN, 0x802, METHOD_NEITHER, FILE_ALL_ACCESS )

#define IOCTL_ADD_TRACE_RANGE   CTL_CODE( FILE_DEVICE_UNKNOWN, 0x803, METHOD_NEITHER, FILE_ALL_ACCESS )
typedef struct _addTraceRangeInfo {
    ADDRESS stopAddress;
    ADDRESS rangeStart;
    ADDRESS rangeEnd;
} addTraceRangeInfo;

#define IOCTL_SET_PROCESS_INFO  CTL_CODE( FILE_DEVICE_UNKNOWN, 0x804, METHOD_NEITHER, FILE_ALL_ACCESS )
typedef struct _setProcessInfo {
    /* In user land process ids are DWORDs while in kernel land they are HANDLEs.
        this causes a mixing and casting a lot.
        http://www.osronline.com/showthread.cfm?link=161223 */
    unsigned int    processId;
    unsigned int    threadId;
} setProcessInfo;

#define IOCTL_START_TRACE       CTL_CODE( FILE_DEVICE_UNKNOWN, 0x805, METHOD_NEITHER, FILE_ALL_ACCESS )
#define IOCTL_STOP_TRACE        CTL_CODE( FILE_DEVICE_UNKNOWN, 0x806, METHOD_NEITHER, FILE_ALL_ACCESS )

#define IOCTL_GET_LAST_BREAK_POINT_INFO CTL_CODE( FILE_DEVICE_UNKNOWN, 0x807, METHOD_NEITHER, FILE_ALL_ACCESS )

#define IOCTL_PROBE_TRACE       CTL_CODE( FILE_DEVICE_UNKNOWN, 0x808, METHOD_NEITHER, FILE_ALL_ACCESS )
typedef struct trace_info_s {
    unsigned int    buffer_pos;
    unsigned int    trace_counter;
    void *          buffer;
    unsigned int    buffer_index;
    unsigned int    used_buffers;
    unsigned int    is_trace_stopped;
} trace_info_t;

#define IOCTL_READ_BUFFER       CTL_CODE( FILE_DEVICE_UNKNOWN, 0x809, METHOD_NEITHER, FILE_ALL_ACCESS )

#endif /* _IOCONTROL_CODES_H_ */
