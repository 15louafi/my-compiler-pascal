;/ fct
	PUSH	labfinfct
	GOTO
labdebfct	EQU	*
afct	DS	1
	PUSH	afct
	SWAP
	STORE
;/ print...
	PUSH	3
	OUT
	GOTO
labfinfct	EQU	*
;/ fcta
	PUSH	labfinfcta
	GOTO
labdebfcta	EQU	*
afcta	DS	1
	PUSH	afcta
	SWAP
	STORE
b	DS	1
blength	DS	1
	PUSH	blength
	PUSH	1
	STORE	
	PUSH	b
	PUSH	4

	STORE	
bfcta	DS	1
bfctalength	DS	1
	PUSH	bfctalength
	PUSH	1
	STORE	
	PUSH	bfcta
	PUSH	8

	STORE	
;/ print...
	PUSH	afcta
	LOAD	
	PUSH	bfcta
	LOAD	
	ADD	
	OUT
	GOTO
labfinfcta	EQU	*
	PUSH	labcall0fct
	PUSH	3
	PUSH	labdebfct
	GOTO
labcall0fct	EQU	*
	PUSH	labcall1fcta
	PUSH	7
	PUSH	labdebfcta
	GOTO
labcall1fcta	EQU	*
;/ print...
	PUSH	b
	LOAD	
	OUT
	STOP

