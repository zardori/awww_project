;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 3.8.0 #10562 (Linux)
;--------------------------------------------------------
	.module compile_tmp
	.optsdcc -mz80
	
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _main
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _DATA
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area _INITIALIZED
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area _DABS (ABS)
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area _HOME
	.area _GSINIT
	.area _GSFINAL
	.area _GSINIT
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area _HOME
	.area _HOME
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area _CODE
;/mnt/d/studia/czwarty_semestr/awww/main_project/awww_project/compilation_8bit/compilation/compile_tmp.c:2: int main() {
;	---------------------------------
; Function main
; ---------------------------------
_main::
;/mnt/d/studia/czwarty_semestr/awww/main_project/awww_project/compilation_8bit/compilation/compile_tmp.c:4: return 0;
	ld	hl, #0x0000
;/mnt/d/studia/czwarty_semestr/awww/main_project/awww_project/compilation_8bit/compilation/compile_tmp.c:5: }
	ret
	.area _CODE
	.area _INITIALIZER
	.area _CABS (ABS)
