*:run [17], []
*:run [-1], []
* write read + 0;
   0:     IN 1,0,0	read value
   1:    LDC 2,0(0)	int literal
   2:    ADD 3,1,2	binop: +
   3:    OUT 3,0,0
   4:  OUTNL 0,0,0	output \n
