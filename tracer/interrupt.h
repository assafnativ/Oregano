
#ifndef _INTERRUPT_H_
#define _INTERRUPT_H_

#include "GlobalDefines.h"

/* Structs declations */
#pragma pack(1)

typedef struct idt_s {
    unsigned short  limit;      /* WORD */
    unsigned char * base;       /* DWORD / QWORD */
    unsigned short  reserved;
} idt_t;

#ifdef i386
/* Entery in the idt vector */
typedef struct interrupt_info_s {
    unsigned short  low_offset;     /* WORD */
    unsigned short  selector;       /* WORD */
    unsigned char   access;         /* BYTE */
    unsigned char   unused;         /* BYTE */
    unsigned short  high_offset;    /* WORD */
} interrupt_info_t;

#elif AMD64
/* Entery in the idt vector */
typedef struct interrupt_info_s {
    unsigned short  low_offset;     /* WORD */
    unsigned short  selector;       /* WORD */
    unsigned char   ist_index;      /* 3 BTIS ist 5 BITS reserved0 */
    unsigned char   type;           /* 5 BITS type 2 BITS dpl 1 BIT present */
    unsigned short  middle_offset;  /* WORD */
    unsigned long   high_offset;    /* DWORD */
    unsigned long   reserved;       /* DWORD */
} interrupt_info_t;

#endif
#pragma pack()

/* Interrupt hook info */
typedef struct interruptHookInfo_s {
    unsigned int    index;
    ADDRESS *       accessableOrgIntAddress;
    ADDRESS         newInterrupt;
    interrupt_info_t intInfo;
} InterruptHookInfo;

extern InterruptHookInfo interruptsHooks[];

/*
 * load_idt
 *
 *  args:
 *      idt     - Struct containg limit and base filed to be filled
 *                  with the sidt opcode.
 *
 */
#ifndef AMD64
void load_idt( OUT idt_t * idt );
#endif

/*
 * get_interrupt_info
 *
 *  args:
 *      idt                 - The idt pointer
 *      interrupt_index     - Which interrupt do you want?
 *      interrupt_info      - Would hold the information about the interrupt.
 *
 */
void get_interrupt_info(
                        IN  idt_t *             idt,
                        IN  unsigned char       interrupt_index,
                        OUT interrupt_info_t *  interrupt_info );

/*
 * set_interrupt
 *
 *  args:
 *      idt             - The idt pointer
 *      interrupt_index - Which interrupt do you want?
 *      new_interrupt   - Pointer to the new interrupt procedure to be installed.
 *
 */
#ifndef AMD64
void set_interrupt(
                    IN  ADDRESS             idt,
                    IN  unsigned char       interrupt_index,
                    IN  interrupt_info_t *  new_interrupt );

#endif

/*
 * hookAllCPUs
 *
 *  args:
 *      interrupt_index - Which interrupt do you want to hook
 *      new_interrupt   - Info about the new interrupt to install
 *
 */
void hookAllCPUs(
                IN  unsigned char       interruptIndex,
                IN  interrupt_info_t *  newInterrupt );

#endif /* _INTERRUPT_H_ */
