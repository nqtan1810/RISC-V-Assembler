.text

#The program finds the value of fibonacci 

Fibo:
		addi    x23 , x0 , 0 // 0 2048
		addi    x16 , x0 , 1 // 4 2052
		addi    x30 , x0 , 1 // 8 2056
		addi    x24 , x0 , 3 // 12 2060
		beq     x23 , x0 , Result0 // 16 2064
		beq     x23 , x30 , Result1 // 20 2068
Loop: 
		blt     x23 , x24 , Result // 24 2072
		add     x14 , x16 , x30 // 28 2076
		addi    x16 , x30 , 0 // 32 2080
		addi    x30 , x14 , 0 // 36 2084
		addi    x24 , x24 , 1 // 40 2088
		jal     x0 , Loop // 44 2092
Result0:
		addi    x14 , x0 , 0 // 48 2096
		addi    x17 , x0 , 0 // 52 2100
		bne     x14 , x17 , Fail // 56 2104
Result1:
		addi    x14 , x0 , 1 // 60 2108
		addi    x27 , x0 , 1 // 64 2112
		bne     x14 , x27 , Fail // 68 2116
Result:
		addi    x18 , x0 , 0 // 72 2120
		bne     x14 , x18 , Result1 // 76 2124 

Pass: 
		addi    x1 , x0 , 084 // 2128
		jal     x0 , End  // 2132
Fail: 
		addi    x1 , x0 , 070 
End: 
