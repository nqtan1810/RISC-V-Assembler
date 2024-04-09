.text

#The program to calculate the sum of the array
#The main purpose is to check the operation of memory instructions

Main:
		addi    x27 , x0 , 4        //0 512 
		add     x4 , x0 , x0        //4 513
		add     x10 , x0 , x0       //8 514
		addi    x19 , x0 , 32       //12 515
InArr:
		addi    x6 , x0 , 148       //16 516
		addi    x15 , x0 , 48       //20 517
		addi    x7 , x0 , 52        //24 518
		addi    x1 , x0 , 8         //28 519
		sw      x6 , 36 (x19)       //32 520
		sw      x15 , 40 (x19)      //36 521
		sw      x7 , 44 (x19)       //40 522
		sw      x1 , 48 (x19)       //44 523
Loop:
		slli    x2 , x10 , 2        //48 524
		add     x9, x2 , x19        //52 525
		lw      x30 , 36 (x9)       //56 526
		add     x4 , x4 , x30       //60 527
		addi    x10 , x10 , 1       //64 528
		beq     x10 , x27 , Result  //68 529
		jal     x0 , Loop           //72 530 
Result:
		addi    x25 , x0 , 256      //76 531
		bne     x25 , x4 , Fail     //80 532
Pass: 
		addi    x1 , x0 , 084       //84 533	
		jal     x0 , End            //88 534
Fail: 
		addi    x1 , x0 , 070       // 92
End:
		jal     x0, End             // 94
		addi    x1,  x0,  666       // 96
		sw      x1, 32(x0)          // 100
