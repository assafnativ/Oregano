
#ifndef __INTERRUPTS_HOOKS_H__
#define __INTERRUPTS_HOOKS_H__

/* Would be used for calling the original interrupts */
extern unsigned int orgStackFaultInterrupt;
extern unsigned int orgGPFInterrupt;
extern unsigned int orgPageFaultInterrupt;

extern void stackFaultInterrupt( void );
extern void GPFInterrupt( void );
extern void PageFaultInterrupt( void );
#ifdef AMD64
extern void loadIdt64( OUT idt_t * idt );
extern void setInterrupt64(
                    IN	ADDRESS				idt,
					IN	unsigned char		interrupt_index,
					IN	interrupt_info_t *	new_interrupt );
#endif

#endif /* __INTERRUPTS_HOOKS_H__ */

