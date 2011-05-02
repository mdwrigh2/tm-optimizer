0: LD  5, 6(0)
1: LDC 1, 3(0)
2: SUB 2, 0, 1
3: JGE 2, 5(7)	  jump to end of loop
4: LD  3, 6(0)
5: LDC 4, 1(0)
6: ADD 5, 3, 4
7: ST  5, 6(0)
8: LDA 7, -9(7)   branch back to 0:
