.text

#The program checks the ALU instruction in R_type

Main:
		addi    x30 , x0 , 46 
		addi    x13 , x0 , -53 
		addi    x17 , x0 , 136 
		addi    x27 , x0 , 15 
		addi    x22 , x0 , 3 
		blt     x30 , x13 , Less_r 
		bge     x30 , x13 , Bigger_r 
Less_r:
		sub     x20 , x17 , x27 
		and     x23 , x17 , x27 
		slti    x23 , x23 , 106 
		srl     x23 , x23 , x22 
		addi    x3 , x0 , 16 
		bne     x23 , x3 , Fail 
Bigger_r:
		or      x20 , x17 , x27 
		xor     x23 , x17 , x27 
		sltiu   x23 , x23 , 93 
		sra     x23 , x23 , x22 
		addi    x3 , x0 , 34 
		bne     x23 , x3 , Fail 
Pass: 
		addi    x1 , x0 , 084 
		jal     x0 , End 
Fail: 
		addi    x1 , x0 , 070 
End: 
