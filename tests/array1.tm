*:run [], []
*:run [], [8, 7, 6, 5, 4]
.DATA 4
.DATA 5
.DATA 6
.DATA 7
.DATA 8
0: LDC 3, 0(1)
1: LD 1, 1(0)
2: SUB 2, 3, 1
3: JGE 2, 17(0)
4: JLT 3, 13(0)
5: SUB 4, 3, 1
6: JGE 4, 13(0)
7: LDC 2, 2(0)
8: ADD 5, 2, 3
9: LD 5, 0(5)
10: OUT 5, 5, 5
11: LDA 3, 1(3)
12: LDA 7, 1(0)
13: LDC 1, -1(7)
14: OUT 1, 1, 1
15: OUTNL 0,0,0
16: LDA 7, 1(0)
17: OUTNL 0,0,0
