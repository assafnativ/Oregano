
; This file must match the C header file with the same name
%ifdef X64
    ; Get it from PsGetCurrentProcess @ ntoskrnl.exe
    CURRENT_KTHREAD_OFFSET      equ 0188h
    %ifndef NT_VERSION
        %error Missing definition of NT_VERSION
    %elif   NT_VERSION >= 0x602
        KPROCESS_FROM_KTHREAD   equ 00b8h
    %elif   NT_VERSION >= 0x601
        KPROCESS_FROM_KTHREAD   equ 0070h
    %elif NT_VERSION >= 0x600
        KPROCESS_FROM_KTHREAD   equ 0070h
    %elif NT_VERSION >= 0x502
        KPROCESS_FROM_KTHREAD   equ 0068h
    %else
        %error "Unsupported building env"
    %endif

%endif ; !x64
